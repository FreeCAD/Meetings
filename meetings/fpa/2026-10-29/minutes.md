# FPA Meetup: 2026-10-29

> Crow, an automated notetaker, made these minutes. They may contain mistakes or inaccuracies and are for reference only.
>
> Model: Qwen/Qwen3.5-397B-A17B-FP8  
> Source code: <https://github.com/FreeCAD/Meetings/tree/main/bot>

## Attendees

- sliptonic
- chris  @ipatch
- Yorik
- Kurt Kremitzki
- Billy (aka Connor)
- Jackson
- Justin (Philippines)

## Topics

### Infrastructure: ERP Next demo

Kurt Kremitzki announced a temporary demo instance of ERP Next is available for testing. It allows login but does not yet support custom app deployment. Sliptonic mentioned working on scripts to migrate and populate data to make it more production-ready.

Links from the meeting chat:

- <https://erpnext-demo.freecad.org>

### Bug triage: STEP import regression

Chris @ipatch reported investigating a STEP import issue that may date back to FreeCAD 1.0. Suggestions were made to use weekly builds for bisecting and to filter commits unrelated to OCAF or Sketcher to narrow down the search.

### Professional relations and contribution guidelines

Justin from an organization in the Philippines joined to discuss their company's migration to FreeCAD and desire to contribute. The group discussed the current status of the professional network, which is being retooled. Guidelines were explained regarding branding usage, the requirement to credit FreeCAD and link to the upstream source, and the standard process for contributing add-ons or core code via pull requests. It was clarified that using FreeCAD in non-open source workflows is permitted as long as the open-source nature of FreeCAD is disclosed to users.

### New website

The new website content is mostly complete, with a target release alongside version 26.3. Help is needed to finish remaining items. Marcos Polio was not present.

### Server migration and hosting providers

The Lens server remains offline. Discussion continued on migrating from OVH due to reliability concerns, with Infomaniac proposed as an alternative due to its OpenStack offerings and European base. This topic was merged with the cancellation of the DigitalOcean open source program credits.

### Trademark enforcement

No new enforcement actions are pending. The plan is to create a template letter with Chris to send whenever infringement is detected, ensuring a record of action is kept.

### Official grant cancellation policy

A proposal to default to auto-cancellation of grants after one year was discussed and deemed reasonable. The item remains open pending a final written policy from Chris.

### CWG bounty program renewal

The renewal of the CWG bounty program funding (3700 euro for 2027) was discussed. While effectively decided, the agenda item remains until formally added to the next year's budget.

### Formalizing accountability

A vote regarding the contractor reset in 2027 is underway. Several votes have been cast, and the group is waiting for one more before considering the item done.

### Meeting recording and minutes automation

Two instances of the Crow transcription tool are running (local and server). The current workflow creates pull requests that require manual review, preventing auto-merge. The group discussed the trade-off between forcing human review and achieving a hands-off process, inviting feedback on the quality of generated minutes to potentially enable auto-merge.

### Wiki donor project

Yorik has communicated with wiki contributors but has not yet formulated a plan. The item was bumped to the next meeting.

### Competition coordination and CRM

Chris is coordinating efforts to find individuals interested in working on a future CRM system and donor liaison tasks. No immediate action items were identified.

### ERP Next migration task list review

Sliptonic is using AI to generate migration scripts from GNU Cash and existing donor data to ERP Next. A task list of all system interactions has been generated and requires review by admins (Yorik, Chris, Joe) to verify accuracy and completeness before tutorials are created.

### Blocker reward program update

An action item for Joe to update the program description via a pull request is still pending.

### Support for open source AI

No update was available as Peter was not present.

### Thanking translators and budget

A budget item for thanking translators has been proposed by Chris but remains on the agenda until the budget is formally approved.

### Real world meetups (FOSDEM, FAB 27, etc.)

For FOSDEM, the dev room is limited to half a day. Yorik needs to put the budget to a vote and arrange a hackathon day with a local hackerspace. No updates were provided for FAB 27 or the South American meetup. The North American meetup has an outstanding to-do item with no progress.

### 2026 grant program

The next deadline for Q4 submissions is in December. No immediate action is required.

### Educational initiative and school district inquiries

Repeated inquiries from school districts regarding network ports and internal approval processes for FreeCAD were discussed. It was suggested that a FAQ or wiki page be created to address these common questions.

### CI infrastructure and GitHub dependency

Chris @ipatch raised the question of moving CI infrastructure to locally hosted hardware or a data center to reduce dependency on GitHub. Jackson noted that previous cost analyses showed self-hosting is significantly more expensive than GitHub's free tier, especially considering network bandwidth and storage. Yorik noted that GitHub's generous free compute creates a dependency that would be difficult to break, suggesting a long-term strategy might involve reducing CI usage or migrating to self-hosted Git solutions like Codeberg, though no immediate plans exist.

Links from the meeting chat:

- <https://cloud.freecad.org/s/ZCJC5jLGC6SYrER?dir=/&editing=false&openfile=true>

## Decisions

None recorded.

## Action items

- **Kurt Kremitzki:** Provide sliptonic with the password for the ERP Next demo instance.
- **sliptonic:** Contact Justin offline regarding donations, sponsorship, and website branding.
- **sliptonic:** Add items to the agenda regarding the trademark enforcement template letter.
- **chris  @ipatch:** Write up the official grant cancellation policy and provide a public link.
- **Yorik:** Return with a plan for the wiki donor project by next week.
- **Yorik:** Review the ERP Next migration task list for accuracy.
- **chris  @ipatch:** Review the ERP Next migration task list for accuracy.
- **Jackson:** Find and share previous cost analysis numbers regarding self-hosted CI infrastructure.
- **Yorik:** Put the FOSDEM budget to a vote.
- **Yorik:** Contact hackerspace organizers to arrange a hackathon day before FOSDEM. *(review)*
