# Crow, the notetaker bot

This directory contains the source code of the proof of concept. The bot joins a Jitsi meeting as a guest and records one audio file for each participant.

The speaker label of each file comes from the owner of the audio track. The bot does not analyze voices.

## Requirements

- Node.js 20 or later
- Chromium at `/usr/bin/chromium`, or set the `CHROMIUM_PATH` environment variable
- `ffmpeg`, for the report and the self test

Install the dependencies:

```
npm install
```

## Record a meeting

1. Make sure that a person with an account opens the room. On `meet.jit.si`, the bot waits until a moderator arrives.
2. Start the bot:

   ```
   node capture.js --url https://meet.jit.si/FreeCAD-devs-meeting --out out/test1
   ```

3. To stop the bot, press Ctrl+C. The bot also stops 1 minute after the last person leaves. Other notetaker bots do not count as persons.
4. Print the report:

   ```
   node report.js out/test1
   ```

Run `node capture.js --help` for the options.

The bot shows the image `bot/avatar.png` as its avatar. Use `--avatar <url>` or the `CROW_AVATAR_URL` environment variable for a different image. The address must be public, because each participant loads the image from it. A Jitsi host that sets `disableThirdPartyRequests` shows the initials of the bot and not the image.

## Output

| File | Content |
|---|---|
| `NNN-<participantId>.webm` | Opus audio of one participant. A new file starts if the participant connects again or if the track owner changes. |
| `events.jsonl` | One line for each event: participant joined or left, name changed, muted, unmuted, segment start and end, chat message, kick. |
| `manifest.json` | The list of segments with the participant ID, the display name, and the start and end offsets. |
| `not-joined.png` | A screen capture, written only when the bot did not get into the conference. |

- All offsets (`t`, `start_s`, `end_s`) are seconds from the capture start. `captureStart` in the manifest gives the clock time.
- A muted participant becomes silence in the file. Thus the time in the file agrees with the offsets.
- The bot records the messages of the meeting chat, with the sender and the time. It does not record private messages.
- If a moderator removes the bot, the capture stops and the bot does not join again. The minutes contain the part before that time.
- The manifest gives the last display name that the participant used in the segment. `events.jsonl` has each name change.

## Check the result of a real meeting

1. Run `node report.js <directory>`.
2. Make sure that each participant who spoke has a file with the correct name.
3. Make sure that `expect_s` and `actual_s` agree for each file.
4. Listen to each file. Make sure that it contains only the voice of the participant in its label.

## Transcribe a capture

The transcription uses a local Whisper model (`faster-whisper`). No audio leaves the computer. The first run downloads the model.

```
uv run transcribe.py out/test1
```

- `uv` installs Python 3.12 or 3.13 and the dependencies automatically.
- The default model is `large-v3-turbo` on the CPU. Use `--model large-v3` for the larger model.
- The script reads the terms in `bot/glossary.txt` and gives them to the model as preferred words.
- The speaker of each utterance comes from the audio file, not from the voice.

Output in the capture directory:

| File | Content |
|---|---|
| `transcript-<model>.jsonl` | One line for each utterance: start, end, participant ID, speaker, text. A pause of 1 second starts a new utterance. |
| `transcript-<model>.md` | The transcript for a person to read. Consecutive utterances of one speaker are joined. |

## Make the minutes

The minutes step uses a hosted Qwen model at Infomaniak AI Tools. The text transcript goes to the Infomaniak API. The audio stays on the computer.

1. Set the API key and the product ID in the shell. Do not write the key into a file of the repository.

   ```
   read -rs INFOMANIAK_API_KEY && export INFOMANIAK_API_KEY
   export INFOMANIAK_PRODUCT_ID=<product ID>
   ```

2. Make the minutes:

   ```
   uv run minutes.py out/test1 --series "CAM Meetup" --date 2026-10-06
   ```

3. To use a different model, print the model names with `uv run minutes.py --list-models`. Then add `--infomaniak-model <model name>`.

4. If the meeting has an agenda, add `--agenda <path to agenda.md>`.
5. If the series has one agenda for all meetings, add `--rolling-agenda <path to agenda.md>`.

Other options:

- The default model is `Qwen/Qwen3.5-397B-A17B-FP8`. The `INFOMANIAK_MODEL` environment variable changes the default.
- `--infomaniak-product <ID>` selects the AI Tools product, as an alternative to the environment variable.
- `--backend ollama` uses a local model through Ollama (`qwen3.5:9b`). Then no data leaves the computer. Start Ollama first with `ollama serve &`.
- `--ollama-model <name>` selects a different local model.
- `--backend claude` uses the Claude API (`claude-opus-5-5`). The `ANTHROPIC_API_KEY` environment variable must be set. This backend is not tested with a real API call.
- `--think` lets the Qwen model think before it answers.
- `--tag <text>` adds a suffix to the output file names, so that the results of two runs can be compared.

To make the report, the transcript, and the minutes with one command:

```
./process.sh out/test1 "CAM Meetup" 2026-10-06
```

`process.sh` uses the Infomaniak backend. Set `BACKEND=ollama` before the command to use the local model.

Output in the capture directory:

| File | Content |
|---|---|
| `minutes.md` | The public minutes: attendees, topics, decisions, action items, proposals and objections. No quotes and no time stamps. |
| `minutes-review.md` | Notes for the reviewer: the items with low confidence and the items that the checks removed. |
| `minutes-evidence.json` | Private. The transcript quotes that support each item. |

The script makes two checks on each decision, action item, proposal, and objection:

- A program looks for each evidence quote in the transcript, from the same speaker, near the same time. An item with no quote in the transcript is removed.
- A second model call compares each item with the transcript. An item with no support, with the wrong person, or with the wrong type is removed. An item with partial support gets the mark *(review)*.

The chat messages are in the transcript that the model reads, with the mark "(chat)". The model can use a link or a comment from the chat in the minutes.

With a rolling agenda, the model finds the agenda items that the meeting discussed. It does not assume that the meeting used the agenda from top to bottom.

The model can select names only from the attendee list.

The attendee list comes from the capture events, not from the model.

### The prompts

The prompts are constants near the top of `minutes.py`:

| Constant | Use |
|---|---|
| `SYSTEM` | The system prompt of the two calls. It describes the meeting, the transcript, and the four kinds of items. |
| `DRAFT_TASK` | The task of the first call. The model writes the draft minutes with evidence quotes. |
| `REVIEW_TASK` | The task of the second call. The model checks each draft item against the transcript. |

The script adds the meeting data before each task: the series, the date, the attendees, the glossary, the agenda, and the transcript. The JSON schemas `make_draft_schema` and `Review` set the structure of each answer.

To change the prompts:

1. Edit the text of the constant in `minutes.py`.
2. Run the script on a capture that you know, with a tag. For example, `--tag new`.
3. Compare `minutes-new.md` and `minutes-review-new.md` with the files of an earlier run.
4. Put the changes of the prompt in a pull request, so that a maintainer can review them.

All backends use the same prompts.

### Correct a mistake that repeats

If the minutes make the same mistake again and again, add a line to `bot/corrections.txt`. You do not have to edit the prompts. There are two kinds of lines:

- A spelling correction, for example `Yorick -> Yorik`. The script replaces the wrong word in the spoken transcript before the model reads it. The match ignores case and finds only full words. The model also gets the instruction "Write Yorik, not Yorick".
- A rule, for example `Write "CAM" for the workbench, not "Path".` All lines without `->` are rules. The model gets each rule as an instruction.

Use a spelling correction only for a word that is always wrong. Use a rule for a word that is correct in some sentences, for example "Path".

Speech-to-text can also make the mistake. If a name or a term is often wrong in the transcript, add the correct form to `bot/glossary.txt` also.

Use `--corrections <file>` to use a different file.

## Operate the scheduler

The scheduler reads the public calendar and starts the bot for each meeting. It needs the API key, the product ID, and the GitHub App credentials (see "The GitHub App of the bot"). Without the app credentials, it uses the `gh` login.

```
systemd-inhibit --what=sleep:idle uv run scheduler.py
```

- `uv run scheduler.py --dry-run` prints the meetings of the next 7 days and the decision for each.
- `bot/series.json` contains the calendar address, the permitted Jitsi hosts, and the series list. An entry with `"deny": true` is not recorded.
- Two minutes before a meeting, the scheduler starts `run-meeting.sh`. That script records the meeting, makes the minutes, and opens the pull request.
- The output of a meeting is in `out/<series directory>-<date>/`, with the log `run.log`.
- The scheduler starts each meeting only once.

`run-meeting.sh` reads the agenda from the repository after the meeting:

1. `meetings/<series directory>/<date>/agenda.md` is the agenda of that meeting.
2. If that file is not there, `meetings/<series directory>/agenda.md` is the rolling agenda of the series.

## The GitHub App of the bot

The bot opens the pull requests as the GitHub App "crow-notetaker" of the FreeCAD organization. The pull requests then show `crow-notetaker[bot]` as the author, not a person.

The app has these repository permissions:

- Contents: read and write
- Issues: read and write (for the labels)
- Pull requests: read and write

The app is installed only on `FreeCAD/Meetings`.

To give the bot computer access to the app:

1. Move the private key out of the download directory, and make it private:

   ```
   mkdir -p ~/.config/crow
   mv ~/Downloads/crow-notetaker.*.private-key.pem ~/.config/crow/app-key.pem
   chmod 600 ~/.config/crow/app-key.pem
   ```

2. Set the App ID and the path to the key in the shell that starts the scheduler. The App ID is on the settings page of the app.

   ```
   export CROW_APP_ID=<App ID>
   export CROW_APP_KEY=~/.config/crow/app-key.pem
   ```

3. Make sure that the app gives a token:

   ```
   GH_TOKEN=$(uv run github_app.py) gh api repos/FreeCAD/Meetings --jq .full_name
   ```

`github_app.py` makes a token that expires after 1 hour. `publish.py` and `run-meeting.sh` get a new token each time. Without `CROW_APP_ID`, the scripts use the `gh` login of the person.

Do not put the private key in the repository. If the key is lost or stolen, delete it on the settings page of the app and make a new key.

## Open the pull request

The pull request step uses the GitHub CLI (`gh`). It operates as the GitHub App of the bot if `CROW_APP_ID` is set, and with the `gh` login if not. It sends only `minutes.md` and the review notes.

1. Read `minutes.md` and `minutes-review.md` in the capture directory.
2. Show the pull request and send nothing:

   ```
   uv run publish.py out/test1 --series "CAM Meetup" --series-dir cam --date 2026-10-06 --dry-run
   ```

3. Open the pull request:

   ```
   uv run publish.py out/test1 --series "CAM Meetup" --series-dir cam --date 2026-10-06
   ```

- The pull request adds `meetings/<series directory>/<date>/minutes.md` to `FreeCAD/Meetings`. Use `--repo` for a different repository.
- The branch name is `minutes/<series directory>/<date>`.
- The pull request text contains the review procedure and the review notes.
- A second run for the same meeting updates the file on the branch. It does not open a second pull request.
- The script stops if the minutes of that meeting are already on the default branch.
- The pull request gets the label `minutes`. The script makes the labels `minutes` and `hold` if they do not exist.

### Automatic merge

The workflow `.github/workflows/merge-minutes.yml` runs one time each day. It merges a pull request with the label `minutes` when all these conditions are true:

- The pull request opened 7 days ago or more. `REVIEW_DAYS` in the workflow sets the period. Also change `REVIEW_DAYS` in `publish.py`, because the pull request text gives the period.
- The pull request is not a draft, and it does not have the label `hold`.
- No reviewer requested changes.
- `minutes.md` has no *(review)* mark.

For a *(review)* mark or a failed merge, the workflow writes one comment on the pull request.

To see the result without a merge, start the workflow by hand in the Actions tab of the repository. The option "dry-run" is on by default.

The workflow needs write access. In the repository settings, set Actions > General > Workflow permissions to "Read and write permissions". If the default branch gets a rule that requires approving reviews, the workflow cannot merge.

## Self test

The self test starts two fake speakers, "Chris" (440 Hz tone) and "Kris" (880 Hz tone), and the capture bot. It passes when each file contains only the tone of the speaker in its label.

```
node selftest.js --url https://<jitsi host>/<room name>
```

The room must open without a login, so `meet.jit.si` is not applicable. Use a Jitsi host that permits guests to open rooms.

## Files

| File | Function |
|---|---|
| `capture.js` | The capture bot. |
| `page-recorder.js` | The code that operates in the Jitsi Meet page and records the tracks. |
| `join.js` | Starts Chromium, opens the room, and waits until the bot is in the conference. |
| `report.js` | Prints the table of segments with the measured duration and level. |
| `manifest.js` | Makes the segment list from the capture events. |
| `transcribe.py` | Transcribes a capture directory with a local model and merges the speakers by time. |
| `github_app.py` | Prints an access token of the GitHub App of the bot. |
| `minutes.py` | Makes the minutes from a transcript with a hosted or a local model, and checks each item against the transcript. |
| `publish.py` | Opens the pull request that adds the minutes of one meeting to the repository. |
| `scheduler.py` | Reads the calendar and starts the bot for each meeting. |
| `run-meeting.sh` | Runs one meeting: capture, transcript, minutes, pull request. |
| `process.sh` | Runs the report, the transcription, and the minutes for one capture directory. |
| `speak.js` | Test helper. Joins a meeting and plays a WAV file as the microphone. |
| `selftest.js` | The self test. |

## Limits

- The bot uses `APP.conference._room`, an internal object of the Jitsi Meet page. A Jitsi Meet update can break it.
- Two persons who share one microphone are one speaker.
- The bot does not answer a lobby. A moderator must admit it.
