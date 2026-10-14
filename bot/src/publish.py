#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10,<3.14"
# dependencies = []
# ///
"""Open a pull request that adds the minutes of one meeting to the Meetings repository.

The script uses the GitHub CLI (`gh`). If CROW_APP_ID and CROW_APP_KEY are set, it operates as
the GitHub App of the bot (see github_app.py). If not, it uses the `gh` login. It sends only
`minutes.md` and the review notes. The transcript, the evidence file, and the audio stay on this computer.

    uv run publish.py out/test1 --series "CAM Meetup" --series-dir cam --date 2026-10-06

The pull request adds `meetings/<series directory>/<date>/minutes.md` on the branch
`minutes/<series directory>/<date>`. A second run for the same meeting updates the file on that
branch and does not open a second pull request.
"""
import argparse
import base64
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

REVIEW_DAYS = 7

PR_BODY = """\
An automated agent (Crow) made these minutes from a transcript of the meeting. This pull request \
merges automatically {days} days after it opens, if nobody stops it.

## Review procedure

- [ ] Make sure that each decision and each action item is correct, and that it names the correct person.
- [ ] Correct or remove each item that has the mark *(review)*, then remove the mark. \
The automatic merge does not occur while a mark remains.
- [ ] Correct wrong technical terms and display names. For a mistake that repeats, add a line to \
`bot/corrections.txt` in a separate pull request.

To correct the minutes, push a commit to this branch or add suggestions in a review. To stop the \
automatic merge, add the label `hold` or request changes. To publish before the {days} days, merge \
the pull request.

## Review notes

{notes}
"""


def gh(*args: str, body: dict | None = None, check: bool = True) -> subprocess.CompletedProcess:
    """Run one GitHub CLI command. A JSON body goes to the command on standard input."""
    command = ["gh", *args] + (["--input", "-"] if body is not None else [])
    try:
        result = subprocess.run(command, input=json.dumps(body) if body is not None else None, capture_output=True, text=True)
    except FileNotFoundError:
        sys.exit("The GitHub CLI is not installed. Install `gh` and run: gh auth login")
    if check and result.returncode != 0:
        sys.exit(f"GitHub error ({' '.join(args[:2])}): {(result.stderr or result.stdout).strip()[:500]}")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("directory", type=Path, help="capture directory with minutes.md")
    parser.add_argument("--series", required=True, help='name of the meeting series, for example "CAM Meetup"')
    parser.add_argument("--series-dir", required=True, help="directory name of the series in the repository, for example cam")
    parser.add_argument("--date", required=True, help="date of the meeting, YYYY-MM-DD")
    parser.add_argument("--repo", default="FreeCAD/Meetings", help="GitHub repository (default: FreeCAD/Meetings)")
    parser.add_argument("--tag", help="suffix of the minutes file names, as given to minutes.py")
    parser.add_argument("--dry-run", action="store_true", help="print the pull request and stop")
    args = parser.parse_args()

    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.date):
        sys.exit("The date must have the format YYYY-MM-DD.")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", args.series_dir):
        sys.exit("The series directory name can contain only lower-case letters, digits, and hyphens.")

    suffix = f"-{args.tag}" if args.tag else ""
    minutes_file = args.directory / f"minutes{suffix}.md"
    notes_file = args.directory / f"minutes-review{suffix}.md"
    if not minutes_file.exists():
        sys.exit(f"{minutes_file} does not exist. Run minutes.py first.")
    minutes = minutes_file.read_text()
    # Remove the title of the notes file, because the pull request text has its own heading.
    notes = re.sub(r"\A# .*\n+", "", notes_file.read_text()).strip() if notes_file.exists() else "No review notes."

    path = f"meetings/{args.series_dir}/{args.date}/minutes.md"
    branch = f"minutes/{args.series_dir}/{args.date}"
    title = f"Minutes: {args.series}, {args.date}"
    body = PR_BODY.format(days=REVIEW_DAYS, notes=notes)

    if args.dry_run:
        print(f"repository: {args.repo}\nbranch:     {branch}\nfile:       {path}\ntitle:      {title}\n\n{body}")
        return

    if os.environ.get("CROW_APP_ID"):
        # Get a new token here, because a token from the start of the meeting can be expired.
        token = subprocess.run(["uv", "run", str(HERE / "github_app.py"), "--repo", args.repo],
                               capture_output=True, text=True)
        if token.returncode != 0:
            sys.exit(f"No token of the GitHub App: {token.stderr.strip()[-500:]}")
        os.environ["GH_TOKEN"] = token.stdout.strip()

    base = gh("api", f"repos/{args.repo}", "--jq", ".default_branch").stdout.strip()
    if gh("api", f"repos/{args.repo}/contents/{path}?ref={base}", check=False).returncode == 0:
        sys.exit(f"{path} is already on the branch {base}. The minutes of this meeting are published.")

    base_sha = gh("api", f"repos/{args.repo}/git/ref/heads/{base}", "--jq", ".object.sha").stdout.strip()
    created = gh("api", f"repos/{args.repo}/git/refs", body={"ref": f"refs/heads/{branch}", "sha": base_sha}, check=False)
    if created.returncode != 0 and "already exists" not in created.stdout + created.stderr:
        sys.exit(f"GitHub error (create branch): {(created.stderr or created.stdout).strip()[:500]}")

    # The update of a file needs the hash of the old file.
    old = gh("api", f"repos/{args.repo}/contents/{path}?ref={branch}", "--jq", ".sha", check=False)
    content = {
        "message": f"Add minutes of {args.series}, {args.date}",
        "content": base64.b64encode(minutes.encode()).decode(),
        "branch": branch,
    }
    if old.returncode == 0:
        content["sha"] = old.stdout.strip()
    gh("api", "-X", "PUT", f"repos/{args.repo}/contents/{path}", body=content)

    # The workflow merge-minutes.yml merges only pull requests with the label "minutes".
    # The command fails if the label exists, so ignore the result.
    gh("label", "create", "minutes", "--repo", args.repo, "--color", "0e8a16",
       "--description", "Minutes from the notetaker bot. Merges automatically after the review period.", check=False)
    gh("label", "create", "hold", "--repo", args.repo, "--color", "d93f0b",
       "--description", "Stops the automatic merge of minutes.", check=False)

    url = gh("pr", "list", "--repo", args.repo, "--head", branch, "--state", "open", "--json", "url", "--jq", ".[0].url").stdout.strip()
    if url:
        gh("pr", "edit", url, "--add-label", "minutes")
        print(f"updated the pull request: {url}")
    else:
        url = gh("pr", "create", "--repo", args.repo, "--base", base, "--head", branch, "--title", title,
                 "--body", body, "--label", "minutes").stdout.strip()
        print(f"opened the pull request: {url}")


if __name__ == "__main__":
    main()
