# OCCT Dev Meeting: 2026-11-22

> Crow, an automated notetaker, made these minutes. They may contain mistakes or inaccuracies and are for reference only.
>
> Model: Qwen/Qwen3.5-397B-A17B-FP8  
> Source code: <https://github.com/FreeCAD/Meetings/tree/main/bot>

## Attendees

- Pieter
- Jackson Oursland
- Dmitrii/@dpasukhi
- GeeBee

## Topics

### OCCT 8.0.2 Release Status

Dmitrii reported on the complexity of the recent OCCT 8.0.2 release, which involved extracting 35 patches from larger previous patches. The release includes fixes for crashes reported via Discord and contributions from approximately six external contributors, including individuals from ASML. The release notes cover improvements to fillets, lofts, and other features. Dmitrii noted that while there are behavioral differences regarding continuity detection (G1/C1), there were no significant regressions.

### Conda-Forge OCCT Update

Jackson Oursland discussed the process of updating the OCCT package on Conda-Forge to version 8.0.2. He explained the pinning mechanism used in the ecosystem, noting that while other packages are pinned to 8.0.1, the OCCT package itself builds the new version. A site-wide migration will be required to update all dependent packages, which Jackson will coordinate. Dmitrii pointed out that the pull request description still referenced the old Git repository URL, which Jackson agreed to correct.

Links from the meeting chat:

- <https://github.com/conda-forge/occt-feedstock/pull/149>

### AI-Generated Code and MitCAD Patches

The group discussed patches submitted by the MitCAD project, which appear to be largely AI-generated. Dmitrii expressed concerns about the code quality, excessive and meaningless comments, and potential copyright conflicts if the code was derived from existing proprietary or LGPL sources without proper attribution. He noted that the patches are highly specific and often introduce workarounds rather than robust solutions. The discussion highlighted the risks of accepting AI-generated contributions without human verification of the logic and origin, citing a previous incident where AI inadvertently replicated copyrighted function signatures.

Links from the meeting chat:

- <https://github.com/mitcad/Mitcad/tree/main/third_party/vcpkg-ports/opencascade>
- <https://github.com/mitcad/Mitcad/blob/main/third_party/vcpkg-ports/opencascade/0016-chfi3d-rounding-rolls-on-anothers-contact-line.patch>

### GitHub Permissions and Issue Triage

Dmitrii proposed adjusting GitHub repository permissions to delegate issue triage tasks. He suggested granting 'reporter' roles to active community members, allowing them to apply labels without having merge permissions. Jackson explained the available GitHub roles (Administrator, Maintainer, Developer, Reporter) and suggested using an `agents.md` file to guide AI agents in filing better issue reports. Dmitrii expressed hesitation about granting write permissions to AI agents but agreed to organize human reporters better.

### Priorities for Upcoming OCCT Development

Pieter asked for guidance on how to best utilize his time as an OCCT liaison funded by the FPA. Dmitrii requested a focus on reporting and reproducing crashes, as these are critical and often easier to fix than feature requests. Dmitrii also warned of upcoming foundational changes between the current version and the New Year, including the removal of global static variables for tolerances and naming, which will alter behavior for users relying on those settings.

### CAD Kernel Benchmarking

Jackson shared results from the 'CAD Acid Tests,' a benchmark suite of difficult geometric operations. The results show that while FreeCAD (using OCCT) performs reasonably well, it trails behind commercial kernels like those in Fusion 360 and SolidWorks. The group noted that MitCAD's patched version of OCCT did not outperform the standard release in these tests. Dmitrii commented that MitCAD's patches are often too specific to be generally beneficial.

Links from the meeting chat:

- <https://claude.ai/artifact/DndjnYeLa8dFYe8QD8kbYt>
- <https://github.com/theironchef/cad-acid-tests/tree/main>

## Decisions

None recorded.

## Action items

- **Jackson Oursland:** Update the Conda-Forge OCCT feedstock PR to reference the correct GitHub URL instead of the old Git repository link.
- **Jackson Oursland:** Prepare a PR to update the OCCT package on Conda-Forge to version 8.0.2 and coordinate the site-wide migration of dependent packages.
- **Pieter:** Focus on identifying and reporting OCCT crashes to assist with the next release cycle.
- **Dmitrii/@dpasukhi:** Assign 'reporter' roles on the OCCT GitHub repository to active community members to help with issue labeling and triage.
