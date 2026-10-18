# OCCT Dev Meeting: 2026-10-18

> Crow, an automated notetaker, made these minutes. They may contain mistakes or inaccuracies and are for reference only.
>
> Model: Qwen/Qwen3.5-397B-A17B-FP8  
> Source code: <https://github.com/FreeCAD/Meetings/tree/main/bot>

## Attendees

- Pieter
- Jackson Oursland
- Chris Hennes (@chennes)
- 3
- GeeBee
- Dmitrii/@dpasukhi

## Topics

### Jitsi meeting limits

Participants noted that Jitsi now imposes a 95-minute limit on meetings and discussed potential future changes.

### OCCT 8.0.2 release status

Dmitrii reported on the progress of the OCCT 8.0.2 release. He is currently fixing bugs in the master branch, noting that fixing one bug often reveals others. Once the master branch is stable, he plans to backport patches to create the 8.0.2 release. He mentioned that the Experimental Release (ER) branch is currently unstable due to ongoing changes.

### Data exchange plugin architecture

The group discussed how to implement data exchange plugins for FreeCAD using OCCT. Chris explained that FreeCAD add-ons are primarily Python-based. To include compiled code (such as OCCT plugins or proprietary DLLs), developers should create a Python wheel published on PyPI. The Addon Manager can install these wheels. FreeCAD has a Python API for registering importable and exportable file formats. Dmitrii intends to create a loader mechanism in Python that can dynamically load necessary DLLs at runtime. The add-on would be categorized under 'Other' in the Addon Manager.

Links from the meeting chat:

- <https://freecad.github.io/Addon-Academy/>

### Python bindings for OCCT

Jackson reported that removing `pythonocc-core` from FreeCAD packages version 26.3 has broken some add-ons. He asked about the status of an official OCCT Python binding. Dmitrii clarified that an official wrapper is postponed for at least six months due to resource constraints. Furthermore, the planned official wrapper will have a different API logic compared to existing bindings like `OCP` (used by CadQuery) or `pythonocc`, making it unsuitable as a direct replacement. The consensus was to direct users to CadQuery/OCP where possible, as the CadQuery maintainer is responsive to OCCT updates, whereas `pythonocc` updates are slow and lack a PyPI package.

### Fillet and crash issue reporting

Pieter and GeeBee discussed the reporting of fillet issues and crashes. Dmitrii requested that crash reports be prioritized and clearly labeled (e.g., including 'crash' in the issue title) to help identify them quickly. He advised against testing on the unstable ER branch for now but encouraged testing on the master branch once upcoming fillet fixes are merged in the next few days. GeeBee asked about co-edges and the B-Rep graph; Dmitrii explained that co-edges have always existed in OCCT but were previously disconnected from faces, a problem being addressed in the B-Rep graph rework which is currently under development.

Links from the meeting chat:

- <https://wiki.freecad.org/Compile_with_OCCT>

### Automated meeting minutes

Chris explained that an automated AI bot named 'Crow' attends FreeCAD meetings to generate transcripts and draft minutes via a pull request to the FreeCAD/Meetings repository.

Links from the meeting chat:

- <https://github.com/FreeCAD/Meetings/>
- <https://github.com/FreeCAD/Meetings/pull/5>

### Security advisory

Chris mentioned a security issue regarding compromised emails and a pending security advisory. He stated he will make the advisory public once the relevant pull requests to fix the vulnerability are merged.

## Decisions

None recorded.

## Action items

- **Dmitrii/@dpasukhi:** Update contribution guidelines (CONTRIBUTING.md and README.md) to specify that pull requests requiring full rewrites should be converted to issue reports, while simple ones may be merged.
- **Chris Hennes (@chennes):** Send information about the Rust-based dependency in FreeCAD's libpack to Dmitrii.
- **Pieter:** Prioritize reporting crash issues over fillet-specific issues and include the word 'crash' in the issue titles.
- **Dmitrii/@dpasukhi:** Merge pending fillet fixes into the master branch within the next few days. *(review)*
