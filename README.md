# FreeCAD Meetings

This repository contains the agendas and the minutes of the public FreeCAD community meetings.

| Directory | Content |
|---|---|
| `meetings/` | One directory for each meeting series, with one directory for each meeting date. |
| `bot/src/` | The source code of Crow, the bot that records the meetings and drafts the minutes. |
| `bot/reference/` | The plan and the research for the bot. |
| `bot/glossary.txt` | FreeCAD terms that the bot uses to read the transcripts. |

Crow joins a meeting with the display name "Crow - AI Notetaker". It drafts the minutes and opens a pull request. A maintainer reviews each pull request before the merge.

This is a proof of concept. See `bot/reference/document.md` for the plan and `bot/src/README.md` for the procedures.
