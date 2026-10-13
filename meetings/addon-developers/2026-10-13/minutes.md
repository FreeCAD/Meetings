# Addon Developer Meetup: 2026-10-13

## Attendees

- Frank (mnesarco)
- John ( PhoneDroid )

## Topics

### FreeCAD Launcher demonstration and status

Frank demonstrated the FreeCAD Launcher, a tool for managing multiple FreeCAD versions (stable, weekly, release candidate) and local installations. The launcher allows users to create profiles combining specific FreeCAD versions with sets of add-ons, macros, and Python packages. These profiles can be backed up, restored, and launched directly. The tool is currently available for Linux and Windows, with a Mac version technically compatible but untested due to lack of hardware and signing requirements. Frank noted that the project is intentionally minimal in scope, focusing solely on launching and configuration rather than file or project management.

Links from the meeting chat:

- <https://github.com/mnesarco/FreeCAD-Launcher/releases/tag/v0.4.11>

### Launcher feature requests and UI improvements

John provided feedback on the launcher interface. He suggested allowing users to customize profile avatars, either by uploading images or selecting from a preset library, and caching these icons locally to prevent broken links. He also proposed changing the add-on selection dialog from a single-column list to a multi-column grid to better utilize screen space and improve visual identification of add-ons. Additionally, he recommended adding a 'minimize to tray' function so the launcher can run in the background, and improving the visual feedback during add-on installation to make the process more obvious to the user.

### Branding and logo usage guidelines

The participants discussed the use of the FreeCAD logo within the launcher. Frank expressed uncertainty about using the official colorful logo versus a modified version, given that the launcher is a community project and not an official FreeCAD product. John referenced the Developer Handbook design guidelines, which specify how the logo and brand colors should be used by third parties. They agreed that Frank should seek clarification or permission from the project council or administrators to ensure compliance.

Links from the meeting chat:

- <https://freecad.github.io/DevelopersHandbook/designguide/logo>

### Distribution channels and packaging

Frank and John discussed distribution methods for the launcher. Frank confirmed he would not pursue Snap packages or system-level Debian files, preferring to maintain AppImage and potentially add Flatpak support for automatic updates on Linux. He noted that the Windows version works but lacks a digital signature, triggering security warnings, while the Mac version faces significant hurdles regarding code signing and notarization without a paid developer account. John suggested looking into Flatpak packaging utilities to simplify the process.

### Community promotion and communication

John suggested that the launcher needs more visibility, proposing a dedicated channel on the FreeCAD Discord server for user questions and discussion, as well as a blog post on the official website. Frank agreed to contact the blog author to request coverage and to ask Discord administrators about creating a dedicated channel. They noted that current awareness is low, with few user reports outside of specific Windows permission issues.

### Add-on ecosystem health dashboard

Frank presented a dashboard he developed to analyze the health of the add-on ecosystem. The tool tracks static analysis issues, dependency usage, and trends in add-on quality over time, highlighting which add-ons are improving and which are accumulating errors. Frank explained that the report is currently public but not widely promoted, as he is still refining the metrics and removing confusing elements, such as false positives caused by add-on index changes. The dashboard reveals that PySide and matplotlib are the most common external dependencies.

### Pull request review bottlenecks and project governance

John raised concerns about his pending pull requests and a discussion regarding workflow skip labels that have received no response from maintainers. The conversation expanded to a broader critique of the project's reliance on volunteers, noting that maintainers often prioritize features they personally need while neglecting reviews for modules they are unfamiliar with. Both participants acknowledged the difficulty of reviewing complex code without domain expertise. John suggested that the project should consider hiring dedicated staff for triage and merging to resolve the backlog, while Frank noted that previous grant efforts have not fully solved the issue of contributors losing interest due to long wait times.

Links from the meeting chat:

- <https://github.com/FreeCAD/FreeCAD/pull/32828>
- <https://github.com/FreeCAD/FreeCAD/discussions/33066>
- <https://codeberg.org/yorikvanhavre/LinesCAD>

## Decisions

None recorded.

## Action items

- **Frank (mnesarco):** Contact the FreeCAD blog author to request a post about the FreeCAD Launcher.
- **Frank (mnesarco):** Ask Discord administrators to create a dedicated channel for the FreeCAD Launcher.
- **Frank (mnesarco):** Implement the ability for users to customize profile icons, including selecting from a library or uploading a custom image, and ensure the icon is stored within the profile.
- **Frank (mnesarco):** Investigate and implement Flatpak packaging for the launcher to enable automatic updates on Linux.
- **Frank (mnesarco):** Implement a system integration feature to add the launcher and profile shortcuts to the operating system's application menu.
- **Frank (mnesarco):** Refine the add-on health dashboard by removing confusing metrics and clarifying the index logic before wider promotion.

---

An automated agent made this draft from a transcript of the meeting. A maintainer reviews it before publication.
