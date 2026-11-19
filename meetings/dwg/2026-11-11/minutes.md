# DWG Meetup: 2026-11-11

> Crow, an automated notetaker, made these minutes. They may contain mistakes or inaccuracies and are for reference only.
>
> Model: Qwen/Qwen3.5-397B-A17B-FP8  
> Source code: <https://github.com/FreeCAD/Meetings/tree/main/bot>

## Attendees

- Max
- creymore
- pierreporte

## Topics

### Unified library system for FreeCAD

The participants discussed the need for a unified library system in FreeCAD to consolidate libraries currently scattered across the BIM workbench, CAM workbench, and various add-ons. The discussion covered the necessity of 'pack and go' functionality to ensure projects work consistently across different computers and the potential integration with the Addon Manager. It was noted that previous attempts to find developers interested in implementing such a system at developer meetings had been unsuccessful.

### UI layout and tablet panels

The group discussed proposals for reorganizing the FreeCAD interface using tabs or 'tablet panels,' similar to the vertical tab bars in SOLIDWORKS or the panel systems in NX. Suggestions included placing these panels on the left (replacing or augmenting the tree view) or on the right side of the screen. The conversation compared how different CAD applications handle task panels, properties, and workbench-specific tools, with some participants expressing concern that constant tab switching could be annoying for users. Screenshots of SOLIDWORKS and NX were shared to illustrate different approaches to UI organization.

Links from the meeting chat:

- <https://github.com/FreeCAD/FreeCAD/issues/12814>
- <https://www.eassistant.eu/fileadmin/user_upload/eAssistant_EN/CAD_PlugIns/SOLIDWORKS/SW_CylGear_with_SplinedHub.png>
- <https://develop3d.com/wp-content/uploads/2021/03/Screenshot-2021-03-02-at-11.12.31.jpg>
- <https://blogs.sw.siemens.com/wp-content/uploads/sites/2/2024/08/NX-Process-Model-1024x576.png>

### Comparison with NX and SOLIDWORKS workflows

A detailed comparison was made between FreeCAD's current workflow and those of NX and SOLIDWORKS. Topics included how NX handles applications (similar to workbenches), construction groups, and the separation of modeling, assembly, and drawing into different contexts or files. The participants examined how NX manages library components, parameters, and variants, as well as its approach to material assignment and selection filters. The complexity and cost of commercial solutions like NX were contrasted with FreeCAD's flexibility.

### Assembly structure and Part containers

The discussion turned to the structure of assemblies in FreeCAD, specifically the practice of allowing Body objects to be placed directly into Assembly containers. It was proposed that to enforce better order, the software should prevent Bodies from being added directly to assemblies, requiring them to be wrapped in Part containers instead. Suggestions included modifying the 'New Body' command to automatically create a Part container or checking for an active Part container before creation. The group acknowledged the need to maintain backward compatibility for existing files while guiding new users toward a more structured workflow.

### Future meeting format

Towards the end of the meeting, the participants suggested a format for future DWG Meetups. It was proposed that the group could review specific open issues and pull requests, particularly those marked for UI review, discussing one or two items per meeting to make progress on the backlog.

## Decisions

None recorded.

## Action items

- **Max:** Look through the Discord thread regarding the internal comprehensive library to review previous discussions.
