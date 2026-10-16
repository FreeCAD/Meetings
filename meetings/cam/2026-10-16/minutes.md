# CAM Meetup: 2026-10-16

> Crow, an automated notetaker, made these minutes. They may contain mistakes or inaccuracies and are for reference only.
>
> Model: Qwen/Qwen3.5-397B-A17B-FP8  
> Source code: <https://github.com/FreeCAD/Meetings/tree/main/bot>

## Attendees

- jffmichi
- sliptonic
- Fae
- 3
- MTronic/Stefan
- Alan Grover
- Jackson Oursland
- Billy (aka Connor)
- David

## Topics

### Epic management and tracker cleanup

The meeting discussed moving Epic descriptions from the source tree (stored as pull requests) to top-level GitHub issues to allow for more flexible editing and tracking. Several existing epics were reviewed: 'Better tool library' and 'Circular holes improvement' were considered complete; 'Clipper' is ongoing with arc fitting work; 'Feeds and speeds' consolidation is deferred; 'Core dressups' will be retooled as an epic for version 27.1 to include base class consolidation; and the 'Post-processors' epic was closed as the focus shifts to adding specific machines rather than infrastructure changes. The tracker count for the CAM workbench was noted to be at a historic low of about 75 issues.

### Release candidate preparation and pull request reviews

The team reviewed open pull requests ahead of the upcoming release candidate tagging. The 'Dynapath' PR requires a final review from Alan Grover. The 'Dragknife' PR was approved by Billy. The 'Clipper' PR, addressing arc fitting and pre-processing bugs, was deemed an improvement despite some remaining questionable areas; it was decided to merge it now and address further issues in the next iteration. A translation fix PR was discussed, specifically regarding string interpolation in `base.py` where tool names were accidentally removed; Billy agreed to comment on the PR to request restoring the names.

### Machine templates and community repository integration

Discussion focused on the user experience when using machine templates from the community repository. Currently, users must explicitly create a local copy of a template to use it in a job, which prevents unexpected behavior changes if the upstream template is updated. Fae proposed adding version tracking and warnings (or a diff view) to notify users when a community machine template has been updated. It was agreed that the UI should clearly distinguish between templates and user machines, and sliptonic will add guidance in the machine editor to advise installing the machines add-on.

### Automated issue reproduction using AI (CAMPR bot)

Billy demonstrated an automated system using an LLM and a custom Model Context Protocol (MCP) to reproduce and analyze GitHub issues. The bot can read issue descriptions, attempt to recreate test files, run headless tests, and post findings back to the issue thread. Access is currently limited to specific contributors to manage costs. The group discussed the potential for running this via a GitHub App bot account for transparency.

Links from the meeting chat:

- <https://github.com/Connor9220/Freecad-MCP-plus>

### ADR-010: Tool holder definition and lathe support

The group reviewed Architectural Decision Record 10 (ADR-010) regarding the definition of a 'tool holder'. Concerns were raised that the current draft implies a milling-centric definition (referencing the spindle nose) which conflicts with lathe terminology (tool post). Participants suggested generalizing terms like 'spindle' to 'spindle/tool post' and explicitly acknowledging future lathe support to avoid rework. Fae offered to review the document and provide specific suggestions for accommodating lathe geometry and terminology.

Links from the meeting chat:

- <https://github.com/FreeCAD/FreeCAD/pull/33612>
- <https://github.com/Connor9220/FreeCAD/blob/d835b65b9e140b5d944b9b76c0416edcee04f836/src/Mod/CAM/Roadmap/ADR/ADR-010.md>

### Work holding and simulation demo

Billy provided a demonstration of new work holding features, including the ability to move and place vises, clamps, and 1-2-3 blocks in the simulation environment. Collision detection for tool holders was also shown. Additionally, a tutorial video generated entirely by an AI assistant using the custom MCP was shared, showcasing the potential for automated documentation and content creation.

Links from the meeting chat:

- <https://www.youtube.com/watch?v=pEyQGzIL55I>

## Decisions

- Move Epic descriptions from the source tree to top-level GitHub issues to allow for easier editing and tracking of sub-issues.
- Close the 'Better tool library' and 'Circular holes improvement' epics as complete.
- Defer the consolidation of feeds and speeds calculations to a later date.
- Retool the 'Improving core dressups' epic for version 27.1 to include consolidating code into a base class.
- Close the 'Post-processors' epic as the work has shifted to adding specific post-processors and machines rather than infrastructure changes.
- Merge the Clipper arc fitting pull request in its current state as an improvement, deferring remaining questionable issues to the next iteration.
- Create a GitHub issue to track the reported bug where post-processors output XY moves before Z moves, as it was previously only reported on the forum.

## Action items

- **sliptonic:** Move Epic descriptions from the source tree to top-level GitHub issues and perform cleanup.
- **Billy (aka Connor):** Create a top-level roadmap issue for 27.1 to coordinate remaining tooling work for plasma, jet, and laser tools.
- **Alan Grover:** Review the Dynapath pull request.
- **Billy (aka Connor):** Review the Dragknife pull request and comment on the translation PR to request restoring tool names in `base.py`.
- **Fae:** Draft a GitHub issue with mock-up graphics proposing a version warning system for community machine templates.
- **sliptonic:** Add guidance in the machine editor to advise users to install the machines add-on.
- **Fae:** Review ADR-010 and provide comments or a write-up on how to adapt the tool holder definition for lathe support. *(review)*
