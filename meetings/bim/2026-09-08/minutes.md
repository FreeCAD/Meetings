# FreeCAD BIM Meetup Notes — 8th September 2026

Attendees:

- [@Roy-043](https://github.com/Roy-043)
- [@maxwxyz](https://github.com/maxwxyz)
- [@semhustej](https://github.com/semhustej)
- [@tritao](https://github.com/tritao)
- [@markkomartin](https://github.com/markkomartin)
- [@marcuspollio](https://github.com/marcuspollio)

## Overview

The meeting focused primarily on the future technical direction of FreeCAD BIM, particularly IFC integration, the 2D documentation workflow, architectural cleanup of the BIM codebase, and coordination between contributors.

A recurring theme was the need to avoid developing parallel systems that solve the same problem. The group generally favored improving and reusing existing infrastructure where possible, while defining a clearer roadmap so contributors know which systems are expected to remain, evolve, or eventually be replaced.

#### __1. Summer of Code / mentoring__

There was a short discussion about mentoring and the availability of volunteers.

João noted that he has previous Summer of Code experience, including experience as a mentor, and would be open to mentoring again. However, he pointed out that the amount of mentoring effort depends heavily on how familiar the contributor already is with the project.

No specific mentoring assignment was decided during the meeting.

#### __2. IFC strategy and strict IFC mode__

A substantial part of the meeting focused on how deeply FreeCAD BIM should pursue native or “strict IFC” modeling.

There was concern that the current IFC implementation has become difficult to maintain. João has started reviewing and refactoring the IFC-related BIM code, with the goal of centralizing IFC functionality rather than having different parts of BIM interact with IfcOpenShell independently. He plans to make the work available as a draft PR for review.

The existing strict IFC workflow also has practical issues. Roy highlighted undo/transaction problems where conversion to strict IFC can occur outside the expected transaction, making some operations difficult to undo cleanly.

The broader question was whether maintaining a full strict IFC editing mode is worth the additional complexity. The emerging direction was:

- High-quality IFC import/export remains essential.
- IFC should continue to inform BIM semantics and data structures.
- FreeCAD does not necessarily need to constrain its native modeling workflow to IFC internally.
- Full native/strict IFC modeling should not consume disproportionate development effort in the short term.

Marcus and Tom both supported using the IFC schema as an important reference without making FreeCAD entirely dependent on its limitations. João proposed auditing how closely the current native BIM representation maps to IFC and looking for opportunities to simplify or unify the two.

Another issue is that IFC export and conversion into strict IFC currently follow different paths, which can lead to inconsistent behavior and additional maintenance. Unifying more of that infrastructure was seen as desirable.

#### __3. 2D documentation and the 3D → 2D workflow__

The group discussed 2D documentation as one of the most important areas for BIM improvement.

Producing a full drawing set from a BIM model is currently cumbersome, particularly when many pages, views, dimensions, and annotations are required. Marcus suggested that a medium-term goal should be to make the transition from the 3D BIM model to finished 2D documentation significantly easier.

Rather than building a completely separate BIM drawing engine, the discussion leaned toward making better use of TechDraw and improving the integration between BIM and TechDraw.

The desired workflow would be much more automated: users should ideally be able to create drawing views or sheets from BIM contexts with much less manual setup while preserving BIM-aware information such as dimensions, labels, sections, stories, and object semantics.

A longer-term idea was a more unified 2D/3D experience where users could move between modeling and documentation contexts without feeling that they had entered completely separate systems. Preset views, stories, filters, section planes, and contextual overlays could help provide the appropriate working environment with fewer manual steps.

João indicated that this could influence his current BIM 2D/plan work and agreed to think further about the approach before the next discussion.

#### __4. Roadmap and contributor coordination__

The group returned to the roadmap discussion from the previous meeting.

There appeared to be enough overlap between contributors' priorities to build a general roadmap. The roadmap should not only list desired features, but also show **who is working on what**, so contributors do not unknowingly duplicate work or develop systems that conflict with another planned change.

Roy again raised the example of several contributors independently working around the wall tool as the kind of situation better coordination should prevent.

The roadmap should therefore help answer questions such as:

- Which existing systems are expected to remain?
- Which areas are being actively redesigned?
- Who is currently working on each area?
- Where can contributors collaborate instead of producing competing implementations?
- Which legacy systems are expected to be replaced, and on what timescale?

#### __5. BIM architecture and core-object refactoring__

João identified architectural cleanup as another important part of the roadmap.

Several core BIM objects, including major building elements such as walls and windows, currently contain a large amount of tightly coupled logic. The discussion described these objects as too monolithic and difficult to extend or maintain.

A possible direction would be to separate responsibilities more clearly: geometry/calculation code, object behavior, and user-interface code should not all be intertwined in the same implementation.

Marcus agreed with the need for refactoring, while emphasizing that any new architecture should still provide the extension points and hooks required by other contributors and add-ons.

#### __6. Existing tools vs. replacement tools__

An important roadmap question is how much effort should continue going into existing Draft/BIM systems when newer approaches are being explored.

Roy specifically raised current problems with BIM/Draft-generated views, including text and dimension rendering, and questioned whether it makes sense to spend significant effort improving them if another system may replace them relatively soon.

The group did not make a final decision. Tom suggested leaving the question open until João has investigated the alternatives further, because it is important not to spend substantial development time on functionality that could become obsolete shortly afterward.

João's general preference was to improve reusable Draft APIs and integrate new functionality into existing infrastructure where practical rather than continually introducing replacements alongside old tools.

#### __7. Stair designer and integrating large contributions__

The new stair-design functionality was used as an example of a broader integration problem.

Large new contributions can contain substantial improvements, but they become difficult to merge when they duplicate an existing tool instead of extending or replacing it through a coordinated migration.

The preferred direction discussed was to see whether the new stair functionality could be unified with the existing stair system so FreeCAD does not end up maintaining two competing implementations.

João offered to investigate/refactor the integration and suggested that the same principle should guide future work on other major BIM objects such as windows, doors, roofs, and similar tools.

The discussion also touched on AI-assisted development. The group acknowledged that AI can enable contributors to produce much larger changes quickly, which makes architectural review and integration strategy even more important.

There was also recognition of the human side of code review: maintainers need to give necessary architectural feedback without unnecessarily discouraging contributors who have invested significant effort.

#### __8. Current release priorities__

Before closing, Marcus asked whether there were particular PRs or issues that needed focused attention during the coming week.

A large design/stair-related contribution was identified as a possible candidate for the current release. The release cutoff discussed in the meeting was **September 30**.

João agreed to take another look at the contribution. At the same time, Marcus cautioned against rushing a large architectural change simply to meet the release deadline.

The priority is therefore to determine whether the work can be integrated cleanly rather than treating the release deadline as a requirement to merge it.

#### __9. Meeting notes and agenda organization__

The group also discussed how future agendas and meeting notes should be stored.

A practical model would be to keep a **rolling agenda** where anyone can add topics, while storing each meeting's finalized notes separately.

Possible storage options included FreeCAD's Nextcloud or a repository. Existing FreeCAD developer and FPA meetings were mentioned as examples of keeping meeting minutes in repositories. No final storage location was selected.

The meeting itself used a new simplified transcription prototype from João. If it proves useful, João said he would document the command-line tool so others can use it.

For the agenda, the preference remained informal: contributors can simply add subjects to the rolling list when there is something they want discussed.

## Action items

- **João:** Continue the IFC code cleanup and prepare a draft PR for review.
- **João:** Audit how the native BIM representation relates to IFC and investigate opportunities to unify the IFC/export infrastructure.
- **João:** Investigate the longer-term 2D documentation architecture and how it relates to his current BIM 2D/plan work.
- **Marcus:** Post additional reasoning around the proposed 2D/3D workflow.
- **Contributors:** Develop the BIM roadmap with enough detail to show both priorities and who is working on each area.
- **João:** Continue restructuring/refining his larger BIM work into pieces that are easier to review and integrate.
- **João:** Revisit the stair/design-tool contribution and investigate how it could integrate with the existing tool rather than becoming a parallel implementation.
- **Group:** Keep the future of the existing Draft/BIM 2D view system open until the replacement/integration direction is clearer.
- **Meeting organizers:** Continue with a rolling agenda and establish a place for separate per-meeting notes.
- **João:** Document the new transcription tool if the prototype proves successful.

## Next meeting

Likely follow-up topics include:

- Results of the IFC architecture audit/refactoring
- Further discussion of the 2D/3D documentation workflow
- Progress on the BIM roadmap and contributor coordination
- Review/integration strategy for the stair-design contribution
- Decisions about which existing BIM/Draft systems should be improved versus gradually replaced

## 
