# Developers Meeting: 2026-11-01

> Crow, an automated notetaker, made these minutes. They may contain mistakes or inaccuracies and are for reference only.
>
> Model: Qwen/Qwen3.5-397B-A17B-FP8  
> Source code: <https://github.com/FreeCAD/Meetings/tree/main/bot>

## Attendees

- Pieter
- Max
- sliptonic
- Billy (aka Connor)
- pierreporte
- creymore
- caio-venancio
- Tanju
- Jackson Oursland
- GeeBee
- JohnOCFII
- Dmitrii/@dpasukhi

## Topics

### Meeting logistics and channel limits

The meeting started with technical difficulties regarding the video conferencing channel time limits. It was noted that the limit is per day per channel name, not per meeting. Because the channel was used earlier for an OCCT dev meeting, the remaining time for this Developers Meeting was reduced. Participants agreed that future meetings should use distinct channel names to avoid burning up the daily limit.

### Release blockers and Release Candidate plan

The group discussed the remaining blockers for the upcoming release. Four blockers were identified: a unit error in the dimension field, conflicting licenses in TechDraw templates, an assembly hasher mismatch, and a hidden member issue in a Python group related to AI policy. The consensus was to fix all blockers before issuing a final Release Candidate. Once the Release Candidate is issued, a one-week period would follow before the full release, allowing time to catch any severe issues not previously marked as blockers. The website update was noted as independent and should not block the release.

Links from the meeting chat:

- <https://github.com/FreeCAD/FreeCAD/issues/33388>
- <https://github.com/FreeCAD/FreeCAD/pull/33728>
- <https://github.com/FreeCAD/FreeCAD/pull/34018>
- <https://github.com/FreeCAD/FreeCAD/issues/32954>
- <https://github.com/FreeCAD/FreeCAD/issues/33675>

### AI policy and community trust

The meeting discussed the FreeCAD AI policy following negative feedback on social media. Participants generally supported the current policy, which requires a human to be in the loop, responsible for the PR, and able to stand behind the code. Concerns were raised about "drive-by" contributions where AI is used to generate large amounts of code without community engagement or intent to maintain. The group emphasized that trust and collaboration are more valuable than code volume. It was noted that large PRs require extra scrutiny and that contributors should be established members of the community who communicate with maintainers before submitting significant changes.

Links from the meeting chat:

- <https://social.freecad.org/@freecad/117449849310612601>

## Decisions

- The group agreed to fix all remaining blockers before creating the next Release Candidate, followed by a one-week testing period before the full release. *(review)*

## Action items

- **sliptonic:** Write a comment on the PR regarding the hidden member issue to clarify that the objection is to the communication method (AI-generated description) rather than the code fix itself.
- **Pieter:** Investigate the unit error issue (dimension field) and attempt to fix it or determine if the related PR should be reverted.
