# BIM Meetup: 2026-10-13

## Attendees

- Roy
- marcuspollio
- Tom (semhustej)
- MarkkoMartin
- sliptonic

## Topics

### AI Note-taker Setup

Participants acknowledged the new AI note-taker bot. sliptonic explained that the bot will post minutes as a pull request to the meetings repository about an hour after the meeting ends, and requested that any corrections be made via comments on that pull request.

### BIM Toolbar Icons Consolidation

Tom reported an issue regarding the 'BIM Extrude' and 'BIM Extrude Face' tools having separate icons despite similar functionality, suggesting they be grouped to reduce toolbar clutter. Roy agreed with the idea and noted he would check the status of the translation/UI freeze to ensure new strings could still be added before the 26.3 release.

Links from the meeting chat:

- <https://github.com/FreeCAD/FreeCAD/issues/33503>

### BIM Project Board Utility

The group discussed the utility of the GitHub BIM project board. Tom noted he did not find it advantageous compared to standard issue filtering. Marcus explained that the board automatically adds items with the 'BIM' label but requires manual maintenance for subcategories. It was agreed that if the board is not being actively used or maintained, it might be removed, though Marcus offered to investigate making it more useful (e.g., filtering for blockers) before a final decision is made.

### Meeting Notes Repository Migration

Marcus proposed moving all previous BIM meeting notes from the old cloud location to the new meetings repository to centralize them. The participants agreed this was logical, and Marcus volunteered to create pull requests to migrate the old notes.

### Collections and View Filters Prototype

Marcus presented a concept called 'Collections' (previously referred to as 'Scenes'), a core FreeCAD utility to group objects based on rules and filters rather than physical containers. He demonstrated a Python prototype addon that allows defining collections via JSON rules based on object properties. The group discussed potential synergies with the BIM Report workbench and Joao's drawing prototype. Marcus plans to refine the prototype, create UI mockups, and consult with the Design and TechDraw workgroups before proposing it as a core feature or FreeCAD Enhancement Proposal (FEP).

### Deprecation of GetGlobalPlacement

Roy raised a concern about the upcoming deprecation of the `GetGlobalPlacement` function, which is currently used extensively in the BIM workbench for exporting buildings and levels. He explained that the replacement function requires a specific nesting path, which conflicts with the current export logic that collects objects regardless of nesting. The group agreed this requires significant refactoring and decided to discuss it further in a future meeting, potentially targeting the 27.1 development cycle.

## Decisions

- The meeting agreed to combine the 'BIM Extrude' and 'BIM Extrude Face' icons into a single command, pending verification of the UI freeze deadline for the 26.3 release.
- The meeting agreed to migrate all previous BIM meeting notes to the new meetings repository to have a single location for archives.

## Action items

- **Roy:** Check the UI freeze deadline for the 26.3 release to confirm if new strings for the combined icon command can still be added.
- **Roy:** Look into the pull request for combining the BIM Extrude icons.
- **marcuspollio:** Create pull requests to move previous BIM meeting notes into the new meetings repository.
- **marcuspollio:** Clean up the code for the 'Collections' prototype, add documentation, and prepare instructions for running it as a module.
- **marcuspollio:** Create UI mockups for the 'Collections' feature and consult with the Design and TechDraw workgroups (specifically Peter) to gather feedback.

---

An automated agent made this draft from a transcript of the meeting. A maintainer reviews it before publication.
