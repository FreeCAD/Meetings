#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10,<3.14"
# dependencies = ["anthropic>=1.0", "pydantic>=2"]
# ///
"""Make meeting minutes from a transcript with a hosted or a local model.

With the Infomaniak backend (the default) and the Claude backend, only the text transcript goes
to the API. With the Ollama backend, no data leaves this computer. The audio stays on this
computer in all cases.

    uv run minutes.py out/test1 --series "CAM Meetup" --date 2026-10-06

The script writes three files into the capture directory:

    minutes.md             the public minutes (no quotes, no time stamps)
    minutes-review.md      notes for the reviewer: items with low confidence and removed items
    minutes-evidence.json  private: the transcript quotes that support each item
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Literal

import anthropic
from pydantic import BaseModel, create_model

HERE = Path(__file__).resolve().parent
CLAUDE_MODEL = "claude-opus-5-5"
INFOMANIAK_URL = "https://api.infomaniak.com/2/ai/{product}/openai/v1"
BOT_NAME_MARK = "Notetaker"
REPO_URL = "https://github.com/FreeCAD/Meetings/tree/main/bot"

# The system prompt and the meeting context are the same for the two calls, and the task comes
# last. Thus the second call can use the prompt cache of the first call again.
SYSTEM = """\
You work on the minutes of public meetings of the FreeCAD open-source community. The minutes are \
published in a public GitHub repository after a review period, so a wrong statement \
about what a named person decided, promised, or opposed does real harm. An incomplete record is \
acceptable; an invented one is not.

The transcript comes from automatic speech-to-text. Each participant was recorded on a separate \
audio track, so the speaker label of each line is reliable even when the words are not. Expect \
wrong words, especially technical terms and names. The glossary lists terms that the community \
uses; use it to read the transcript, and write those terms in their correct form. The \
corrections are rules from the maintainers about mistakes that earlier minutes made. Obey each \
correction.

A line with "(chat)" after the name is a message that the participant typed in the meeting chat. \
Its text is exact. Participants use the chat for links, names of issues and pull requests, and \
short comments on what is said at that time. Treat a chat message as part of the discussion. When a \
link or a reference from the chat belongs to a topic, a decision, or an action item, give it there \
and copy it character for character. Leave chat messages that have no relation to the meeting out.

The minutes have four kinds of items:

- Topic: a subject that the meeting discussed, with a short neutral summary of what was said.
- Decision: something that the participants agreed to do or to adopt, in this meeting. One person \
who describes a plan has not made a decision. A decision needs the clear agreement of the others.
- Action item: a task that one person said they will do, or that the meeting gave to a person who \
accepted it. The owner is the person who will do the task.
- Proposal or objection: a proposal is a concrete suggestion for a change or a plan ("I suggest we \
move the release to March", "My plan is to write the document and open a PR"). An objection is \
disagreement with a proposal, or a concern about it ("I don't think that works, because it breaks \
old files").

These are not items, and most lines of a meeting are in this group: agreement and approval ("sounds \
good", "I like it", "makes sense", "yes"), questions, explanations, greetings, small talk, \
technical problems with the call, and words that a participant clearly said to someone outside the \
meeting. Agreement is never an objection. Many meetings have no objections and no decisions.
"""

DRAFT_TASK = """\
Write the minutes of this meeting.

- Topics: do not attribute ordinary discussion to named persons more than is necessary.
- Give a decision, an action item, a proposal, or an objection only when the transcript clearly \
shows it. If the meeting has none of a kind, return an empty list for that kind. Do not fill lists.
- For each decision, action item, proposal, and objection, give one or more quotes from the \
transcript that support it. Copy each quote word for word from one line of the transcript, with \
the speaker and the start time of that line. A program checks each quote against the transcript \
and removes items whose quotes it cannot find.
- For each topic, give in "links" each web address from a chat message that belongs to the topic. \
Copy each address character for character. Give an empty list if the topic has none.
- If an agenda for this meeting is given, use its items as the topics where the discussion matches \
them. Leave out agenda items that the meeting did not discuss.
- If a rolling agenda is given, it is one document for all meetings of the series. It can contain \
items of earlier meetings, items that are complete, and items for later meetings. The series can add \
new items at the top or at the bottom, and the meeting can work through the items from the top \
down or from the bottom up. Do not assume a direction. Use date headings and marks in the agenda, \
and most of all the transcript, to find the items that this meeting discussed. Use those items as \
the topics, with the wording of the agenda. Do not report an agenda item that the transcript does \
not show.
- Give the topics in the sequence in which the meeting discussed them.
"""

REVIEW_TASK = """\
The draft items below come from a first pass over this meeting. Check each item against the \
transcript before reviewers read it. Judge each item on its own; do not let a confident \
draft persuade you.

Give one verdict for each item, with the item's kind and index:

- supported: the transcript shows this, the item has the right kind, and the right person is named.
- partly: the item has the right kind, but a detail is stronger than the transcript shows.
- unsupported: the transcript does not show this, or the wrong person is named, or the item has \
the wrong kind. Examples of a wrong kind: agreement that the draft calls an objection, a plan of \
one person that the draft calls a decision, a question that the draft calls a proposal.

Say in one sentence what is wrong when the verdict is not "supported".
"""


class Topic(BaseModel):
    title: str
    summary: str
    links: list[str]


class Verdict(BaseModel):
    kind: Literal["decision", "action_item", "statement"]
    index: int
    verdict: Literal["supported", "partly", "unsupported"]
    reason: str


class Review(BaseModel):
    verdicts: list[Verdict]


def make_draft_schema(attendees: list[str]) -> type[BaseModel]:
    """The schema of the draft. Each name field accepts only a name from the attendee list."""
    Name = Literal[tuple(attendees)]  # type: ignore[valid-type]
    Evidence = create_model("Evidence", start_s=(float, ...), speaker=(Name, ...), quote=(str, ...))
    Decision = create_model("Decision", text=(str, ...), evidence=(list[Evidence], ...))
    ActionItem = create_model("ActionItem", owner=(Name, ...), task=(str, ...), evidence=(list[Evidence], ...))
    Statement = create_model("Statement", speaker=(Name, ...), text=(str, ...),
                             kind=(Literal["proposal", "objection"], ...), evidence=(list[Evidence], ...))
    return create_model("Draft", topics=(list[Topic], ...), decisions=(list[Decision], ...),
                        action_items=(list[ActionItem], ...), statements=(list[Statement], ...))


def normalize(text: str) -> str:
    return " ".join(re.sub(r"[^a-z0-9 ]+", " ", text.lower()).split())


def load_events(directory: Path) -> tuple[list[str], list[dict]]:
    """The attendees and the chat messages of a capture.

    The attendees are the display names of all participants, in the sequence that they joined.
    The last name of a participant wins. A chat message has the form of a transcript utterance.
    """
    events = [json.loads(line) for line in (directory / "events.jsonl").read_text().splitlines() if line]
    names: dict[str, str] = {}
    for event in events:
        if event.get("type") in ("participant_joined", "name_changed") and event.get("name"):
            names[event["participantId"]] = event["name"]
    attendees = list(dict.fromkeys(n for n in names.values() if BOT_NAME_MARK not in n))
    chat = []
    for event in events:
        # A person who left before the bot joined is not an attendee, so their message has no speaker.
        speaker = names.get(event.get("participantId")) if event.get("type") == "chat" else None
        if speaker in attendees and event.get("text", "").strip():
            start = 0.0 if event.get("beforeCapture") else event["t"]
            chat.append({"start_s": start, "end_s": start, "participantId": event["participantId"],
                         "speaker": speaker, "text": event["text"].strip(), "chat": True})
    return attendees, chat


def load_corrections(path: Path) -> tuple[list[tuple[re.Pattern, str]], list[str]]:
    """The spelling corrections ("wrong -> right") and the rules of the corrections file."""
    lines = [t.strip() for t in path.read_text().splitlines()] if path.exists() else []
    spelling, rules = [], []
    for line in lines:
        if not line or line.startswith("#"):
            continue
        wrong, arrow, right = line.partition("->")
        if arrow and wrong.strip() and right.strip():
            spelling.append((re.compile(rf"\b{re.escape(wrong.strip())}\b", re.IGNORECASE), right.strip()))
            rules.append(f'Write "{right.strip()}", not "{wrong.strip()}".')
        else:
            rules.append(line)
    return spelling, rules


def quote_found(evidence, utterances: list[dict], window_s: float = 90.0) -> bool:
    """True if the quote is in the words of that speaker near that time."""
    quote = normalize(evidence.quote)
    nearby = " ".join(
        u["text"] for u in utterances
        if u["speaker"] == evidence.speaker and abs(u["start_s"] - evidence.start_s) <= window_s
    )
    return bool(quote) and quote in normalize(nearby)


def ask_ollama(model: str, url: str, think: bool, system: str, content: str, output_format: type[BaseModel]):
    """Ask a local model through the Ollama API. The JSON schema constrains the answer."""
    # Ollama cuts the prompt without a warning if it is longer than num_ctx, so make the context
    # large enough. Round the value up, so that the two calls use one loaded model.
    num_predict = 6000
    num_ctx = max(8192, (len(system) + len(content)) // 3 + 2 * num_predict)
    num_ctx = -(-num_ctx // 8192) * 8192
    body = {
        "model": model,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": content}],
        "format": output_format.model_json_schema(),
        "stream": False,
        "think": think,
        "keep_alive": "30m",
        "options": {"temperature": 0, "num_ctx": num_ctx, "num_predict": num_predict},
    }
    request = urllib.request.Request(f"{url}/api/chat", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    started = time.monotonic()
    try:
        with urllib.request.urlopen(request, timeout=4 * 3600) as response:
            answer = json.load(response)
    except urllib.error.HTTPError as e:
        sys.exit(f"Ollama error {e.code}: {e.read().decode(errors='replace')[:500]}")
    except urllib.error.URLError as e:
        sys.exit(f"No connection to Ollama at {url}: {e.reason}. Start it with: ollama serve")

    print(f"  {model}: {answer.get('prompt_eval_count')} input tokens, {answer.get('eval_count')} output tokens, "
          f"{time.monotonic() - started:.0f} s", flush=True)
    if answer.get("prompt_eval_count", 0) + answer.get("eval_count", 0) >= num_ctx:
        sys.exit("The transcript is too long for the context of the local model.")
    if answer.get("done_reason") == "length":
        sys.exit("The local model did not complete its answer (output limit).")
    try:
        return output_format.model_validate_json(answer["message"]["content"])
    except ValueError as e:
        sys.exit(f"The local model gave an answer that does not agree with the schema: {e}")


def infomaniak_request(product: str, path: str, body: dict | None = None) -> dict:
    """Send one request to the OpenAI-compatible API of Infomaniak AI Tools."""
    key = os.environ.get("INFOMANIAK_API_KEY")
    if not key:
        sys.exit("No API key. Set the INFOMANIAK_API_KEY environment variable.")
    if not product:
        sys.exit("No product ID. Set the INFOMANIAK_PRODUCT_ID environment variable.")
    request = urllib.request.Request(
        INFOMANIAK_URL.format(product=product) + path,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=1800) as response:
            return json.load(response)
    except urllib.error.HTTPError as e:
        sys.exit(f"Infomaniak API error {e.code}: {e.read().decode(errors='replace')[:800]}")
    except urllib.error.URLError as e:
        sys.exit(f"No connection to the Infomaniak API: {e.reason}")


def ask_infomaniak(product: str, model: str, think: bool, system: str, content: str, output_format: type[BaseModel]):
    """Ask a hosted model. The JSON schema constrains the answer."""
    body = {
        "model": model,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": content}],
        "response_format": {"type": "json_schema", "json_schema": {
            "name": output_format.__name__, "schema": output_format.model_json_schema(), "strict": True}},
        "temperature": 0,
        "max_tokens": 16000,
    }
    if not think:
        # Qwen thinks before it answers by default. The chat template has a switch for that.
        body["chat_template_kwargs"] = {"enable_thinking": False}
    started = time.monotonic()
    answer = infomaniak_request(product, "/chat/completions", body)

    usage = answer.get("usage") or {}
    print(f"  {answer.get('model', model)}: {usage.get('prompt_tokens')} input tokens, "
          f"{usage.get('completion_tokens')} output tokens, {time.monotonic() - started:.0f} s", flush=True)
    choice = answer["choices"][0]
    if choice.get("finish_reason") == "length":
        sys.exit("The hosted model did not complete its answer (output limit).")
    text = re.sub(r"<think>.*?</think>", "", choice["message"].get("content") or "", flags=re.DOTALL).strip()
    try:
        return output_format.model_validate_json(text)
    except ValueError as e:
        sys.exit(f"The hosted model gave an answer that does not agree with the schema: {e}")


def ask_claude(client: anthropic.Anthropic, system: str, content: str, output_format: type[BaseModel]):
    try:
        response = client.beta.messages.parse(
            model=CLAUDE_MODEL,
            max_tokens=16000,
            system=system,
            messages=[{"role": "user", "content": content}],
            output_format=output_format,
            output_config={"effort": "high"},
            # If a safety classifier declines the request, the API runs it again on the fallback model.
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
        )
    except TypeError as e:
        # The SDK raises TypeError when it finds no credentials.
        if "authentication" not in str(e):
            raise
        sys.exit("No API credentials. Set the ANTHROPIC_API_KEY environment variable.")
    except anthropic.AuthenticationError:
        sys.exit("The API key is not valid. Set ANTHROPIC_API_KEY.")
    except anthropic.RateLimitError as e:
        sys.exit(f"Rate limit. Try again after {e.response.headers.get('retry-after', '60')} seconds.")
    except anthropic.APIStatusError as e:
        sys.exit(f"API error {e.status_code}: {e.message}")
    except anthropic.APIConnectionError as e:
        sys.exit(f"Network error: {e}")

    if response.stop_reason == "refusal":
        sys.exit(f"The model declined the request: {response.stop_details}")
    if response.stop_reason == "max_tokens" or response.parsed_output is None:
        sys.exit(f"The model did not complete its answer (stop reason: {response.stop_reason}).")

    usage = response.usage
    print(f"  {response.model}: {usage.input_tokens} input tokens, {usage.output_tokens} output tokens", flush=True)
    return response.parsed_output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("directory", type=Path, nargs="?", help="capture directory")
    parser.add_argument("--series", help='name of the meeting series, for example "CAM Meetup"')
    parser.add_argument("--date", help="date of the meeting, YYYY-MM-DD")
    parser.add_argument("--transcript", type=Path, help="transcript .jsonl file (default: transcript-large-v3-turbo.jsonl)")
    parser.add_argument("--agenda", type=Path, help="agenda.md of the meeting, if there is one")
    parser.add_argument("--rolling-agenda", type=Path, help="agenda.md of the series, if the series uses one agenda for all meetings")
    parser.add_argument("--glossary", type=Path, default=HERE.parent / "glossary.txt")
    parser.add_argument("--corrections", type=Path, default=HERE.parent / "corrections.txt")
    parser.add_argument("--backend", choices=["infomaniak", "ollama", "claude"], default="infomaniak",
                        help="infomaniak: a hosted model at Infomaniak AI Tools (default). "
                             "ollama: a local model, no data leaves this computer. claude: the Claude API")
    parser.add_argument("--infomaniak-model", default=os.environ.get("INFOMANIAK_MODEL", "Qwen/Qwen3.5-397B-A17B-FP8"))
    parser.add_argument("--infomaniak-product", default=os.environ.get("INFOMANIAK_PRODUCT_ID"),
                        help="product ID of the AI Tools product (default: the INFOMANIAK_PRODUCT_ID environment variable)")
    parser.add_argument("--list-models", action="store_true", help="infomaniak: print the model names of the product and stop")
    parser.add_argument("--ollama-model", default="qwen3.5:9b")
    parser.add_argument("--ollama-url", default="http://localhost:11434")
    parser.add_argument("--think", action="store_true", help="infomaniak, ollama: let the model think before it answers (slower)")
    parser.add_argument("--tag", help="suffix for the output file names, for example to compare two backends")
    args = parser.parse_args()

    if args.list_models:
        for model in infomaniak_request(args.infomaniak_product, "/models").get("data", []):
            print(model.get("id"))
        return
    if not (args.directory and args.series and args.date):
        parser.error("the capture directory, --series, and --date are necessary")

    transcript_file = args.transcript or args.directory / "transcript-large-v3-turbo.jsonl"
    utterances = [json.loads(line) for line in transcript_file.read_text().splitlines() if line]
    # Correct the spoken words before the model reads them. The quote check then uses the same text.
    spelling, rules = load_corrections(args.corrections)
    for u in utterances:
        for pattern, right in spelling:
            u["text"] = pattern.sub(right, u["text"])
    attendees, chat = load_events(args.directory)
    # The chat messages go into the transcript at their times, so the quote check applies to them also.
    utterances = sorted(utterances + chat, key=lambda u: u["start_s"])
    if not attendees:
        sys.exit("The capture has no participants.")
    glossary = [t.strip() for t in args.glossary.read_text().splitlines()] if args.glossary.exists() else []
    glossary = [t for t in glossary if t and not t.startswith("#")]

    transcript = "\n".join(f"[{u['start_s']:.1f}] {u['speaker']}{' (chat)' if u.get('chat') else ''}: {u['text']}" for u in utterances)
    context = (
        f"<meeting>\nSeries: {args.series}\nDate: {args.date}\n</meeting>\n\n"
        "<attendees>\n" + "\n".join(attendees) + "\n</attendees>\n\n"
        f"<glossary>\n{', '.join(glossary)}\n</glossary>\n\n"
        + ("<corrections>\n" + "\n".join(f"- {r}" for r in rules) + "\n</corrections>\n\n" if rules else "")
        + (f"<agenda>\n{args.agenda.read_text()}\n</agenda>\n\n" if args.agenda else "")
        + (f"<rolling_agenda>\n{args.rolling_agenda.read_text()}\n</rolling_agenda>\n\n" if args.rolling_agenda else "")
        + "The number in brackets at the start of each transcript line is its start time in seconds.\n\n"
        f"<transcript>\n{transcript}\n</transcript>\n\n"
    )

    if args.backend == "claude":
        client = anthropic.Anthropic()

        def ask(content: str, output_format: type[BaseModel]):
            return ask_claude(client, SYSTEM, content, output_format)
    elif args.backend == "infomaniak":
        def ask(content: str, output_format: type[BaseModel]):
            return ask_infomaniak(args.infomaniak_product, args.infomaniak_model, args.think, SYSTEM, content, output_format)
    else:
        def ask(content: str, output_format: type[BaseModel]):
            return ask_ollama(args.ollama_model, args.ollama_url, args.think, SYSTEM, content, output_format)

    suffix = f"-{args.tag}" if args.tag else ""
    started = time.monotonic()

    print("draft the minutes", flush=True)
    draft = ask(context + DRAFT_TASK, make_draft_schema(attendees))

    # Check 1, by program: each quote must be in the transcript, from that speaker, near that time.
    items = (
        [("decision", i, d) for i, d in enumerate(draft.decisions)]
        + [("action_item", i, a) for i, a in enumerate(draft.action_items)]
        + [("statement", i, s) for i, s in enumerate(draft.statements)]
    )
    notes: dict[tuple[str, int], list[str]] = {(kind, i): [] for kind, i, _ in items}
    removed: set[tuple[str, int]] = set()

    for kind, i, item in items:
        found = [e for e in item.evidence if quote_found(e, utterances)]
        if not found:
            removed.add((kind, i))
            notes[kind, i].append("Removed: no quote of its evidence is in the transcript.")
        elif len(found) < len(item.evidence):
            notes[kind, i].append("One or more quotes of its evidence are not in the transcript.")

    # Check 2, by a second model call: does the transcript support each item, and is its kind correct?
    remaining = [(kind, i, item) for kind, i, item in items if (kind, i) not in removed]
    if remaining:
        print("check the draft against the transcript", flush=True)
        listing = json.dumps([{"kind": kind, "index": i, "item": item.model_dump()} for kind, i, item in remaining], indent=1)
        review: Review = ask(f"{context}{REVIEW_TASK}\n<draft_items>\n{listing}\n</draft_items>", Review)
        verdicts = {(v.kind, v.index): v for v in review.verdicts}
        for kind, i, _ in remaining:
            verdict = verdicts.get((kind, i))
            if verdict is None:
                notes[kind, i].append("The check gave no verdict for this item.")
            elif verdict.verdict == "unsupported":
                removed.add((kind, i))
                notes[kind, i].append(f"Removed by the check: {verdict.reason}")
            elif verdict.verdict == "partly":
                notes[kind, i].append(f"Low confidence: {verdict.reason}")

    def kept(kind: str, entries: list) -> list:
        return [(i, e) for i, e in enumerate(entries) if (kind, i) not in removed]

    def mark(kind: str, i: int) -> str:
        return " *(review)*" if notes[kind, i] else ""

    model = {"claude": CLAUDE_MODEL, "infomaniak": args.infomaniak_model, "ollama": args.ollama_model}[args.backend]
    lines = [f"# {args.series}: {args.date}", "",
             "> Crow, an automated notetaker, made these minutes. "
             "They may contain mistakes or inaccuracies and are for reference only.", ">",
             f"> Model: {model}  ", f"> Source code: <{REPO_URL}>", "", "## Attendees", ""]
    lines += [f"- {name}" for name in attendees]
    lines += ["", "## Topics", ""]
    # A link is published only if a participant typed exactly that link into the chat.
    chat_text = " ".join(u["text"] for u in utterances if u.get("chat"))
    for topic in draft.topics:
        lines += [f"### {topic.title}", "", topic.summary, ""]
        links = [link for link in dict.fromkeys(topic.links) if re.fullmatch(r"https?://\S+", link) and link in chat_text]
        if links:
            lines += ["Links from the meeting chat:", ""] + [f"- <{link}>" for link in links] + [""]
    lines += ["## Decisions", ""]
    lines += [f"- {d.text}{mark('decision', i)}" for i, d in kept("decision", draft.decisions)] or ["None recorded."]
    lines += ["", "## Action items", ""]
    lines += [f"- **{a.owner}:** {a.task}{mark('action_item', i)}" for i, a in kept("action_item", draft.action_items)] or ["None recorded."]
    statements = kept("statement", draft.statements)
    if statements:
        lines += ["", "## Proposals and objections", ""]
        lines += [f"- **{s.speaker}** ({s.kind}): {s.text}{mark('statement', i)}" for i, s in statements]
    if any(json.loads(line).get("type") == "kicked" for line in (args.directory / "events.jsonl").read_text().splitlines() if line):
        lines += ["", "---", "", "A moderator removed the notetaker from the meeting before the end. "
                  "These minutes contain only the part of the meeting before that time."]
    lines.append("")
    (args.directory / f"minutes{suffix}.md").write_text("\n".join(lines))

    review_lines = ["# Review notes", "", "Items marked *(review)* in the minutes must be checked and the mark removed.", ""]
    flagged = [(kind, i, item) for kind, i, item in items if notes[kind, i]]
    for kind, i, item in flagged:
        text = getattr(item, "text", None) or getattr(item, "task", "")
        review_lines += [f"- **{kind.replace('_', ' ')}:** {text}"] + [f"  - {note}" for note in notes[kind, i]]
    if not flagged:
        review_lines.append("No item has a note.")
    (args.directory / f"minutes-review{suffix}.md").write_text("\n".join(review_lines) + "\n")

    (args.directory / f"minutes-evidence{suffix}.json").write_text(json.dumps({
        "draft": draft.model_dump(),
        "removed": [list(key) for key in sorted(removed)],
        "notes": [{"kind": kind, "index": i, "notes": n} for (kind, i), n in notes.items() if n],
    }, indent=2) + "\n")

    print(f"{len(draft.topics)} topics, {len(kept('decision', draft.decisions))} decisions, "
          f"{len(kept('action_item', draft.action_items))} action items, {len(statements)} statements; "
          f"{len(removed)} items removed, {len(flagged) - len(removed)} items marked for review; "
          f"{time.monotonic() - started:.0f} s")
    print(f"output: {args.directory / f'minutes{suffix}.md'}")


if __name__ == "__main__":
    main()
