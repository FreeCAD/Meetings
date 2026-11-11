# FreeCAD BIM Meetup Notes — 15th September 2026

Attendees:

- [@Roy-043](https://github.com/Roy-043)
- [@semhustej](https://github.com/semhustej)
- [@tritao](https://github.com/tritao)
- [@markkomartin](https://github.com/markkomartin)
- [@furgo16](https://github.com/furgo16/)
- [@sliptonic](https://github.com/sliptonic)

## Overview

The meeting focused primarily on João's ongoing BIM contextual-editing work, the desired relationship between 2D and 3D editing, how architectural drawings and annotations should fit into the workflow, and how BIM contributors can coordinate around a shared roadmap.

A recurring theme was that the new 2D workflow should not become an isolated alternative to normal FreeCAD modeling. The preferred direction is a more unified experience where the same BIM objects can be edited from either 2D or 3D views, while view-specific information such as dimensions and annotations can remain associated with the appropriate drawing context.

The group also discussed how to expose these workflows in the UI, how to make large experimental changes available for testing, and how to organize development around a small number of collective objectives rather than a rigid long-term roadmap.

#### __1. Contextual editing and view definitions__

João presented the current state of his plan-edit work, which has evolved into a more general **contextual editing** architecture.

The original implementation was heavily specialized around BIM plan editing and implemented largely in Python. During the rework, João identified a more fundamental problem: visual state such as a footprint representation should not be tied only to a single object's view provider if FreeCAD is expected to support multiple concurrent views with different representations.

To address this, he has been working on a lower-level concept of a **view definition**. The intention is for different FreeCAD views to be able to display the same underlying model using different representations without one view unintentionally changing the others.

On top of this foundation, BIM can provide contextual editing behavior separately from the individual BIM objects themselves. Rather than every wall, space, or other BIM object needing to know how to edit itself in each possible context, the BIM workbench can provide the relevant editing behavior for the active view or operation.

The architecture is still under active development and is not yet back to the level of polish of the earlier prototype. João said he needs to retest the basic functionality from scratch and expects to have a more useful demonstration soon.

#### __2. Unified 2D and 3D editing__

A major part of the discussion concerned whether 2D editing should be treated as a separate workflow or as another view onto the same BIM model.

João clarified that the goal is the latter. Suitable BIM operations should eventually work from both 2D and 3D views. A user could work on a plan, switch to a 3D view, and continue manipulating the same walls and other building elements without changing modeling systems.

David considered seamless switching particularly important. He noted that different people may naturally prefer different representations: some architects work primarily in 2D while other FreeCAD users are accustomed to manipulating models in 3D.

Tom supported the same direction and compared it to workflows where architectural objects can be edited in essentially the same way from a plan or from a 3D representation.

The existing FreeCAD workflows are not intended to disappear as a result of the new system. João described contextual editing as an addition, although there are still open questions about which editing interaction should become the primary one when, for example, a wall is selected in a 3D view.

Possible future interactions include showing contextual editing handles directly on the selected object instead of requiring the user to invoke separate Draft/BIM commands.

The exact editing UX therefore remains an open design question, but there was broad support for keeping 2D and 3D editing closely connected.

#### __3. Testing and incremental integration__

The contextual-editing work has become a very large development branch. João estimated that breaking it down naïvely could result in dozens of pull requests, so finding the right review granularity is itself a challenge.

David recommended providing pre-built versions for testers who do not normally compile FreeCAD. He noted that this had been valuable on previous large experimental changes because it allowed a much broader group of users to provide practical feedback.

João agreed and plans to provide builds once the implementation is sufficiently usable. He expects the development to take more than a single week before everything is ready for wider testing.

Roy also cautioned that the feature is too large to expect the whole system to land in the next release.

João agreed that it does not need to merge all at once. The architecture is being structured so that foundational pieces and native infrastructure can be reviewed and merged progressively before the full contextual-editing experience is complete.

The general direction is therefore:

- Break the work into understandable foundational pieces.
- Make experimental builds available for user testing.
- Gather feedback before committing to later UI decisions.
- Merge the architecture progressively instead of treating the feature as one monolithic change.

#### __4. Task panel and contextual UI__

The group discussed where contextual BIM commands should appear in the interface.

João is not fully satisfied with putting every operation into the task panel. For operations such as joining two walls, a command located close to the objects or in a view-specific contextual toolbar could potentially be easier to discover than an option in a distant panel.

At the same time, duplicating the entire BIM toolbar inside every plan view would create another form of clutter. João has experimented with temporary or view-specific toolbars containing only commands relevant to the current context, but FreeCAD does not currently provide exactly this behavior out of the box.

For the initial implementation, the group favored avoiding premature UI redesign. The current task-panel implementation is functional, and Tom suggested that contributors first test this simpler version and provide feedback based on actual use.

João agreed to keep the task panel for the first iteration and revisit a more contextual toolbar or in-view interface later.

This lets the group evaluate the editing model itself before investing heavily in a new interaction system.

#### __5. TechDraw and automated architectural drawings__

The discussion then returned to the longer-term 3D-to-2D documentation workflow.

João noted that much of the infrastructure being developed for contextual views could potentially be reused for **TechDraw integration**. Once the first contextual-editing iteration is available for testing, he plans to investigate this more closely.

A possible direction is to automate the creation of architectural plans, sections, and elevations and make them usable as TechDraw documents rather than requiring users to assemble every drawing manually.

This would build on the same underlying view infrastructure rather than creating an unrelated BIM drawing system.

The larger unanswered question is how annotations, dimensions, labels, and similar documentation elements should fit into this architecture.

#### __6. Dimensions and view-specific annotations__

Roy and Tom emphasized that architectural documentation involves more than simply generating geometry.

Dimensions, labels, window marks, annotations, and similar information have behavior that is specific to drawings. Repeated or similar building units may require similar annotation sets, while different drawings of the same model may need different information.

Tom described a workflow influenced by Revit in which there is a distinction between:

- The physical BIM model — walls, windows, slabs, and other things representing real building elements.
- Annotation objects — dimensions, text, detail lines, and other documentation that belongs to a particular view rather than to the physical building itself.

Under this approach, a dimension created for one floor plan would be visible when working in that plan but would not clutter the main 3D model or unrelated views.

João suggested that existing Draft dimensions and related objects may be reusable if their visibility can be controlled appropriately. Draft layers or a similar view-specific visibility mechanism might provide part of the solution.

The discussion generally favored view-specific annotations as the primary architectural workflow, while still allowing other kinds of dimensions or annotations to exist directly in 3D when appropriate.

No final technical architecture was selected, and João said he needs to investigate how this should interact with TechDraw and the new view infrastructure.

#### __7. BIM project navigation and the BIM Views Manager__

The discussion of view-specific annotations led into the question of how users should navigate a BIM project.

Tom suggested that plan views, elevations, sections, levels, and sheets should be presented through a BIM-oriented project/navigation interface rather than forcing users to find everything in the complete FreeCAD model tree.

João noted that he had already prototyped something similar several months earlier, tentatively described as a BIM project view. He plans to revisit that work.

There was broad agreement that the normal model tree and a BIM project navigator serve different purposes:

- The normal model tree exposes detailed document structure and remains useful when users need full access to the model.
- A BIM-oriented project view can provide a curated architectural structure focused on levels, views, drawings, and sheets.

This becomes especially important on larger projects, where implementation objects and drawing-related objects can make the complete document tree increasingly difficult to navigate.

David did not consider the existing BIM Views Manager ideal, particularly because of UI integration issues, but acknowledged that it contains useful functionality that should not simply be discarded.

The current direction is therefore to review the useful features of the existing BIM Views Manager and João's earlier prototype, then decide whether the existing manager should evolve, be replaced, or provide functionality to a new project-oriented panel.

João plans to revisit the implementation and continue the discussion at the next meeting.

#### __8. Collective BIM roadmap__

The final major topic was how to turn contributors' individual plans into a useful collective BIM roadmap.

Roy returned to the issue raised in previous meetings: different contributors have their own ideas and areas of work, but FreeCAD BIM has not traditionally organized these into a shared development effort.

David argued that the group should avoid trying to create a detailed year-long roadmap. The project changes too quickly for such a plan to remain reliable.

Instead, he proposed identifying **one or two shared objectives** that contributors can collectively move toward while still allowing individuals to work on their own interests.

Possible objectives mentioned included improving IFC import/export and continuing the broader 2D/documentation work, although no final set of priorities was chosen during this meeting.

The intention is to use the current momentum around BIM development and these regular meetings to create enough shared direction that individual contributions reinforce rather than conflict with one another.

David suggested using a future meeting to converge on those first collective objectives.

#### __9. Lessons from the CAM roadmap__

Brad/sliiptonic joined near the end of the meeting and described how similar coordination has helped FreeCAD CAM development.

He emphasized that a roadmap cannot dictate exactly what an open-source project will do. Instead, the CAM team found value in grouping related problems together and treating them as larger areas of work rather than isolated issues.

For example, related issues can be tagged or organized into an epic and approached as one design problem. This makes it possible to recognize that several apparent bugs may actually be symptoms of one underlying workflow that should be redesigned.

The CAM project also keeps roadmap-related documents in the source tree and records architectural decisions.

One particularly useful document has been a **ubiquitous language** or glossary defining what important project terms mean. Clarifying terms makes discussions easier for contributors and also improves the quality of AI-assisted development by reducing ambiguity about concepts.

Brad suggested that BIM could benefit from a similar approach and offered maintainer help if needed.

## Action items

- **João:** Continue the contextual-editing rework and retest the basic functionality.
- **João:** Prepare a more usable contextual-editing demonstration for a future meeting.
- **João:** Structure the large development branch so foundational pieces can be reviewed and merged progressively.
- **João:** Provide test builds once the contextual-editing implementation is sufficiently stable for wider feedback.
- **Group:** Test the initial task-panel-based contextual-editing interface before deciding whether view-specific toolbars or other contextual UI should replace it.
- **João:** Investigate TechDraw integration and more automated generation of plans, sections, elevations, and architectural drawings once the first contextual-editing iteration is available.
- **João:** Investigate how view-specific dimensions and annotations should interact with the new view architecture, Draft objects, and TechDraw.
- **João:** Revisit the previous BIM project/BIM Views Manager prototype and review the useful functionality of the existing BIM Views Manager.
- **David:** Put his thoughts about collective BIM objectives/roadmap priorities into writing.
- **Group:** Use a future meeting to converge on one or two near-term collective BIM objectives rather than attempting to define a rigid long-term roadmap.
- **Group:** Consider organizing related BIM issues into larger roadmap themes or epics rather than treating each issue independently.
- **Group:** Consider maintaining roadmap/architecture documents and a shared BIM terminology glossary in the source tree.
- **Brad/sliiptonic:** Available to help from the maintainer side if support is needed to make the roadmap/coordination process work effectively.

## Next meeting

Likely follow-up topics include:

- Demonstration and testing status of the new contextual-editing workflow.
- Feedback on the initial task-panel UI.
- Further design of seamless 2D/3D BIM editing.
- TechDraw integration and automated architectural drawing generation.
- How dimensions and other annotations should be scoped to individual views.
- Review of the BIM project/BIM Views Manager approach.
- Selection of one or two shared BIM roadmap objectives.
- Possible adoption of roadmap epics, architecture-decision documents, and a common BIM terminology glossary.

## 
