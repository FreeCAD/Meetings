# CAM Meetup: 2026-11-06

> Crow, an automated notetaker, made these minutes. They may contain mistakes or inaccuracies and are for reference only.
>
> Model: Qwen/Qwen3.5-397B-A17B-FP8  
> Source code: <https://github.com/FreeCAD/Meetings/tree/main/bot>

## Attendees

- Billy (aka Connor)
- Carl
- J
- Jaka
- Alan Grover
- sliptonic
- 3
- Jackson Oursland
- jffmichi
- David
- entuland
- MTronic/Stefan
- Fae
- Lemuria

## Topics

### Meeting logistics and new attendees

The meeting addressed technical issues with the meeting URL causing bot access problems. New attendee Jaka introduced himself and asked about testing resources for CAM setups, specifically for Siemens 840D. The group discussed the lack of physical integration tests and the concept of 'golden' G-code files for unit testing. Billy mentioned questions from Dr. Marco regarding fourth-axis drilling and thread milling, noting current limitations in defining work planes for rotary operations.

### Pull Request #33100 (Qt version requirement)

The group reviewed a PR requiring Qt 6.7. Despite a minor note about the version requirement, the consensus was that it was acceptable, and the PR was merged with a backport label for version 26.3.

### Pull Request #33226 (M6T variations)

Discussion centered on whether to merge this PR into the 26.3 release. It was determined that the changes add options for M6-T interactions rather than fixing a critical bug or regression. The group agreed to defer the decision, allowing more time for review, and noted it would not block the release.

### Pull Request #33323 (Machine state/UI option fix)

This PR addresses a bug where a UI option in the machine-based post-processor did not function correctly. The group identified it as a bug fix suitable for the 26.3 release and agreed to flag it for backport.

### Pull Request #34027 (Counterbore depth logic)

Billy presented a fix for counterbore operations that were incorrectly rejecting duplicate holes. While technically adding new feature behavior regarding depth calculation, the group agreed the change was low-risk and necessary to resolve the functional issue, deciding to merge it.

### Rotary parentage and axis configuration

Billy and sliptonic discussed complex issues with rotary axis configurations (AC, BC) where compensating errors masked underlying logic flaws. Sliptonic committed to testing the proposed fixes on his physical rotary table over the weekend to verify correct movement before finalizing the merge.

### Pull Request #31760 (Tag dressup recompute)

This PR fixes an annoyance where tag dressups do not automatically recompute when the base operation changes. The group classified this as a feature improvement rather than a bug fix and scheduled it for the 27.1 release.

### Job operations subgroup

The group briefly discussed a PR involving job operation subgroups. It was noted that the change is largely GUI-related and touches many files. No final decision was made, but it was tentatively targeted for 27.1 pending further review.

### Sanity checks refactoring (PR #32576)

A debate occurred between incremental bug fixes versus a major refactoring of the 'Sanity' checking system. David proposed merging the current incremental improvements while assigning sliptonic to create a roadmap or epic describing the long-term vision for the system. Sliptonic agreed to draft this roadmap.

Links from the meeting chat:

- <https://github.com/FreeCAD/FreeCAD/pull/33739>

### Pull Request #32728 (New Deburr operation)

The group reviewed a new Deburr operation intended to replace the old one. They established a deprecation schedule: the old operation will show a warning in 27.1, be hidden in 27.2, and removed in 27.3. Billy agreed to perform a CAMPR review.

### Pull Request #32925 (Error message and check cleanup)

This PR improves error messages for identical start/final depths and moves redundant height checks to the base class. Billy accepted the task to review the specific changes regarding clearance and safe height checks.

### Pull Request #33001 (Dynamic retract height)

Discussion focused on a new 'flexi height' or 'dynamic retract height' feature allowing the tool to hop over obstacles at intermediate heights. Concerns were raised about interactions with canned cycles (G81, etc.). Billy agreed to investigate the implementation details and validate it against canned cycles.

### Pull Request #33038 (Handle multiple features for Pocket Shape)

This PR extends the 'handle multiple features' capability to the Pocket Shape operation. The group discussed whether property migrations were required due to moving properties between classes. It was concluded that if properties match exactly, no migration is needed, but verification was requested.

### Pull Request #33275 (Full circle detection tolerance)

A small fix regarding the tolerance for detecting full circle G2/G3 moves was discussed. David expressed concern about the precision logic and agreed to add a comment to the PR detailing the need for a robust decision method on what constitutes a full circle.

### Pull Request: Tool holders and ADR

Billy presented a large PR adding standardized tool holders and a new file format. Concerns were raised about the terminology's applicability to lathe tools versus mills. The group agreed to proceed with the PR for 27.1 but to reduce the number of shipped predefined tool holders to a single generic example, moving the rest to an add-on.

### Pull Request #33535 (Block delete and operation annotations)

Fae's PR for block delete was pulled back to 27.1 due to complexity. The discussion highlighted a missing capability for operation-level annotations. Sliptonic agreed to create an issue to investigate operation-level annotations, assigning Alan Grover to lead the research.

### Pull Request: Lollipop and Keyway cutters

This PR corrects properties for reamers and adds support for lollipop and keyway cutters. It also touches on the deprecated CAMotics simulator. The group agreed to merge the cutter changes and separately create an issue to fully sunset the CAMotics integration.

### CAM Simulator Epic and upcoming PRs

Billy outlined the roadmap for the new CAM simulator, starting with an enhanced CSG simulator for 3+2 machining as a fallback, followed by a Voxel-based simulator. He noted the large size of the upcoming PRs and the potential for code churn between stacked PRs. The group encouraged open communication via the Epic issue.

### Recent GitHub Issues and Adaptive Clearing

Alan highlighted new issues, including a bug report for version 26.3 RC2. David discussed two PRs related to migrating Adaptive Clearing from Clipper 1 to Clipper 2. The group decided to merge the migration PR immediately but to defer the associated bug fix PR to a future point release (26.3.1 or later) rather than backporting it immediately.

Links from the meeting chat:

- <https://github.com/FreeCAD/FreeCAD/pull/33739>
- <https://meet.jit.si/FreeCADCAMMeetup>

## Decisions

- Merge PR #33100 with a backport label for version 26.3.
- Defer decision on PR #33226 (M6T variations) for 26.3; it will not block the release.
- Flag PR #33323 for backport to 26.3 as it fixes a bug.
- Merge PR #34027 (Counterbore fix) despite it being technically a feature, as it resolves a functional refusal.
- Schedule PR #31760 (Tag dressup recompute) for version 27.1 as a feature.
- Merge incremental Sanity check fixes (PR #32576) while deferring major refactoring until a roadmap is defined.
- Adopt a deprecation schedule for the old Deburr operation: warning in 27.1, hidden in 27.2, removed in 27.3.
- Reduce shipped predefined tool holders in the Tool Holder PR to a single generic example; move additional definitions to an add-on.
- Merge the Lollipop and Keyway cutter PR, and create a separate issue to sunset CAMotics integration.
- Merge the Adaptive Clearing Clipper 2 migration PR immediately, but defer the associated bug fix PR to a future point release rather than backporting to 26.3.

## Action items

- **sliptonic:** Test rotary axis fixes on physical hardware (AC table) over the weekend.
- **Billy (aka Connor):** Investigate and finalize the drop-down change for rotary preferred direction.
- **sliptonic:** Create a roadmap or epic description for the future direction of the Sanity checking system. *(review)*
- **Billy (aka Connor):** Perform a CAMPR review on PR #32728 (Deburr operation).
- **Billy (aka Connor):** Investigate the 'dynamic retract height' implementation (PR #33001) and validate it against canned cycles.
- **David:** Verify if migrations are required for PR #33038 (Handle multiple features for Pocket Shape). *(review)*
- **David:** Add a comment to PR #33275 regarding the logic for full circle detection tolerance.
- **Billy (aka Connor):** Reduce the number of shipped tool holder assets to a single generic example before merging.
- **sliptonic:** Create a GitHub issue to investigate operation-level annotations and assign Alan Grover to it.
- **sliptonic:** Create a GitHub issue to sunset CAMotics integration completely.
- **Billy (aka Connor):** Assign the reported 26.3 RC2 bug to himself and Brad.
