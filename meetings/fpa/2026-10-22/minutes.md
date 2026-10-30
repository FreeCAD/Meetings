# FPA Meetup: 2026-10-22

> Crow, an automated notetaker, made these minutes. They may contain mistakes or inaccuracies and are for reference only.
>
> Model: Qwen/Qwen3.5-397B-A17B-FP8  
> Source code: <https://github.com/FreeCAD/Meetings/tree/main/bot>

## Attendees

- Chris Hennes (@chennes)
- Yorik
- Jackson Oursland
- reqrefusion
- Frank (mnesarco)
- Billy Mobile
- sliptonic
- shai
- Kurt Kremitzki

## Topics

### Add-on Manager and AI-generated add-ons

Discussion regarding the influx of AI-generated add-ons in the Addon Manager. Concerns were raised about ephemeral, unmaintained add-ons created without developer commitment. A 30-day waiting period for new repositories has been instituted to filter out low-effort submissions. Participants discussed the scalability of manual reviews and the potential for an automated delisting policy based on maintenance activity scores, while noting that stable, single-purpose add-ons should not be removed automatically.

### New FreeCAD website

An update was provided regarding the new website preparation for version 26.3. The community was invited to review the site and the associated priority list.

### Lens server security incident and migration

The FPA Lens server was taken offline following the exploitation of three vulnerabilities (two critical, one moderate). The current plan is to discard the compromised droplet and migrate to a new server on OVH hosting in the EU, managed via Ansible. User data and accounts will be preserved. Security advisories (CVEs) will be published once fixes are deployed to protect other potential Lens server operators.

### Trademark enforcement

The meeting reviewed the process for trademark enforcement to maintain legal standing. The immediate action involves sending cease-and-desist letters to two U.S. companies. It was agreed to document the enforcement process and maintain a log of all correspondence. A template for EU-specific letters may be developed in the future.

### DigitalOcean migration and Ansible setup

Due to the cancellation of DigitalOcean's open-source credits program, the FPA will migrate its hosting to OVH. The migration will utilize an Ansible setup previously planned by Kurt Kremitzki to automate server management, allowing administrators to update configurations via code.

### Grant cancellation policy

A draft policy for grant cancellations was presented. The proposal suggests that grants auto-cancel after one year of inactivity unless an extension is requested, with a hard cancellation after two years requiring a new proposal. The document is available for review, with a formal discussion scheduled for a future meeting.

### CWG bounty program renewal

The Core Work Group (CWG) bounty program will be renewed for the coming year using the remaining budget of 3,700 euros. The CWG will determine how to allocate these funds.

### Accountability and contract renewal rules

The discussion on accountability concluded with an open vote initiated by Yorik regarding contract renewal rules. Remaining incomplete items in the accountability document are to be removed or noted as part of the open vote.

### Meeting recording infrastructure

The meeting confirmed that AI note-taking is functional. Action items remain to provision a new server (via OVH or DigitalOcean) to host the recording infrastructure permanently, pending credit card authorization.

### Wiki grant and donation

Updates were given on a 2,500 euro grant earmarked for wiki work. Communications have been sent to potential contributors to gauge interest and ideas, but no replies have been received yet. An offer to refund the donor was also made if the project does not proceed.

### ERP Next evaluation

The evaluation of ERP Next as a potential management tool continues. A sandbox instance needs to be set up to verify requirements. Odoo was considered but rejected due to its closed-source enterprise tier requirements. ERP Next was identified as a viable open-source option requiring minimal custom development.

### Blocker rewards and hackathon updates

The blocker reward program has not been necessary for the 26.3 release as the community has been diligent in resolving issues. No significant updates were available regarding the recent hackathon.

### Translator and participant appreciation

The budget item for thanking translators is being expanded to a general program for providing swag to active participants and contributors.

### Real-world meetups: FOSDEM, FAB27, and North American meetup

The Open Hardware Dev Room at FOSDEM has been accepted for a half-day session on Sunday morning. FreeCAD Day is scheduled for the preceding Friday, January 29th. A hackathon with local hackerspaces is being planned for the Thursday prior. Attendance was confirmed by several members. The FAB27 summit will be held in Finland next August. For the North American meetup, NoiseBridge in the Bay Area has offered space, and coordination assistance is being sought.

### 2027 Grant Program budget

The deadline for Q4 grant applications is November 15th. A proposal to set the 2027 grant program budget at 40,000 euros (10,000 euros per quarter) was discussed and accepted as a starting point.

### SolidCAM inquiry

The FPA received an inquiry from the CEO of SolidCAM, a commercial CAM application, expressing interest in joining the FPA and collaborating on specific non-CAM technical features. They were invited to a future meeting to discuss potential relationships and conflicts of interest with the FreeCAD CAM workbench.

### Anonymous sponsorship and Debian AI inference

An anonymous organization donated $5,000 via GitHub Sponsors. Additionally, a Debian project offering open-weight LLM inference for developers was shared as a potential ethical AI resource for the community.

Links from the meeting chat:

- <https://inference.debian.net/doc>

## Decisions

- The 2027 grant program budget will start at 40,000 euros total, allocated as 10,000 euros per quarter.

## Action items

- **Chris Hennes (@chennes):** Send trademark enforcement letters to two U.S. companies and document the process and correspondence in a new NextCloud document.
- **Yorik:** Review and adapt the trademark enforcement letter template for EU legal language when the next opportunity arises.
- **Chris Hennes (@chennes):** Migrate FPA services from DigitalOcean to OVH hosting using Ansible for server management.
- **Chris Hennes (@chennes):** Publish GitHub security advisories (CVEs) for the Lens server vulnerabilities once fixes are in place.
- **Chris Hennes (@chennes):** Set up an ERP Next sandbox instance for evaluation.
- **Chris Hennes (@chennes):** Coordinate with Yorik to obtain credit card authorization and provision a server for meeting recordings.
- **Yorik:** Contact hackerspace organizers to schedule a hackathon prior to FOSDEM.
- **Kurt Kremitzki:** Reach out to the NoiseBridge social network to find volunteers for coordinating the North American meetup.
