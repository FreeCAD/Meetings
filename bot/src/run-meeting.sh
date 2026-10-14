#!/usr/bin/env bash
# Record one meeting, make the minutes, and open the pull request, with no operator action.
# The scheduler starts this script. The bot joins immediately.
#
#   ./run-meeting.sh <jitsi room url> <series name> <series directory> <date YYYY-MM-DD> [maximum minutes]
set -euo pipefail

if [ $# -lt 4 ]; then
    echo "Usage: $0 <jitsi room url> <series name> <series directory> <date YYYY-MM-DD> [maximum minutes]"
    exit 2
fi

here=$(cd "$(dirname "$0")" && pwd)
url=$1
series=$2
series_dir=$3
day=$4
max_minutes=${5:-120}
out="$here/out/$series_dir-$day"
repo=${MEETINGS_REPO:-FreeCAD/Meetings}

mkdir -p "$out"
{
    node "$here/capture.js" --url "$url" --out "$out" --wait-minutes 30 --max-minutes "$max_minutes"
    # With the GitHub App of the bot, gh uses a token of the app. publish.py gets its own token.
    if [ -n "${CROW_APP_ID:-}" ]; then
        GH_TOKEN=$(uv run "$here/github_app.py" --repo "$repo")
        export GH_TOKEN
    fi
    # Read the agenda from the repository after the meeting, because persons can change it in the meeting.
    # The agenda of the meeting date has priority. The agenda of the series is a rolling agenda.
    agenda=()
    if gh api -H "Accept: application/vnd.github.raw" "repos/$repo/contents/meetings/$series_dir/$day/agenda.md" > "$out/agenda.md" 2> /dev/null; then
        agenda=(--agenda "$out/agenda.md")
        echo "agenda: meetings/$series_dir/$day/agenda.md"
    elif gh api -H "Accept: application/vnd.github.raw" "repos/$repo/contents/meetings/$series_dir/agenda.md" > "$out/agenda.md" 2> /dev/null; then
        agenda=(--rolling-agenda "$out/agenda.md")
        echo "agenda: meetings/$series_dir/agenda.md (rolling agenda)"
    else
        rm -f "$out/agenda.md"
        echo "agenda: none"
    fi
    BACKEND=infomaniak "$here/process.sh" "$out" "$series" "$day" "${agenda[@]}"
    uv run "$here/publish.py" "$out" --series "$series" --series-dir "$series_dir" --date "$day" --repo "$repo"
} 2>&1 | tee "$out/run.log"
