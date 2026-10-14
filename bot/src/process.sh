#!/usr/bin/env bash
# Make the transcript and the minutes of one capture directory.
#
#   ./process.sh out/test1 "CAM Meetup" 2026-10-06 [options for minutes.py]
#
# For example: --agenda <file> for the agenda of the meeting, or --rolling-agenda <file>.
#
# Set BACKEND=ollama to make the minutes with the local model. The default is infomaniak.
set -euo pipefail

if [ $# -lt 3 ]; then
    echo "Usage: $0 <capture directory> <series name> <date YYYY-MM-DD> [options for minutes.py]"
    exit 2
fi

here=$(cd "$(dirname "$0")" && pwd)
dir=$1
series=$2
date=$3

backend=${BACKEND:-infomaniak}

if [ "$backend" = infomaniak ] && [ -z "${INFOMANIAK_API_KEY:-}" ]; then
    echo "No API key. Set the INFOMANIAK_API_KEY environment variable."
    exit 1
fi
if [ "$backend" = ollama ] && ! curl -s -m 3 -o /dev/null http://localhost:11434/api/version; then
    echo "Ollama does not answer. Start it with: ollama serve"
    exit 1
fi

node "$here/report.js" "$dir"
uv run "$here/transcribe.py" "$dir"
uv run "$here/minutes.py" "$dir" --series "$series" --date "$date" --backend "$backend" "${@:4}"
