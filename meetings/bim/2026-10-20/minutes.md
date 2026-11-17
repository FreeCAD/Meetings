# BIM Meetup: 2026-10-20

> Crow, an automated notetaker, made these minutes. They may contain mistakes or inaccuracies and are for reference only.
>
> Model: Qwen/Qwen3.5-397B-A17B-FP8  
> Source code: <https://github.com/FreeCAD/Meetings/tree/main/bot>

## Attendees

- Roy
- Markko Martin Loris De Rosso

## Topics

### Meeting time adjustment for end of summertime

With summertime ending, the participants discussed adjusting the meeting time to maintain the same local European time. They agreed to propose a change to 17:00 UTC to the wider group.

### Participation in shared documentation

Roy clarified that the shared documents regarding BIM workflows are intended for all users, not just developers. He encouraged non-programmers to contribute their practical experiences and views to improve the documents.

### Status of Jao Tritao's project and concerns about scope

Markko expressed concern that Jao Tritao's project might be too abstract or 'reinventing the wheel,' suggesting a simpler, incremental approach might be more immediately useful. Roy acknowledged the long-term nature of the project but agreed that immediate improvements should not be forgotten. Roy noted he is not fully aware of the project's full scope but mentioned that test models and code are being prepared to help prevent regressions.

### Multi-material display bug

Markko reported a bug where multi-material objects (specifically windows) display only one color instead of distinct materials. Roy mentioned a potential fix he has developed that is not yet merged. Markko agreed to test the latest release candidate and file a GitHub issue if the problem persists.

### Reporting issues to GitHub

Markko hesitated to report bugs due to the high number of existing open issues. Roy strongly encouraged reporting all issues regardless of the current count, emphasizing that it is a vital communication channel and that he specifically monitors BIM-related issues.

## Decisions

- The meeting participants agreed to propose changing the meeting time to 17:00 UTC to accommodate the end of summertime. *(review)*

## Action items

- **Markko Martin Loris De Rosso:** Read the shared documents and write down his opinion on the matters discussed.
- **Markko Martin Loris De Rosso:** Test the new release candidate for the multi-material bug and open a GitHub issue if the problem persists.
