#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10,<3.14"
# dependencies = ["icalendar>=6", "recurring-ical-events>=3"]
# ///
"""Read the public calendar and start the bot for each meeting.

The scheduler reads the calendar and the series list in `bot/series.json`. Two minutes before a
meeting starts, it starts `run-meeting.sh`, which records the meeting, makes the minutes, and
opens the pull request.

    uv run scheduler.py              operate until Ctrl+C
    uv run scheduler.py --dry-run    print the meetings of the next 7 days and stop
"""
import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

import icalendar
import recurring_ical_events

HERE = Path(__file__).resolve().parent
JOIN_BEFORE = dt.timedelta(minutes=2)
EXTRA_MINUTES = 60  # a meeting can continue after its end time in the calendar


def log(message: str) -> None:
    print(f"[{dt.datetime.now():%Y-%m-%d %H:%M:%S}] {message}", flush=True)


def find_series(config: dict, summary: str) -> dict | None:
    return next((s for s in config["series"] if s["match"].lower() in summary.lower()), None)


def find_room(config: dict, event) -> str | None:
    """The first link to a permitted Jitsi host in the location or the description."""
    text = f"{event.get('LOCATION', '')} {event.get('DESCRIPTION', '')}"
    for url in re.findall(r"https://[^\s<>\"')]+", text):
        if urlparse(url).hostname in config["jitsi_hosts"]:
            return url.rstrip(".,;")
    return None


def meetings(config: dict, calendar, start: dt.datetime, end: dt.datetime) -> list[dict]:
    """The meetings between two times, with the decision for each one."""
    result = []
    for event in recurring_ical_events.of(calendar).between(start, end):
        begin, finish = event["DTSTART"].dt, event["DTEND"].dt
        summary = str(event.get("SUMMARY", ""))
        meeting = {"summary": summary, "skip": None}
        if not isinstance(begin, dt.datetime):
            meeting.update(start=None, skip="an event for the full day")
        else:
            series = find_series(config, summary)
            room = find_room(config, event)
            # The date of a meeting is the date in the time zone of its calendar entry.
            meeting.update(start=begin.astimezone(dt.timezone.utc), end=finish.astimezone(dt.timezone.utc), date=f"{begin:%Y-%m-%d}", room=room)
            if str(event.get("STATUS", "")).upper() == "CANCELLED":
                meeting["skip"] = "cancelled"
            elif series is None:
                meeting["skip"] = "the series is not in series.json"
            elif series.get("deny"):
                meeting["skip"] = "the series is on the deny list"
            elif room is None:
                meeting["skip"] = "no link to a permitted Jitsi host"
            else:
                meeting.update(name=series["name"], dir=series["dir"])
        result.append(meeting)
    return sorted((m for m in result if m["start"]), key=lambda m: m["start"])


def describe(meeting: dict) -> str:
    when = f"{meeting['start'].astimezone():%a %Y-%m-%d %H:%M}"
    if meeting["skip"]:
        return f"{when}  {meeting['summary']}: no record ({meeting['skip']})"
    return f"{when}  {meeting['summary']}: record {meeting['room']} -> meetings/{meeting['dir']}/{meeting['date']}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--config", type=Path, default=HERE.parent / "series.json")
    parser.add_argument("--refresh-minutes", type=float, default=15, help="read the calendar again after this time (default 15)")
    parser.add_argument("--dry-run", action="store_true", help="print the meetings of the next 7 days and stop")
    args = parser.parse_args()
    config = json.loads(args.config.read_text())

    def read_calendar():
        with urllib.request.urlopen(config["calendar"], timeout=60) as response:
            return icalendar.Calendar.from_ical(response.read())

    now = dt.datetime.now(dt.timezone.utc)
    if args.dry_run:
        for meeting in meetings(config, read_calendar(), now, now + dt.timedelta(days=7)):
            print(describe(meeting))
        return

    # Find configuration errors now, not after a meeting.
    for name in ("INFOMANIAK_API_KEY", "INFOMANIAK_PRODUCT_ID"):
        if not os.environ.get(name):
            sys.exit(f"Set the {name} environment variable.")
    # With the GitHub App of the bot, check that the app gives a token. Without it, check the gh login.
    github_check = (["uv", "run", str(HERE / "github_app.py")] if os.environ.get("CROW_APP_ID")
                    else ["gh", "auth", "status"])
    for command in (["uv", "run", str(HERE / "minutes.py"), "--list-models"], github_check):
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            sys.exit(f"The check `{' '.join(command[:4])}` failed:\n{(result.stderr or result.stdout).strip()[-1000:]}")
    log("the configuration is correct")

    calendar, read_at, shown = None, 0.0, set()
    running: list[tuple[str, subprocess.Popen]] = []
    try:
        while True:
            if time.monotonic() - read_at > args.refresh_minutes * 60 or calendar is None:
                try:
                    calendar = read_calendar()
                except Exception as e:  # keep the last calendar if the server does not answer
                    log(f"calendar error: {e}")
                    if calendar is None:
                        time.sleep(60)
                        continue
                read_at = time.monotonic()
                now = dt.datetime.now(dt.timezone.utc)
                for meeting in meetings(config, calendar, now, now + dt.timedelta(hours=24)):
                    if describe(meeting) not in shown:
                        shown.add(describe(meeting))
                        log(f"calendar: {describe(meeting)}")

            now = dt.datetime.now(dt.timezone.utc)
            for meeting in meetings(config, calendar, now - dt.timedelta(hours=12), now + dt.timedelta(hours=1)):
                if meeting["skip"] or not meeting["start"] - JOIN_BEFORE <= now < meeting["end"]:
                    continue
                key = f"{meeting['dir']}-{meeting['date']}"
                # The output directory shows that this meeting started before, also after a restart.
                if (HERE / "out" / key).exists():
                    continue
                minutes = int((meeting["end"] - now).total_seconds() / 60) + EXTRA_MINUTES
                log(f"start the bot: {meeting['name']}, {meeting['room']}")
                (HERE / "out" / key).mkdir(parents=True)
                running.append((key, subprocess.Popen(
                    [str(HERE / "run-meeting.sh"), meeting["room"], meeting["name"], meeting["dir"], meeting["date"], str(minutes)])))

            for key, process in list(running):
                if process.poll() is not None:
                    running.remove((key, process))
                    log(f"{key}: {'complete' if process.returncode == 0 else f'FAILED (exit code {process.returncode})'}, see out/{key}/run.log")
            time.sleep(20)
    except KeyboardInterrupt:
        # Ctrl+C also goes to the bots, which then stop the capture and make the minutes.
        for key, process in running:
            log(f"wait for {key}")
            process.wait()


if __name__ == "__main__":
    main()
