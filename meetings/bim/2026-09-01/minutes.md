# FreeCAD BIM Meetup Notes — 1st September 2026

Attendees:

- [@Roy-043](https://github.com/Roy-043)
- [@maxwxyz](https://github.com/maxwxyz)
- [@semhustej](https://github.com/semhustej)
- [@tritao](https://github.com/tritao)
- [@markkomartin](https://github.com/markkomartin)
- [@aothms](https://github.com/aothms)
- [@marcuspollio](https://github.com/marcuspollio)

## Overview

The meeting focused on improving coordination around  FreeCAD BIM development, establishing a lightweight roadmap, improving  PR review and maintenance, and discussing several technical and  organizational topics.

Participants agreed that regular meetings could help  provide a central place for BIM contributors, developers, testers,  documentation contributors, and users to coordinate work and discuss  priorities.

#### __1. Introductions__

1.1 Every attendee briefly presented themself, their interest and experience in BIM and AEC (architecture, construction, and engineering), except @aothms who unfortunately had sound issues.

#### __2. Meeting organization__

2.1 General agreement that future meetings should have a lightweight agenda rather than being completely informal. Proposed format is a shared, editable document with a few recurring topics, while still allowing new topics to be added freely.

2.2 Possible recurring agenda items include:  
- Open PRs requiring review or testing

\- Bugs, regressions, and feature requests

\- Development priorities and roadmap topics

\- Current development work

\- Larger architectural or workflow proposals

**Decision:** A shared FreeCAD BIM meetup agenda/notes document is created and accessible.

#### __3. BIM roadmap__

3.1 The group discussed whether BIM should have a strict roadmap or a more flexible set of priorities. The consensus was that the roadmap should be driven by what contributors are realistically able and interested to work on rather than defining a large plan without people available to implement it.

3.2 As a starting point, contributors were encouraged to prepare their own short roadmap or list covering:

\- What they are currently working on

\- What they would like to work on

\- What they consider important for FreeCAD BIM

\- Important work that they cannot personally commit to

3.3 These individual views can then be combined to identify shared priorities, overlapping initiatives, and areas where contributors can collaborate. The group also discussed reviewing existing BIM/Draft issues and feature requests and assigning clearer priorities. This would help both existing and new contributors identify valuable work.

**Decision:** Every contributor interested share their own short roadmap with the 3.2 points above on the [common roadmap discussion thread](https://github.com/FreeCAD/FreeCAD/discussions/17139).

#### __4. Python typing for BIM codebase__

4.1 @tritao described ongoing work to introduce stronger Python typing for Draft and BIM. The goal is to improve code completion, developer documentation, static checking, and detect invalid API usage and other mistakes. The work uses standard Python type-hinting mechanisms and existing type-checking tools rather than a FreeCAD-specific solution.

4.2 There was also discussion about modernizing docstrings (currently using NumPy verbose style) alongside type hints. With type information available directly in function signatures, documentation could focus more on explaining behavior and intent instead of duplicating parameter type information.

**Decision:** @marcuspollio will open an issue covering type hints, Python versioning concerns, and related documentation improvements.

#### __5. BIM maintenance__

5.1 @Roy-043 notes the current major BIM maintainer/reviewer workload. Reviewing BIM PRs alone is difficult, particularly for larger or technically complex changes involving Python or C++. The group discussed moving toward shared responsibility rather than relying on one person.

5.2 Potential contributions to the review process include:

\- Triaging issues and PRs  
- Checking whether a proposal fits BIM workflows and architectue  
- Functional testing  
- Code review  
- Providing the final maintainer approval

5.3 @tritao offered to become more active in reviewing BIM PRs. The group also suggested using these meetings to review difficult PRs collectively when useful. For large changes, there was agreement that discussing the architecture and rationale before implementation could make later review significantly easier. Smaller or staged PRs were also encouraged where practical.

**Decision:** Revisit the maintenance topic at next meetings, while trying to split roles and responsibilities among contributors, and encourage adopting [existing contributions guidelines](https://github.com/FreeCAD/FreeCAD/blob/main/CONTRIBUTING.md) to ease the review and maintenance process for everyone.

#### __6. Upcoming 26.3 release__

6.1 Contributors were encouraged to review the BIM and Draft PR backlog, especially work intended for the upcoming release. PR authors should move relevant PRs out of draft status when they are ready and clearly indicate where testing or review is needed. Testing was highlighted as an area where non-maintainer contributors can provide substantial help.

\- [List of current open PRs for BIM](https://github.com/FreeCAD/FreeCAD/pulls?q=is%3Aopen+is%3Apr+label%3A%22Mod%3A+BIM%22+milestone%3A26.3+draft%3Afalse)  
- [List of currently `Draft` PRs for BIM](#)

**Decision:** Every contributor indicate on each own open PR whether they intend their changes to be part of the next 26.3 release, and make sure they are rebased, ready for testing or review, or note that they are targeting a later release cycle.

#### __7. IFCX Core by buildingSMART__

7.1 The group discussed whether FreeCAD should become more involved with the development of the next generation of IFCx standards with a strong FOSS stance. Rather than FreeCAD directly providing significant development manpower, one possible approach would be to support existing IFC experts already involved in the process, including people connected with IfcOpenShell.

**Decision:** @marcuspollio will investigate with @aothms, Dion Moult, and Yorik Van Havre which strategy to adopt, and discuss the topic at a FPA meeting.

#### __8. Code:__ `Arch` __to__ `BIM` __naming__

8.1 The group discussed completing the transition from the older `Arch` naming toward the current `BIM` module naming. There was broad support for the cleanup, but backwards compatibility for existing add-ons and external code was considered important.

8.2 The suggested approach is:

\- Document the overall migration plan in an issue  
- Perform the migration incrementally where useful  
- Maintain backwards compatibility for a significant transition period, potentially around one to two years (three to six releases)  
- Consider providing scripts or tooling to help add-on developers migrate  
- Account for open PRs that may still use the old naming

**Decision:** @marcuspollio will document the broader rationale and migration plan, and @tritao offered to help with the implementation/migration PR.

## Actions

- **All:** Prepare short personal BIM roadmap / list of priorities before a future meeting.
- **@Roy-043:** Go through existing BIM/Draft bugs and consider assigning priorities.
- **All:** Help triage and prioritize existing BIM issues and feature requests.
- **All:** Review and test open BIM/Draft PRs, especially release-targeted PRs.
- **PR authors:** Mark relevant PRs ready for review when appropriate.
- **@marcuspollio:** Open issue covering Python typing/docstring improvements.
- **@marcuspollio:** Bring the IFCx participation/support topic to OSarch.org and FPA for discussion.
- **@marcuspollio:** Document overall Arch → BIM migration rationale and plan and coordinate with **@tritao** on implementation and tooling.

## Next meeting

September 8th 2026 16:00 UTC same online Jitsi

Focus on reviewing selected open PRs and continuing the roadmap/prioritization discussion.
