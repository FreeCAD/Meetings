# FPA Meetup: 2026-11-12

> Crow, an automated notetaker, made these minutes. They may contain mistakes or inaccuracies and are for reference only.
>
> Model: Qwen/Qwen3.5-397B-A17B-FP8  
> Source code: <https://github.com/FreeCAD/Meetings/tree/main/bot>

## Attendees

- shai
- Billy (aka Connor)
- Chris Hennes (@chennes)
- sliptonic
- Frank (mnesarco)
- reqrefusion
- Jackson Oursland
- Adam Spontarelli
- Niemann Pest
- Yorik
- Bennett
- Alexandre

## Topics

### Contractor roles and API documentation

Discussion regarding the role of contractors in maintaining API documentation versus LLM-oriented documentation. It was noted that keeping type stubs up to date benefits both humans and LLMs. The Add-on ecosystem technical lead was encouraged to continue maintaining stubs and assist with reviewing add-on submissions.

### Robotics team sponsorship

Adam Spontarelli, along with team mentor Niemann Pest and student Bennett, requested continued sponsorship for their high school robotics team. They proposed a $500 sponsorship in exchange for a blog post and logo display, and discussed additional travel funding to present their use of FreeCAD at FOSDEM and a conference in Virginia. It was clarified that travel grants should be requested through the standard FPA travel grant program, with a maximum of 600 euros for FOSDEM, while the additional event requires a special vote. The team agreed to submit the necessary forms and emails. It was also suggested that the team produce a series of blog posts for the official FreeCAD blog rather than only a forum post to reach a wider audience.

### New website

The new website is available at the staging URL. Translation will be handled via CrowdIn. Challenges were noted regarding Hugo shortcodes embedded in Markdown, which CrowdIn attempts to translate incorrectly; a script is being developed to strip these out prior to translation.

### Lens server status

The Lens server is back online but remains closed to new account registrations while three remaining security issues are resolved. A new release is planned but has no specific date.

### Trademark enforcement

Template work for trademark enforcement is pending and remains an action item for sliptonic.

### Server migration

The organization is migrating servers, with an estimated cost of 125 euros per month. Ansible playbooks for the migration are nearly complete.

### Grant cancellation policy

A draft policy for grant cancellations was reviewed. The policy stipulates a one-year free term, requiring an application for a second year before the first expires, and automatic cancellation after two years allowing reapplication. The meeting agreed to put the document up for a vote.

### CWG bounty program

A reminder was issued to ensure the Core Work Group (CWG) bounty program is included in the upcoming budget.

### Formalizing accountability and contractor renewals

The contractor reset vote was approved. Discussion focused on organizing payment oversight with two people per payment and the renewal of Turan's contract. Issues were raised regarding Turan's inability to access PayPal due to Turkish citizenship restrictions. It was determined that the role requiring PayPal access must be filled by someone in a supported country, and the scope and budget of Turan's renewed contract need to be redefined.

### Meeting recording status

A to-do item exists to add 'crow' to the Ansible configuration to enable meeting recordings.

### Organizational task list

Participants were asked to review an AI-generated task list to ensure all FPA-related activities are reflected as well-bounded tasks and to remove items that are no longer relevant. sliptonic agreed to pare down and organize the list.

### Blocker reward plus up

Brief mention of the blocker reward program; no detailed discussion occurred.

### Thanking participants

Reminder that budget allocation for thanking participants needs to be secured.

### Next real world meetup

Plans for the FOSDEM hackathon space were discussed. The previous venue expressed concerns about cleanliness and supervision. Yorik proposed designating a person responsible for cleanliness and sending a formal commitment to the venue. Chris Hennes volunteered to stay late to ensure the space is cleaned. If the venue is not secured, alternative locations such as Yorik's apartment will be considered.

### Blog team and Bay Area meetup

sliptonic is continuing efforts to connect with the blog team and locate FreeCAD users in the Bay Area for a potential meetup.

### Grant program submission deadline

The deadline for the quarterly grant program submissions is November 15th, any time zone on Earth. Alexandre offered to post an announcement regarding the deadline.

## Decisions

- The meeting agreed to put the grant cancellation policy document up for a vote in its current form.

## Action items

- **Frank (mnesarco):** Keep type stubs up to date and assist with reviewing incoming add-on submissions. *(review)*
- **Adam Spontarelli:** Submit a travel grant request form for FOSDEM.
- **Adam Spontarelli:** Send an email requesting a special travel grant for the conference in Virginia.
- **Adam Spontarelli:** Prepare a series of blog posts about the robotics team's work for the official FreeCAD blog.
- **Chris Hennes (@chennes):** Initiate the vote to renew the $500 team sponsorship.
- **sliptonic:** Complete template work for trademark enforcement.
- **Chris Hennes (@chennes):** Add 'crow' to the Ansible configuration to enable meeting recordings.
- **sliptonic:** Review, pare down, and organize the AI-generated organizational task list.
- **Yorik:** Send an email to the FOSDEM hackathon venue committing to cleanliness and designating a responsible person. *(review)*
- **Chris Hennes (@chennes):** Act as the person responsible for staying late to ensure the hackathon space is cleaned.
- **Alexandre:** Post an announcement regarding the grant program submission deadline.

## Proposals and objections

- **Yorik** (proposal): Proposed splitting the robotics team funding request into three parts: a $500 sponsorship renewal, a travel grant request for FOSDEM (max 600 euros), and a special grant request for the Virginia conference.
- **sliptonic** (proposal): Suggested that the robotics team create a series of blog posts for the official FreeCAD blog instead of only a forum post to better reach audiences outside the current community.
