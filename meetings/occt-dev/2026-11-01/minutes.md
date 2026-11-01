# OCCT Dev Meeting: 2026-11-01

> Crow, an automated notetaker, made these minutes. They may contain mistakes or inaccuracies and are for reference only.
>
> Model: Qwen/Qwen3.5-397B-A17B-FP8  
> Source code: <https://github.com/FreeCAD/Meetings/tree/main/bot>

## Attendees

- hyarion
- Dmitrii/@dpasukhi
- Pieter
- GeeBee
- caio-venancio

## Topics

### Meeting logistics and recording

Participants discussed the automatic recording of the meeting by an AI notetaker, noting that previous meetings in the series had also been recorded and summarized in GitHub repositories. The recording setup was attributed to a third party, not the current attendees.

### OCCT fillet operations and legacy code structure

The group discussed recent changes in OCCT regarding minimum angle thresholds for fillet operations, which have been removed. The conversation covered the age of the fillet and chamfer algorithms, noting they are among the oldest parts of the codebase and rely on empirical functions rather than modern classes. The unusual file naming convention (e.g., file_0, file_1) was explained as a legacy template system predating C++ templates.

### Exception handling in OCCT

Discussion arose regarding why OCCT does not inherit all exceptions from standard C++ exceptions. It was clarified that while there are flags to disable certain debug checks (like out-of-bounds), these do not eliminate all exceptions. The behavior is controlled by macros within specific container definitions, and the system remains complex due to the legacy nature of the codebase.

### Proposal for law-based symbolic geometry in OCCT

hyarion presented a concept and implementation for adding user-created parametric shapes to OCCT using symbolic, law-based geometry defined by expressions rather than new C++ classes per shape. The proposal aims to solve precision issues with shapes like helices, which currently degrade to B-spline approximations during operations like meshing or Booleans. The approach uses a Directed Acyclic Graph (DAG) of immutable nodes to evaluate expressions, derivatives, and bounds efficiently. Examples demonstrated included exact helices, squircles, Trefoil surfaces, and ocean wave simulations, showing improved precision and smaller file sizes compared to NURBS approximations. The implementation currently consists of approximately 48,000 lines of code, including tests and serialization logic.

### OCCT development direction: GeomEval and B-Rep Graph

Dmitrii/@dpasukhi confirmed that the proposed law-based approach aligns with his ongoing work on 'GeomEval,' an intermediate representation intended to reduce approximation errors for trigonometric laws (like helices). He noted challenges in implementing full serialization and handling continuity gaps between derivatives. The discussion also covered the 'B-Rep Graph' project, which is currently undergoing significant redesign to remove C-matches and improve sustainability, resulting in a codebase exceeding 120,000 lines. It was agreed that serialization could potentially be handled via a new binary format (using FlatBuffers) rather than the traditional BREP format, though the B-Rep Graph is not yet ready for release in OCCT 8.

## Decisions

None recorded.

## Action items

None recorded.

---

A moderator removed the notetaker from the meeting before the end. These minutes contain only the part of the meeting before that time.
