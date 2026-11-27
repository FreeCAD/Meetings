# CAM Meetup: 2026-11-27

> Crow, an automated notetaker, made these minutes. They may contain mistakes or inaccuracies and are for reference only.
>
> Model: Qwen/Qwen3.5-397B-A17B-FP8  
> Source code: <https://github.com/FreeCAD/Meetings/tree/main/bot>

## Attendees

- Billy (aka Connor)
- MTronic/Stefan
- sliptonic
- Jackson Oursland
- 3
- gyordanvo

## Topics

### Release status and community updates

The group noted that version 26.3 was tagged and the final release announcement is expected soon. Discussion touched on the absence of some community members due to the US holiday. The conversation shifted to the challenge of integrating large new features, such as the simulator and a potential native C++ Sheet Metal workbench, into the core without slowing down the stable release process.

### Proposal for a 'Skunkworks' or bleeding-edge build

A proposal was made to create a separate 'Skunkworks' or 'Bleeding Edge' build of FreeCAD where merge barriers are minimal to allow rapid prototyping of large features. This build would be reset periodically (e.g., every 90 days). Participants discussed how this could help FreeCAD compete with faster-moving projects like SolidCraft by allowing experimentation without compromising the stability of the main branch. It was noted that AI tools could assist in managing the rebasing required for such a branch.

### Review of open issues

The group reviewed several open issues, including a request for constant surface speed support for turning (noting that turning is not yet in the core), a bug regarding copying jobs retaining dependencies, and an issue with grouping operations. A fix for a drive-by AI spamming incident was confirmed as already merged.

### Pull Request: Toolpath binary storage and tool vector (PR #34606)

Discussion focused on a PR to change the toolpath persistence model from text-based G-code to a binary format. This change significantly improves read speeds for large toolpaths and enables the storage of tool orientation vectors at every point, which is necessary for continuous five-axis machining. The change is backward compatible for loading old files but requires recomputation if a new file is opened in an older version. The group agreed to target this for version 27.1.

### Pull Request: Adaptive ramp feed for helix entry

A critical bug fix regarding adaptive ramp feed for helix entry was identified. The fix was intended for version 26.3 but was missed during the backport process. The group recognized this as a major bug affecting the release candidate and prioritized getting it merged immediately.

### Pull Request: Stepdown and single-pass operation logic

The group discussed a PR addressing the logic for single-pass operations (like engraving) versus multi-pass operations. The current behavior where setting stepdown to zero can be ambiguous was reviewed. The consensus was to normalize the approach: if a user wants a single pass, the interface should reflect that clearly, potentially by disabling irrelevant fields, while maintaining the ability to set multiple passes with specific stepdown values.

Links from the meeting chat:

- <https://github.com/FreeCAD/FreeCAD/pull/32925#issuecomment-7123515339>

### Pull Request: Generalizing the asset manager

A PR to generalize the CAM asset manager was discussed. This change would allow add-ons to register additional stores for machines and toolbits, moving away from a hard-coded two-store limit. This would enable features like synchronized cloud storage for CAM assets. The group supported the concept and agreed to merge it early in the 27.1 cycle to allow time for downstream integration.

### Simulation and probing demonstration

Billy demonstrated new capabilities in the CAM simulator, including the ability to manually jog the simulation via G-code in the Python console, perform in-process probing to reset work coordinates (G54), and check for out-of-tolerance cuts. The probing implementation includes support for various probe macros (e.g., Renishaw, Heidenhain) and a 'ProBasic' pseudocode layer.

### V-carve and tapered ball end mill demonstration

A prototype for replacing the V-carve operation was shown, featuring support for bottom clearing, rest machining, and the creation of inlay plugs. The demonstration included using tapered ball end mills to machine both the pocket and the corresponding plug.

### Community contributions and bug reports

gyordanvo reported on ongoing work to fix adaptive clearing issues, specifically regarding tool linking around bosses and helix entry feed rates. A bug was identified where rapid moves could inadvertently persist as feed moves due to modal G-code handling in post-processing. The group encouraged the contributor to submit their patches.

Links from the meeting chat:

- <https://github.com/FreeCAD/FreeCAD/pull/34582>

## Decisions

None recorded.

## Action items

None recorded.
