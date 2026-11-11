# FreeCAD BIM Meetup Notes — 29th September 2026

Attendees:

- [@Roy-043](https://github.com/Roy-043)
- [@semhustej](https://github.com/semhustej)
- [@markkomartin](https://github.com/markkomartin)
- [@marcuspollio](https://github.com/marcuspollio)

## Overview

The meeting focused on four main topics:

1. The `update IfcOpenShell` command status
2. Files testing suite for regressions and profiling
3. The BIM window refactor PR and complex objects refactors
4. Draft functionalities added into FreeCAD core or Part/PD modules

#### __1.__ `update IfcOpenShell` __command status__

@Roy-043 notes that the [update IfcOpenShell](https://wiki.freecad.org/BIM_Workbench#Utils) command [does not work](https://github.com/FreeCAD/FreeCAD/issues/20682) in AppImages. Given the current release schedules of both FreeCAD and IfcOpenShell (roughly 2-3 per year), and the current availability of the latter via pixi and distributions packages, the usefulness of the command is questioned. It is agreed to remove it soon.

**Decision:** A PR removing the `update IfcOpenShell` command is to be submitted for 27.1

#### __2. Files testing suite for regressions and profiling__

@marcuspollio suggests adding a “user/production” files testing suite to ease regressions detection and profiling performance. Complementary to unit testing, this suite would exercise usual operations users perform (opening, importing, exporting, recomputing, GUI interaction, etc.) with a wide range of file versions and objects.

@semhustej would like to help create this files suite. The versions 0.21, 1.0, 1.1, and 26.3 are suggested for inclusion, as well as a representative subset of objects created via different methods (baseless, Draft base, Sketch base, Part, STEP, mesh, etc).

**Decision:** @semhustej and @marcuspollio will clarify the need and scope for the testing files.

#### __3. BIM window refactor PR__

@yorikvanhavre’s [BIM window refactor PR](https://github.com/FreeCAD/FreeCAD/pull/19912) has been stale for almost two years. Some of this work is meaningful and would be great to keep in some way, even if just as an inspiration for another refactor.

A larger discussion about the [workflow of creating and editing windows](https://wiki.freecad.org/Arch_Window) points out the difficulties of choosing the appropriate method (e.g. base Draft, Sketch, Presets, custom components, custom types via other workbenches, etc), and the challenges of maintaining them all. The presets are seen as a quick and easy way to get started, but quickly limiting as well. Relying only on imported objects (e.g. STEP file from manufacturer) is not practical too.

Although not yet precisely defined, a growing consensus indicates that designing a generic method based on parametric assembly-like presets containing components, whose presets would serve as [shared types](https://standards.buildingsmart.org/IFC/DEV/IFC4_3/HTML/lexical/IfcBuiltElementType.html) (e.g. “family” in Revit) and which can be edited in other workbenches such as Part/PD, appears to be the most promising approach. This would allow for a small but representative set of types that would serve as templates for more advanced types, and would allow considerable freedom in the design of windows, whilst still enabling certain parameters/components to be edited on a per-instance basis. Taking advantage of tools provided by other workbenches would lower the need to implement specific tools in BIM to edit the geometry of such assembly-like types/objects.

No implementation or interface specifics have been defined at this stage. The use of [VarSets](https://wiki.freecad.org/Std_VarSet) and future [Variant Parts](https://github.com/FreeCAD/FreeCAD-Enhancement-Proposals/blob/master/FEPs/FEP-0010-variant-parts/README.md) by @[pieterhijma](https://github.com/pieterhijma) is mentioned, although their role or suitability has not yet been established.

**Decision:** All continue to investigate the potential and design of “complex” objects (e.g. windows, doors, stairs, roofs, curtain wall, railings/fence, etc) refactors, both from a workflow, interface, and implementation perspectives.

#### __4. Draft functionalities added into core and Part/PD__

@marcuspollio notes that since version 1.1, several functionalities initially found only in the Draft workbench have been reimplemented in FreeCAD Core (e.g. App, Gui) or other modules (e.g. Part):

- [Standard Transform](https://wiki.freecad.org/Std_TransformManip) in Core now has most of Draft Move, Rotate, Scale and Mirror, with some snapping, support for global, local, relative, and custom coordinate spaces. Standard Transform still lack the easy input points, keyboard/shortcut/accelerator, and copy/clone workflows, but that may be addressed soon.
- [Standard Annotation](https://wiki.freecad.org/Std_AnnotationLabel) in Core has some of [Draft Label](https://wiki.freecad.org/Draft_Label) features (most are lacking for now).
- [Part Pattern/Link Arrays](https://wiki.freecad.org/PartDesign_Workbench#Part_Design_Transformation_Features_toolbar) used in Part, PD, and Assembly mimic most of Draft Circular, Path, and Point Arrays with Links support. Twisted Path remains for now.
- Recent improvement to [Part Attachment](https://wiki.freecad.org/Part_EditAttachment) close some gaps with [Draft WorkingPlane](https://wiki.freecad.org/Draft_SelectPlane), but proxies and restoration of previous/next positions are not yet supported.

Discussions are currently underway to incorporate snapping, grid and layers-like features into Core. Consequently, the question of whether to maintain and keep these overlapping capabilities in Draft (once those in Core have the same features set) may arise.

No specific action is suggested, but it is recommended to monitor the situation, and possibly to take part in discussions regarding the integration of these features into Core/Part, so that certain aspects specific to BIM or Draft workflows are preserved.

**Decision:** None for now.

## Action items

- **@Roy-043:** Open issue or PR regarding the `update IfcOpenShell` command removal.
- **@semhustej & @marcuspollio:** Investigate and clarify testing files suite needs and scope.
- **All:** Continue to investigate the Window object and tool re-design as a tests-bed for “complex” objects refactors.
- **João:** Publish documentation describing the contextual-editing architecture.
- **João:** Publish the reorganized branch and provide test builds.
- **João:** Extract mature generic/core changes into separate reviewable PRs.
- **Group:** Test the contextual-editing branch and provide feedback on the workflow.
- **@marcuspollio:** Continue the BIM README work and add an initial terminology glossary.

## Next meeting

Likely follow-up topics:

- Review of the published contextual-editing architecture.
- Feedback from test builds.
- Integration strategy for the core and BIM-side changes.
- Contextual UI and edit-mode behavior.
- BIM terminology and release documentation.

## 
