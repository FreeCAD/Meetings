# FreeCAD BIM Meetup Notes — 22nd September 2026

Attendees:

- [@Roy-043](https://github.com/Roy-043)
- [@maxwxyz](https://github.com/maxwxyz)
- [@semhustej](https://github.com/semhustej)
- [@tritao](https://github.com/tritao)
- [@markkomartin](https://github.com/markkomartin)
- [@marcuspollio](https://github.com/marcuspollio)

## Overview

The meeting focused on two main topics:

1. Preparing BIM-related work for the FreeCAD 26.3 feature cutoff.
2. Reviewing João's contextual-editing work and how it should be integrated into BIM and FreeCAD core.

The group also briefly discussed release documentation, and BIM terminology.

#### __1. FreeCAD 26.3 release__

There are more than 30 PRs associated with the 26.3 milestone, although many are still drafts.

With the September 30 feature cutoff approaching, contributors should identify which feature PRs genuinely need to be included in 26.3. Those should be moved to ready-for-review, tested, and explicitly brought to reviewers' attention.

Work that is not realistically ready should move to a later or TBD milestone rather than being rushed through review.

The live-preview work was discussed in this context and moved away from the immediate 26.3 target while the more general BIM interaction architecture develops.

#### __2. Contextual editing architecture__

João demonstrated the current contextual-editing branch.

The work has grown beyond plan editing into a broader architecture for BIM views and interaction. The goal is to support different representations of the same BIM model—such as plan, 3D, sections, and elevations—while keeping the underlying BIM objects unchanged.

The branch currently includes work around:

- BIM view contexts.
- Contextual task panels and object interaction.
- Plan and 3D view switching.
- Layers and view-specific controls.
- TechDraw integration.
- Section and clipping-plane infrastructure.
- Reusable preview and interaction behavior.

A key objective is to avoid implementing features such as live preview independently for each BIM object type. Instead, common behavior should live in reusable infrastructure.

Performance has also been a major part of the work. Operations such as wall recomputation and openings currently make some interactive workflows too expensive, so João has been optimizing these lower-level paths.

#### __3. FreeCAD core and BIM integration__

Part of the contextual-editing work requires changes below the BIM workbench itself.

João has been introducing generic concepts such as view definitions and view contexts into FreeCAD core, together with changes related to task panels, TechDraw, clipping planes, and the 3D viewer.

The intention is to keep these mechanisms generic rather than introducing BIM-specific behavior into core.

The group agreed that the architecture should be reviewed before attempting to merge the full BIM-side implementation.

João plans to:

- Document the architecture and explain how the different layers fit together.
- Publish the reorganized development branch for testing.
- Provide pre-built packages for contributors who do not build FreeCAD locally.
- Extract mature, self-contained core changes into separate PRs.

The BIM-side work should then be integrated progressively rather than arriving as a large collection of independent PRs.

#### __4. BIM interaction ideas__

The demonstration led to a short discussion about how BIM editing should work from the user's perspective.

One open question is how contextual controls should relate to FreeCAD's existing distinction between normal object interaction and explicit edit mode.

João is exploring an approach where selecting an object exposes relevant contextual controls directly, rather than always requiring a separate edit mode.

Tom also proposed automatic contextual dimensions: selecting an object such as a door could display relevant distances to surrounding geometry, allowing the user to edit those values directly.

The group considered this useful, while noting that these dimensions should not necessarily imply permanent geometric constraints.

Max suggested draggable guides from the plan-view rulers as another useful editing aid.

These ideas were considered follow-up work rather than requirements for the current contextual-editing branch.

#### __5. Documentation__

Roy said the 26.3 release notes are mostly current and will review the remaining recent PRs for missing documentation.

Once development moves beyond 26.3, a new 27.1 release-notes page should be created so changes can be documented from the start of the next cycle.

Marcus also proposed maintaining a BIM terminology glossary.

The initial scope should be an English glossary covering BIM concepts. Translation consistency can be addressed separately once the terminology itself is better established.

Marcus plans to incorporate this into the BIM README/documentation work already in progress.

## Action items

- **26.3 contributors:** Identify which feature PRs must land before the September 30 cutoff.
- **PR authors:** Move relevant drafts to ready-for-review and explicitly request testing/review.
- **PR authors/maintainers:** Move unfinished work to a later or TBD milestone where appropriate.
- **João:** Publish documentation describing the contextual-editing architecture.
- **João:** Publish the reorganized branch and provide test builds.
- **João:** Extract mature generic/core changes into separate reviewable PRs.
- **Group:** Test the contextual-editing branch and provide feedback on the workflow.
- **Tom:** Share an example of the contextual-dimension workflow discussed in the meeting.
- **Roy:** Check recent 26.3 changes for missing release-note entries.
- **Marcus:** Continue the BIM README work and add an initial terminology glossary.

## Next meeting

Likely follow-up topics:

- 26.3 PR status before the September 30 cutoff.
- Review of the published contextual-editing architecture.
- Feedback from test builds.
- Integration strategy for the core and BIM-side changes.
- Contextual UI and edit-mode behavior.
- BIM terminology and release documentation.

## 
