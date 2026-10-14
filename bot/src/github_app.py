#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10,<3.14"
# dependencies = ["pyjwt[crypto]>=2.8"]
# ///
"""Print an access token of the GitHub App of the bot, for one repository.

With this token, the GitHub CLI operates as the app, and the pull requests come from the app,
not from a person. The token expires after 1 hour.

    export CROW_APP_ID=<App ID>
    export CROW_APP_KEY=<path to the private key .pem file>
    GH_TOKEN=$(uv run github_app.py) gh api repos/FreeCAD/Meetings

The app must be installed on the repository.
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

import jwt

API = "https://api.github.com"


def github(method: str, path: str, token: str, scheme: str = "Bearer", body: dict | None = None) -> dict:
    request = urllib.request.Request(
        API + path, method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": f"{scheme} {token}", "Accept": "application/vnd.github+json",
                 "X-GitHub-Api-Version": "2022-11-28"},
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.load(response)
    except urllib.error.HTTPError as e:
        sys.exit(f"GitHub error {e.code} ({method} {path}): {e.read().decode(errors='replace')[:500]}")
    except urllib.error.URLError as e:
        sys.exit(f"No connection to GitHub: {e.reason}")


def app_token(app_id: str, key_file: Path, repo: str) -> str:
    """An installation access token of the app, limited to the repository."""
    try:
        key = key_file.read_text()
    except OSError as e:
        sys.exit(f"Cannot read the private key {key_file}: {e.strerror}")
    now = int(time.time())
    # GitHub permits a JWT of 10 minutes or less. The start is 60 seconds early for clock drift.
    app_jwt = jwt.encode({"iat": now - 60, "exp": now + 540, "iss": app_id}, key, algorithm="RS256")
    installation = github("GET", f"/repos/{repo}/installation", app_jwt)
    answer = github("POST", f"/app/installations/{installation['id']}/access_tokens", app_jwt,
                    body={"repositories": [repo.split("/", 1)[1]]})
    return answer["token"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo", default=os.environ.get("MEETINGS_REPO", "FreeCAD/Meetings"))
    args = parser.parse_args()
    app_id, key_file = os.environ.get("CROW_APP_ID"), os.environ.get("CROW_APP_KEY")
    if not (app_id and key_file):
        sys.exit("Set the CROW_APP_ID and CROW_APP_KEY environment variables.")
    print(app_token(app_id, Path(key_file).expanduser(), args.repo))


if __name__ == "__main__":
    main()
