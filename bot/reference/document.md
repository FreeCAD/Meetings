# FreeCAD Meeting Notetaker: Plan

Status: research complete, design recommended, capture test built, passed with fake speakers, and recorded one real meeting. The speech-to-text comparison is the next step. Last update: 2026-10-06.

## 1. Purpose

The FreeCAD community has many public meetings. This project builds an automated agent that does these tasks:

1. Read the public community calendar.
2. Join each public meeting that has a meeting link.
3. Make minutes of the meeting.
4. Send the minutes to one GitHub repository as a pull request.

The primary quality target is correct speaker attribution. Earlier tools confused speakers, for example Chris and Kris.

## 2. Current state

### 2.1 Calendar

- The page `https://www.freecad.org/events.php` shows the calendar in an Open Web Calendar iframe.
- The source is a public Nextcloud calendar on `cloud.freecad.org`. It is Nextcloud, not OpenCloud.
- Public ICS link: `https://cloud.freecad.org/remote.php/dav/public-calendars/ZtJiizXtSqBaacwo?export`
- The ICS file has 142 events and no authentication. Its refresh interval is 4 hours.
- Meeting series are split and edited frequently. The file has many `UNTIL` rules, `RECURRENCE-ID` overrides, and `STATUS:CANCELLED` entries.

### 2.2 Active meeting series

All active series use the public `meet.jit.si` host. The link is in the `LOCATION` and `DESCRIPTION` fields.

| Series | Recurrence | Local start | Minutes | Room |
|---|---|---|---|---|
| PR & Issues Review | Weekly, Monday | 17:30 Europe/Brussels | 60 | `FreeCADMergeMeeting` |
| OCCT Dev Meeting | Weekly, Sunday | 14:30 UTC | 60 | `FreeCAD-devs-meeting` |
| Developers meeting | Monthly, first Sunday | 17:30 Europe/Brussels | 90 | `FreeCAD-devs-meeting` |
| Developers meeting (second series) | Monthly, third Saturday | 17:30 Europe/Brussels | 60 | `FreeCAD-devs-meeting` |
| Addon Developer Meetup | Each 2 weeks, Tuesday | 10:00 America/New_York | 60 | `FreeCAD-devs-meeting` |
| CAM Meetup | Weekly, Friday | 17:30 Europe/Amsterdam | 60 | `FreeCADCAMMeetup` |
| FPA Meetup | Weekly, Thursday | 09:00 America/Chicago | 60 | `FPAadmins` |
| DWG Meetup | Weekly, Wednesday | 17:30 Europe/Berlin | 60 | `FreeCAD-devs-meeting` |
| BIM Meetup | Weekly, Tuesday | 18:00 Europe/Berlin | 60 | `FreeCAD-devs-meeting` |

Important facts:

- Five series share the room `FreeCAD-devs-meeting`. The room name does not identify the meeting. The calendar event must identify it.
- In summer, the OCCT Dev Meeting ends at the time that the first-Sunday Developers meeting starts, in the same room.
- The total is approximately 31 meeting hours each month.
- In 2026, some series moved to Bigger Blue Button and Brave Talk, then moved back to `meet.jit.si` in September.
- Since August 2023, `meet.jit.si` requires that a person with a Google, GitHub, or Facebook account opens each room. Guests then join without an account.

### 2.3 Agendas and minutes today

| Series | Agenda | Minutes |
|---|---|---|
| Developers meeting | `FreeCAD/FreeCAD-developer-meetings`, `Agendas/agenda-YYYY-MM-DD.md` | Same repository, `Minutes/minutes-YYYY-MM-DD.md` |
| FPA Meetup | Nextcloud file "FPA Admin Agenda.md" | `FreeCAD/FPA`, `minutes/YYYY-MM-DD-admin.md` |
| CAM Meetup | Google Doc | None found |
| BIM Meetup | Nextcloud file "BIM-meetups-agenda.md" | None found |
| PR & Issues Review | GitHub project board 40 | None found |
| OCCT Dev Meeting | GitHub project board 32 and Discord | None found |
| DWG Meetup, Addon Developer Meetup | None found | None found |

- The FPA admins make the minutes with screenapp.io. A person uploads the output manually.
- The FPA paid 147.75 EUR for the screenapp.io renewal in October 2025 (FPA issue 246).
- Minutes were absent for one month in 2026 because records were missed after a platform change (FPA issue 469).
- The project refused a request to publish meeting records. Only minutes are public (developer-meetings issue 40).
- No written record policy was found.
- The forum was not searched, because it returned a bot check page.

### 2.4 Tools tried

- fireflies.ai joins Jitsi from a calendar link. Its minutes had low quality, because it did not identify speakers reliably.
- screenapp.io has no bot for Jitsi. A person must make and upload a record.

## 3. Requirements

These decisions came from the interview on 2026-10-06.

| Topic | Decision |
|---|---|
| Product | Publish minutes only. Do not publish the transcript or the audio. |
| Publication | The agent opens one pull request for each meeting. A person merges it. |
| Reviewer | Any maintainer with write access can merge. |
| Attribution | Give names for decisions, action items, and important proposals or objections. Summarize other discussion without names. |
| Identity | Use the Jitsi display name as the participant typed it. Do not use voice enrollment. |
| Notice | The bot name and the calendar event text give the notice. No stop command is necessary. |
| Retention | Delete the audio after transcription. Keep the private transcript for 30 days, then delete it. |
| Policy status | The FPA approved the notice and the retention policy for the proof of concept. Formal adoption occurs after the proof of concept test. |
| Repository | A new repository, `Meetings`, in the FreeCAD organization on GitHub. Agendas and minutes of all series move to it. |
| Scope | Join all series that have a meeting link. A deny list in the repository excludes series. |
| Deny list | The deny list contains only the PR & Issues Review series at this time. |
| Platform | Jitsi only. The agent skips and reports events that have other links. |
| Agenda | Use the agenda when one is available. Many meetings will have none. |
| Owner | The FPA owns the infrastructure, the accounts, and the cost. |
| Speech-to-text | Use a local model. No audio goes to a vendor. |

## 4. Options investigated

Marks: [V] verified in a primary source, [S] secondary source only, [U] unverified.

### 4.1 Key result: Jitsi gives one audio track for each participant

- Jitsi sends each participant's audio as a separate track, with a participant ID and a display name. [V]
- A bot that records each track knows the speaker exactly. No acoustic speaker separation is necessary.
- Chris and Kris have different participant IDs. Thus the acoustic confusion cannot occur.
- This result was confirmed in the library documentation and in a public bot project. No live test was done.
- Limit: two persons who share one microphone stay as one speaker.

In comparison, speaker separation on one mixed record has an error rate of 13% to 20% for meetings of this size. This is the probable cause of the fireflies.ai problem.

### 4.2 Capture options

| Option | Jitsi support | Exact attribution | Applies to `meet.jit.si` | Notes |
|---|---|---|---|---|
| Custom headless Chromium bot | Yes | Yes | Yes | Joins as a guest and records each remote audio track. The project owns the code. |
| Vexa (Apache-2.0) | Partial | Not guaranteed | Yes | Its Jitsi path has no live validation. It leaves 4% to 7% of rows without a speaker in crosstalk. |
| Jitsi multitrack recorder / `opus-transcriber-proxy` | Yes | Yes | No | Needs control of the Jitsi videobridge, thus a self-hosted Jitsi. |
| Jigasi transcription | Yes | Yes | No | Self-hosted only. Jitsi declared it deprecated in July 2026. |
| Jibri | Yes | No | No | Records only the mixed output. |
| Attendee, MeetingBaaS, Recall.ai | No | - | - | No Jitsi support. |
| Otter, tl;dv, Fathom, Read.ai | No [S] | - | - | No Jitsi support found. |
| fireflies.ai | Yes | No | Yes | Tried. Attribution is not reliable. |
| Meetily, Hyprnote | No bot | No | - | They capture device audio on a person's computer. |

The project `korjavin/jitsi-recorder` shows the custom bot method. It uses Puppeteer and writes one WebM file for each participant. It has no license file, so the project can use it only as a reference.

### 4.3 Speech-to-text options

| Option | Cost for each audio hour | Custom vocabulary | Notes |
|---|---|---|---|
| AssemblyAI Universal-3.5 Pro | 0.21 USD, plus 0.05 USD for keyterms | Yes | 50 USD free credit. Bills each channel. |
| Deepgram Nova-3 | approximately 0.46 USD [S] | Yes, 100 keyterms | 200 USD free credit. |
| ElevenLabs Scribe v2 | 0.27 USD [S] | [U] | |
| OpenAI `gpt-4o-transcribe-diarize` | approximately 0.36 USD | No | Accepts no prompt. |
| faster-whisper large-v3, self-hosted | Hardware only | Yes, by prompt [U] | Needs 4 GB to 6 GB of GPU memory. |
| NVIDIA Parakeet-TDT v3, self-hosted | Hardware only | [U] | Better benchmark accuracy and speed than Whisper large-v3. |

- Benchmark accuracy is for clean audio. Expect more errors for non-native speakers and technical words. [U]
- Whisper models can invent text on silent audio. Apply voice activity detection to each track before transcription.

### 4.4 Options rejected

- **Voice enrollment.** A voice sample that identifies a person is biometric data under GDPR Article 9. It needs explicit consent. Separate tracks make it unnecessary.
- **Speaker separation on mixed audio.** The error rate is too high for attributed decisions.
- **A general bot platform for all meeting platforms.** The requirement is Jitsi only.

## 5. Recommended design

### 5.1 Recommendation

- Build a small custom bot that records one audio track for each participant on `meet.jit.si`.
- Operate the bot on one small FPA virtual server.
- Use a local speech-to-text model (`faster-whisper`) on the CPU. This is a user decision of 2026-10-06, so that no audio goes to a vendor.
- Use a hosted Qwen model at Infomaniak AI Tools for the minutes (model `Qwen/Qwen3.5-397B-A17B-FP8`). This is a user decision of 2026-10-07. Only the text transcript goes to Infomaniak. The local model (`qwen3.5:9b` through Ollama) and the Claude API stay as alternative backends.
- Prove the capture method on one real meeting before other work starts.

Reasons:

- The custom bot is the only option that gives exact attribution on `meet.jit.si` today.
- The local model transcribed a test meeting on a 16-thread CPU in 0.73 of the meeting duration. No GPU is necessary for 31 hours each month.
- The same bot continues to operate if the project moves to a self-hosted Jitsi later.

Vexa is the fallback if the custom bot fails in the test.

### 5.2 Sequence for one meeting

1. The scheduler reads the ICS file each hour and expands the recurrence rules, overrides, and cancellations.
2. The scheduler ignores events that are on the deny list or that have no Jitsi link. It reports events with links to other platforms.
3. At the start time, the bot joins the room as a guest in headless Chromium.
4. The name of the bot is Crow. Its display name in a meeting is "Crow - AI Notetaker", which states its function.
5. The bot waits if no person opened the room. It stops after a set time and reports that no meeting occurred.
6. The bot records one audio file for each participant, with the participant ID, the display name, and the time offset.
7. The bot leaves when it is alone for 5 minutes, or when the maximum duration is reached.
8. The pipeline applies voice activity detection to each track and sends the speech segments to speech-to-text with the glossary.
9. The pipeline merges the segments by time into one transcript with speaker labels, then deletes the audio.
10. The LLM makes the minutes from the transcript, the attendee list, the glossary, and the agenda, if one is available.
11. A second LLM pass checks each decision and each action item against the transcript. It removes or marks items that have no support.
12. The agent opens a pull request that adds `meetings/<series_name>/<YYYY-MM-DD>/minutes.md`. The pull request text lists the items with low confidence.
13. A maintainer corrects and merges the pull request.
14. A scheduled task deletes the private transcript 30 days after the meeting.

### 5.3 Rules for correct attribution

- The speaker label always comes from the track, never from the content of the speech.
- The LLM must copy display names exactly as they are in the attendee list. It must not correct their spelling.
- The LLM must give a timestamp and an exact quote for each decision and each action item. These stay in the private transcript reference, not in the public minutes.
- The pipeline records each display name change of a participant in a meeting.
- The pipeline follows track owner changes (`TRACK_OWNER_SET`), because Jitsi can assign an audio source to a different participant.

### 5.4 Repository layout

The repository is `FreeCAD/Meetings`. The local directory `notetaker` is the basis of the repository.

```
bot/                     # information related to the notetaker bot
  reference/             # plans and research (this document)
  src/                   # bot source code
meetings/
  <series_name>/
    <YYYY-MM-DD>/
      agenda.md          # optional
      minutes.md
```

- The agent writes `minutes.md` into the directory for the meeting date. It reads `agenda.md` from the same directory, if the file is there.
- A person adds `agenda.md` before the meeting. The agent does not change it.
- The bot configuration is in `bot/`: the series list with the deny flags, and the glossary of FreeCAD terms. The file names are not decided.
- When the calendar has a new series, the agent adds a series entry and a new `meetings/<series_name>/` directory in the same pull request.
- The calendar event, not the room name, selects the series.
- Proposed series directory names: `developers`, `occt-dev`, `addon-developers`, `cam`, `fpa`, `dwg`, `bim`. The two Developers meeting series share `developers`.
- The PR & Issues Review series is on the deny list, so it has no directory.
- Each minutes file has these sections: series and date, attendees, topics, decisions, action items with owners, and a statement that an automated agent made the draft.

### 5.5 Cost estimate

| Item | Each month |
|---|---|
| Speech-to-text, local model | 0 USD, but the server needs a CPU with sufficient capacity |
| LLM, 31 meeting hours, two calls for each meeting | approximately 10 USD [U, an estimate from list prices of 4 USD and 20 USD for each million tokens] |
| Small virtual server | 5 USD to 10 USD [U] |
| Total | 15 USD to 20 USD, plus a larger server if the small server is too slow [U] |

- This is an estimate. The LLM and server prices were not checked against current price lists.
- Some vendors bill each audio channel. Send only the speech segments of each track to prevent a higher cost.
- The current screenapp.io subscription costs approximately 12 EUR each month and needs manual work.

## 6. Risks

| Risk | Effect | Mitigation |
|---|---|---|
| No person with an account opens the room | The bot cannot record | The bot waits, then reports. A self-hosted Jitsi removes this limit. |
| `meet.jit.si` changes its page or blocks automated guests | Capture stops | Monitor each meeting. Keep Vexa and self-hosted Jitsi as alternatives. |
| Two meetings follow each other in the shared room | Minutes of one meeting contain the other | Split at the calendar boundary. Give each series its own room. |
| Display names are free text ("Chris", "chris h", "iPhone") | Names differ between meetings, or do not identify a person | The reviewer corrects names. A roster file is a possible later addition. |
| Any maintainer can merge, thus no person is responsible | Pull requests stay open | Send a reminder after 7 days. Assign owners later if necessary. |
| Notice only, with participants in the EU | A participant objects to the record | The FPA approved the policy for the proof of concept. Write the policy down at formal adoption. This document is not legal advice. |
| The transcript text goes to a hosted LLM vendor | Data protection concern | No audio leaves the server. Sign a data agreement with the LLM vendor, or use a local LLM. |
| The LLM invents a decision | Wrong public minutes | The check pass, the low confidence list, and the human review. |
| Speech-to-text errors on jargon and accents | Wrong terms in minutes | The glossary and keyterms. Reviewers add terms to the glossary. |
| A meeting moves to a different platform | No minutes | The agent reports skipped events. The community keeps recorded meetings on Jitsi. |

## 7. Open decisions

1. **Self-hosted Jitsi.** The design operates on `meet.jit.si`. A self-hosted Jitsi removes the room-open limit and permits the native multitrack recorder.
2. **Migration of old agendas and minutes.** Decide when and how the content of `FreeCAD/FreeCAD-developer-meetings`, `FreeCAD/FPA/minutes`, the Nextcloud files, and the Google Doc moves to `Meetings`.
3. **Transcript access.** Decide where the private transcript is kept for 30 days and which reviewers can read it.
4. **LLM vendor approval.** The proof of concept sends the text transcript to Infomaniak AI Tools. The formal policy approval must include this vendor use and its data agreement.
5. **Calendar notice text.** Decide who adds the notice to each calendar event.
6. **Room for each series.** Decide if each series gets its own Jitsi room.
7. **Series directory names.** Confirm the names proposed in section 5.4.

Closed decisions:

- Repository: `FreeCAD/Meetings`, with the layout in section 5.4.
- Record policy: approved for the proof of concept. Formal adoption occurs after the test.
- Deny list: only the PR & Issues Review series.

## 8. Next steps

### 8.0 Proof of concept

1. Done: the capture test is in `bot/src`. See section 8.1.
2. Done: one real meeting was recorded on `meet.jit.si`. Listen to the files to confirm that each file contains only its participant.
3. Done: `bot/src/transcribe.py` transcribes a capture with a local model. The model `large-v3-turbo` is selected. See section 8.1.
4. Done for a short meeting: `bot/src/minutes.py` makes the minutes with a local model (`qwen3.5:9b`). See section 8.1. A test on a full meeting is the next step. The Infomaniak backend made the minutes of the test meeting, and the user accepted them (2026-10-07). No real call was made with the Claude API backend.
5. Give the results to the FPA for the formal adoption of the policy.

### 8.1 Capture test result (2026-10-06)

The self test (`bot/src/selftest.js`) passed on a public Jitsi host that needs no login.

- Two fake speakers, "Chris" and "Kris", sent different tones. Each captured file contained only the tone of the speaker in its label.
- The duration of each file agreed with the event offsets to 0.1 second. A mute interval of 5 seconds stayed in the file as silence.
- The bot recorded a display name change of a participant.
- On `meet.jit.si`, a guest in a room that is not open gets the wait page "no moderators have yet arrived". The bot waits on this page.

Real meeting test, `meet.jit.si/FreeCADCAMMeetup`, 6 minutes, 3 participants:

- The bot joined a room that was open and made one file for each participant, with the correct display names.
- The duration of each file agreed with the event offsets to 0.1 second. One participant was muted for 4 minutes.
- No person has listened to the files yet to confirm that each file contains only its participant.

Local transcription of that meeting (`large-v3-turbo`, CPU, 16 threads):

- The run took 264 seconds for a meeting of 362 seconds.
- The merged transcript gives the conversation in the correct sequence, with the speaker names from the capture.
- The script must split the words at each pause. Without this step, short answers got wrong times.
- The local GPU (GTX 970, 4 GB) is not usable for the model.

Comparison of two local models on that meeting (one meeting of 6 minutes, so the result is not conclusive):

| Model | Run time | Result |
|---|---|---|
| `large-v3-turbo` | 264 s (0.73 of the meeting) | 792 words. One clear error: "genetic" for "generic". |
| `large-v3` | 777 s (2.15 of the meeting) | 744 words. It lost some short questions and answers of one speaker. It wrote "camp" for "CAM". |

- `large-v3-turbo` is the selected model: it is three times faster and it lost less speech in this test.
- No person has compared the transcripts with the audio word for word.

Minutes of that meeting with a local LLM (`qwen3.5:9b` through Ollama, CPU only):

- The run took 15.5 minutes for a meeting of 6 minutes: 23 input tokens each second and approximately 2 output tokens each second.
- The two topic summaries were correct.
- The one action item was correct, but the model wrote the owner as a short form of the name, not the exact display name. The name check marked it.
- The model reported five expressions of agreement ("Sounds good") as objections. The support check marked all five, but did not remove them.
- The model did not report the one real proposal as a proposal.
- No comparison with the Claude API was made, because no API key was available.

Second run, after a change of the prompt, the schema, and the check (user decision of 2026-10-06: continue with the local model):

- The run took 300 seconds (250 s for the draft and 50 s for the check). The second call used the prompt cache of the first call.
- No false objections. The owner of the action item has the exact display name, because the schema accepts only names from the attendee list.
- The checks marked or removed no item. The minutes have three correct topics, no decisions, and one correct action item.
- One topic ("Testing a note-taking application") is small talk and does not belong in the minutes.
- The local model was the default backend of `bot/src/minutes.py` until 2026-10-07. The default is now the Infomaniak backend.

Not tested:

- A track owner change (SSRC rewriting). The code has a path for it, but no test caused it.
- A long meeting, a large meeting, and a participant who connects again.
- A room with a lobby.

### 8.2 After the proof of concept


6. Done: the `FreeCAD/Meetings` repository contains this directory.
7. Build the scheduler and the ICS parser.
8. Done: `bot/src/publish.py` opens the pull request for one meeting. The scheduler does not start it automatically.
9. Operate a pilot on two series for one month, then add the other series.
10. Move the old agendas and minutes into the repository.

## 9. Sources

Jitsi and bots:

- https://jitsi.org/blog/a-new-architecture-for-transcription-and-more/
- https://jitsi.org/blog/authentication-on-meet-jit-si/
- https://jitsi.org/blog/improving-performance-on-very-large-calls-introducing-ssrc-rewriting/
- https://github.com/jitsi/jitsi-multitrack-recorder
- https://github.com/jitsi/opus-transcriber-proxy
- https://github.com/jitsi/jigasi
- https://github.com/jitsi/skynet
- https://github.com/jitsi/jibri
- https://github.com/korjavin/jitsi-recorder
- https://github.com/Vexa-ai/vexa
- https://github.com/attendee-labs/attendee
- https://docs.recall.ai/docs/meeting-platforms
- https://guide.fireflies.ai/articles/8445630399-how-to-integrate-jitsi-with-fireflies
- https://screenapp.io/features/jitsi-ai-notetaker

Speech-to-text and speaker separation:

- https://www.assemblyai.com/pricing
- https://developers.deepgram.com/docs/keyterm
- https://developers.openai.com/api/docs/guides/speech-to-text.md
- https://arxiv.org/pdf/2509.14128
- https://huggingface.co/pyannote/speaker-diarization-community-1
- https://www.dograh.com/feeds/blog/whisper-hallucination-silence

Data protection:

- https://www.edpb.europa.eu/system/files/2021-07/edpb_guidelines_202102_on_vva_v2.0_adopted_en.pdf
- https://www.skwschwarz.de/en/news/transcription-of-video-conferences

FreeCAD:

- https://www.freecad.org/events.php
- https://github.com/FreeCAD/FreeCAD-developer-meetings
- https://github.com/FreeCAD/FPA/tree/main/minutes
- https://github.com/FreeCAD/FPA/issues/246
- https://github.com/FreeCAD/FPA/issues/469
- https://github.com/FreeCAD/FreeCAD-developer-meetings/issues/40
