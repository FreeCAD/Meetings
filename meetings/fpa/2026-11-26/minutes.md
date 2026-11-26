# FPA Meetup: 2026-11-26

> Crow, an automated notetaker, made these minutes. They may contain mistakes or inaccuracies and are for reference only.
>
> Model: Qwen/Qwen3.5-397B-A17B-FP8  
> Source code: <https://github.com/FreeCAD/Meetings/tree/main/bot>

## Attendees

- Pieter
- Jackson Oursland
- Frank (mnesarco)
- shai
- reqrefusion
- Alexandre
- Billy (aka Connor)

## Topics

### Meeting status and attendance

Participants noted that key members (Yorik, Brett) were absent and chat messages indicated the meeting might be cancelled. However, those present proceeded to discuss urgent technical issues and project updates.

### OCCT 8.02 integration and package management security

The integration of OCCT 8.02 was confirmed as the new standard, allowing for the closure of many existing crash reports. The discussion shifted to security concerns regarding AI-generated code in package managers like Conda. It was noted that while AI could theoretically introduce backdoors, the current supply chain relies heavily on trust regardless of the source. The Conda Forge process involves automated PRs for version bumps which often require manual patching to fit the ecosystem.

### Expression quantity and unit parser issues

A critical issue regarding expression quantities and units was raised, described as a regression from a localization fix that threatens the stability of the upcoming release. The current parser is legacy code with ambiguous behavior. Proposals included creating a comprehensive test set (potentially AI-generated) to define the desired language behavior, and potentially rewriting the parser using a memoizing PEG approach with a unified grammar. Concerns were raised about backward compatibility with existing documents storing expressions verbatim. Suggestions were made to store an intermediate representation in the file format to decouple the user interface from the stored data, possibly requiring a new file format for future projects.

### Open source CAD ecosystem and licensing

The group discussed the emergence of new open-source CAD projects like SolidCraft and the movement of contributors between projects. Concerns about AI-generated code being placed in the public domain were addressed; it was clarified that existing projects use licenses like Apache 2.0 and MIT, which require attribution and source availability. The group noted that large commercial entities adopting an 'AI-first' strategy could pose a competitive threat, but also that users are seeking alternatives to proprietary software due to pricing and AI policies.

Links from the meeting chat:

- <https://github.com/tangency-labs/solidcraft/graphs/contributors?from=2026-08-21T22%3A00%3A00.000Z>

### AI-assisted Addon development policies

Frank reported on the influx of AI-generated addons and his creation of a 'skill' or instruction set to guide AI agents in following FreeCAD best practices, as many generated addons previously used poor patterns. Jackson supported the idea of formalizing such rules to ensure compliance, though it was noted this is a maintainer decision rather than an FPA decision.

### CAM Workbench simulator and Dexel engine demonstration

Billy demonstrated a new CAM simulator featuring a custom-written Dexel (depth pixel) engine, which offers better performance for complex simulations compared to the older CSG-based approach. The demo included multi-axis machining, in-process probing, work holding setups (vises, parallels), and the ability to machine soft jaws in a two-operation process. The Dexel engine allows for variable density based on tool size and supports exporting the simulated cut stock as a solid. Billy noted that the codebase is large and will be submitted via multiple pull requests over the coming months, targeting inclusion in version 27.1.

## Decisions

None recorded.

## Action items

None recorded.
