# FPA Meetup: 2026-11-05

> Crow, an automated notetaker, made these minutes. They may contain mistakes or inaccuracies and are for reference only.
>
> Model: Qwen/Qwen3.5-397B-A17B-FP8  
> Source code: <https://github.com/FreeCAD/Meetings/tree/main/bot>

## Attendees

- Chris Hennes (@chennes)
- Billy (aka Connor)
- sliptonic
- reqrefusion
- Adam Spontarelli

## Topics

### New website translation

The new website is ready except for the translation system. The current plan to use Crowdin with Hugo markdown files is problematic because Crowdin attempts to translate short tags. Options discussed include writing a script to strip and re-inject tags or handling translation within the CMS instead of Crowdin.

### Lens Server status

The Lens Server is back online but new registrations are disabled due to a bug allowing self-verification of emails. Three security vulnerability reports related to a previous hack remain open and have not yet been addressed by Amrapal.

### Trademark enforcement

A template letter for trademark enforcement is needed. It was agreed to draft this using AI assistance and host the file temporarily on cloud.freecad.org, with the possibility of moving it to a Git repository later. Once the template is ready, enforcement actions will begin.

### Server migration

Migration to OVH is stalled due to lack of availability. The group is considering Infomaniak as an alternative, which offers more power than OVH's smallest servers at a lower cost than DigitalOcean. Ansible playbooks are being written to manage the new stack, allowing for easy reprovisioning.

### Official grant cancellation policy

A short policy stating that grants are canceled eventually and do not float forever was posted. Review of the policy was requested but had not yet occurred.

### Renewing the CWG Bounty Program

The group confirmed the decision to renew the CWG Bounty Program. This item remains on the agenda until the decision is documented elsewhere.

### Formalizing accountability and contractor reset

The meeting confirmed that new contract renewal rules have passed. These rules state that contracts are for one year or less, the FPA will reach out prior to expiration, contracts require an annual vote, and payment requires both an invoice and a monthly (or more frequent) report.

### CRM and ERP Next

Discussion focused on coordinating community relations, accounting, and receipts. Kurt has set up an instance of ERP Next. A task list generated from requirements matching ERP Next needs reviewers to verify its completeness and accuracy. The group acknowledged the need for a coordinator for these tasks but noted there is no job description and no one currently willing to take on the high-trust role.

### Robotics team sponsorship request

Adam Spontarelli requested to pitch for continued sponsorship for his robotics team. Due to low attendance, it was decided to move this discussion to the next meeting's agenda to ensure a larger group is present.

### Blocker reward plus up

This item remains on the agenda but has not been acted upon as Joe has been unable to attend meetings for months. The group may need to renegotiate meeting times.

### Item 4 (Peter's project)

This agenda item was removed as Peter is dealing with personal life issues and will be away from the project for some time.

### Thanking translators and participants

The effort to thank translators and participants will wait for next year's budget.

### Merch store

The merch store is live and generating revenue, which may serve as a source for an advertising budget next year.

### Real world meetups

FOSDEM has been accepted for a half-day dev room; the group plans to be more selective this year due to a high volume of AI-generated submissions. Chris Hennes will attend Fab25 in Finland and a South American gathering. A North American meetup is being planned in conjunction with OpenSauce in the Bay Area.

### Grant program deadline

The deadline for Q4 grant submissions is November 15th, which is two weeks earlier than usual.

### Add-on submissions and AI

The group discussed the impact of AI on development, noting an increase in individuals creating add-ons without collaboration. The 30-day waiting period for add-on submissions was noted as an effective filter, as many developers lose interest before the period expires.

## Decisions

- The new contract renewal rules have passed, establishing that contracts are for one year or less, require annual votes, and necessitate invoices and reports for payment.
- The agenda item regarding Peter's project (Item 4) is removed from the agenda.

## Action items

- **sliptonic:** Draft a template letter for trademark enforcement, potentially using AI assistance.
- **Chris Hennes (@chennes):** Send the trademark enforcement template letter once it is ready.
- **Chris Hennes (@chennes):** Add Adam Spontarelli and the robotics team sponsorship pitch to the agenda for next week's meeting.
- **sliptonic:** Have the AI generate a tutorial for ERP Next tasks (monthly accounting, onboarding) and continue verifying the task list.
