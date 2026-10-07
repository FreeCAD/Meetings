#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10,<3.14"
# dependencies = ["faster-whisper>=1.1", "numpy"]
# ///
"""Transcribe a capture directory with a local Whisper model.

Each participant has a separate audio file, so the speaker of each utterance comes from the
file. The script transcribes each file, moves the times to the capture time line, and merges
the utterances by time.

    uv run transcribe.py out/test1 --model large-v3-turbo
"""
import argparse
import json
import os
import subprocess
import time
from pathlib import Path

import numpy as np
from faster_whisper import WhisperModel

HERE = Path(__file__).resolve().parent


def load_segments(directory: Path) -> list[dict]:
    manifest = directory / "manifest.json"
    if manifest.exists():
        return json.loads(manifest.read_text())["segments"]

    # The capture did not stop cleanly. Read the segment starts from the events.
    events = [json.loads(line) for line in (directory / "events.jsonl").read_text().splitlines() if line]
    return [
        {"file": e["file"], "participantId": e["participantId"], "name": e["name"], "start_s": e["t"]}
        for e in events
        if e["type"] == "segment_start"
    ]


def decode(path: Path) -> np.ndarray:
    """Decode a file to 16 kHz mono samples with ffmpeg."""
    pcm = subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(path), "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
        check=True, capture_output=True,
    ).stdout
    return np.frombuffer(pcm, dtype=np.int16).astype(np.float32) / 32768.0


def load_glossary(path: Path | None) -> str | None:
    if not path or not path.exists():
        return None
    terms = [line.strip() for line in path.read_text().splitlines()]
    return ", ".join(t for t in terms if t and not t.startswith("#")) or None


def clock(seconds: float) -> str:
    seconds = int(seconds)
    return f"{seconds // 3600:d}:{seconds % 3600 // 60:02d}:{seconds % 60:02d}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("directory", type=Path, help="capture directory")
    parser.add_argument("--model", default="large-v3-turbo", help="faster-whisper model name (default: large-v3-turbo)")
    parser.add_argument("--device", default="cpu", help="cpu or cuda (default: cpu)")
    parser.add_argument("--compute-type", default="int8", help="CTranslate2 compute type (default: int8)")
    parser.add_argument("--language", default="en")
    parser.add_argument("--glossary", type=Path, default=HERE.parent / "glossary.txt")
    parser.add_argument("--split-gap", type=float, default=1.0, help="start a new utterance after a pause of this length (seconds)")
    parser.add_argument("--merge-gap", type=float, default=5.0,
                        help="in the markdown file, join utterances of one speaker with a smaller gap (seconds)")
    args = parser.parse_args()

    segments = load_segments(args.directory)
    hotwords = load_glossary(args.glossary)
    model = WhisperModel(args.model, device=args.device, compute_type=args.compute_type, cpu_threads=os.cpu_count() or 4)

    utterances = []
    meeting_s = 0.0
    started = time.monotonic()

    for seg in segments:
        speaker = seg["name"] or seg["participantId"]
        offset = seg["start_s"]
        print(f"transcribe {seg['file']} ({speaker})", flush=True)
        # The voice activity filter removes silence, where Whisper can invent text.
        # Each window is independent, so one error does not continue into the next window.
        parts, info = model.transcribe(
            decode(args.directory / seg["file"]),
            language=args.language,
            vad_filter=True,
            vad_parameters={"min_silence_duration_ms": 500},
            condition_on_previous_text=False,
            word_timestamps=True,
            hotwords=hotwords,
        )
        meeting_s = max(meeting_s, offset + info.duration)

        # A Whisper segment can contain speech from before and after a long pause. Split the
        # words at each pause, so that a short answer gets its correct time.
        current = None
        for part in parts:
            for word in part.words or []:
                start, end = offset + word.start, offset + word.end
                if current is None or start - current["end_s"] >= args.split_gap:
                    current = {"start_s": start, "end_s": end, "participantId": seg["participantId"],
                               "speaker": speaker, "text": ""}
                    utterances.append(current)
                current["end_s"] = end
                current["text"] += word.word

    elapsed = time.monotonic() - started
    for u in utterances:
        u["start_s"], u["end_s"], u["text"] = round(u["start_s"], 2), round(u["end_s"], 2), u["text"].strip()
    utterances.sort(key=lambda u: u["start_s"])

    # For the markdown file, join consecutive utterances of one speaker.
    merged: list[dict] = []
    for u in utterances:
        last = merged[-1] if merged else None
        if last and last["participantId"] == u["participantId"] and u["start_s"] - last["end_s"] < args.merge_gap:
            last["end_s"] = u["end_s"]
            last["text"] += " " + u["text"]
        else:
            merged.append(dict(u))

    tag = args.model.replace("/", "_")
    (args.directory / f"transcript-{tag}.jsonl").write_text("".join(json.dumps(u) + "\n" for u in utterances))
    (args.directory / f"transcript-{tag}.md").write_text(
        "".join(f"[{clock(u['start_s'])}] **{u['speaker']}:** {u['text']}\n\n" for u in merged)
    )
    print(f"model {args.model}: meeting of {meeting_s:.0f} s transcribed in {elapsed:.0f} s "
          f"({elapsed / meeting_s:.2f} x the meeting duration), "
          f"{len(utterances)} utterances, {sum(len(u['text'].split()) for u in utterances)} words")
    print(f"output: {args.directory / f'transcript-{tag}.md'}")


if __name__ == "__main__":
    main()
