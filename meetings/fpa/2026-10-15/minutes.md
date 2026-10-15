# FPA Meetup: 2026-10-15

> Crow, an automated notetaker, made these minutes. They may contain mistakes or inaccuracies and are for reference only.
>
> Model: Qwen/Qwen3.5-397B-A17B-FP8  
> Source code: <https://github.com/FreeCAD/Meetings/tree/main/bot>

## Attendees

- Chris Hennes (@chennes)
- shai
- sliptonic
- Frank (mnesarco)
- reqrefusion
- Billy (aka Connor)
- Jackson Oursland
- Yorik
- Christopher Rogers
- Joe (Obelisk)

## Topics

### Addon Ecosystem and Typings Release

Frank reported on pending pull requests for the addon ecosystem and the readiness to release typings. A test release candidate (RC) will be issued to PyPI as a pre-release to verify the process and token permissions before the official RC1 cut. Frank also clarified the use of the FreeCAD icon in a community launcher, confirming it is permissible as long as it refers to the project without implying endorsement.

### Finance Report

The finance report noted that September donations were the lowest of the year but still higher than in previous years. Expenses were limited to fixed costs. The budget planning for the next year will target 180,000 euros, though the final amount may depend on the impact of the second release of the year.

### Infrastructure Migration from DigitalOcean to OVH

DigitalOcean has canceled its open source credit program, prompting a migration to OVH to reduce hosting costs from approximately 300 euros per month to under 100 euros. The plan involves using Ansible scripts previously developed by Kurt to migrate services one by one, with a period of double-hosting. The new servers will have increased storage capacity. Video meeting services like Jitsi will require separate server resources if self-hosted in the future.

### Official Grant Cancellation Policy

Discussion on this item was deferred as the policy has not yet been written.

### Renew the CWG Bounty Program

The Core Working Group (CWG) agreed to roll forward the previously allocated $3,700. The CWG intends to restructure the grants into fewer, larger pieces rather than many small ones. The FPA will allocate the funds accordingly.

### Release Manager Role and Contractor Resets

New rules making it mandatory to renew all contracts are up for an FPA vote. The contractor reset process is underway, with Frank confirming he has been contacted. The organization of the payment schedule and process remains a work in progress.

### Meeting Recording Status

The meeting recording service (Crow) will be the first service migrated to the new OVH infrastructure. The code for Crow and the meeting minutes will reside in a dedicated repository where pull requests are auto-merged after a week if unchanged. Legacy minutes have not yet been moved to the new repository.

### Documentation Donation and Wiki Strategy

A donor canceled a recurring donation intended for wiki evolution after no immediate action was taken, leaving a balance of five months' funding (2,500 euros). The group discussed how to utilize these funds without alienating current volunteer contributors. Proposals included hiring a person specifically for release-time wiki updates, creating a grant program for page updates, or issuing an open call for proposals without a predefined job description. It was agreed that any paid work must be perceived as support rather than an imposition on the community.

### Donor Management and ERP Software

Brad presented an analysis suggesting ERP Next as a potential tool for managing donor data, CRM functions, and accounting, noting it is accrual-based rather than cash-flow-based. To evaluate the tool, a sandbox instance will be set up on the new infrastructure. The group acknowledged the need for better tools to track donor opt-in/opt-out status and manage communications.

### Blocker Reward Plus Up

This initiative has not proven necessary for the current release cycle. Joe plans to document the existence of the program.

### Thank You Merchandise

A budget item of 1,000 euros will be allocated for thank-you merchandise, likely in the form of redemption certificates via Fourthwall.

### Next Real World Meetup (FOSDEM and FreeCAD Day)

FreeCAD Day is confirmed for the last Friday in January, independent of the FOSDEM dev room application status. Christopher Rogers volunteered to handle video recording using equipment he is designing in FreeCAD. Budget preparation for travel and merchandise (stickers, t-shirts, pencils) will begin early. Yorik will investigate sourcing bicolor pencils similar to previous years.

### North American Meetup

No progress has been reported on organizing a North American meetup.

### Grant Program Submission Deadline

The submission deadline for the next quarter's grant program is set for November 15th, two weeks earlier than usual to accommodate the holidays.

### Trademark Enforcement and IP Infringement

The group discussed instances of potential trademark infringement, including a website (freecad-app.com) selling FreeCAD and an app on the Apple Store. While the website's donation links appear broken or redirect to official pages, the group recognized the need for a formal process to demonstrate due diligence in defending the trademark. It was proposed to send a stern letter to the domain registrar or hosting provider (Cloudflare) and document the attempt, even if no immediate takedown occurs.

Links from the meeting chat:


## Decisions

- The FPA will target a budget of 180,000 euros for the next year while finalizing the budget with Yorik.
- The infrastructure team will migrate hosting from DigitalOcean to OVH using Ansible scripts to reduce costs and improve server specifications. *(review)*
- The CWG bounty program funds ($3,700) will be rolled forward to the next year, with the CWG deciding on the distribution structure.
- A sandbox instance of ERP Next will be set up on the new infrastructure to evaluate its suitability for FPA's software management needs. *(review)*
- A budget item of 1,000 euros will be allocated for thank-you merchandise for donors. *(review)*
- FreeCAD Day is confirmed for the last Friday in January, regardless of the FOSDEM dev room application outcome.

## Action items

- **Chris Hennes (@chennes):** Trigger the first test release of the addon typings to PyPI as a pre-release to verify token permissions. *(review)*
- **Chris Hennes (@chennes):** Migrate the FPA infrastructure from DigitalOcean to OVH using Ansible scripts.
- **Chris Hennes (@chennes):** Set up the meeting recording service (Crow) on the new OVH infrastructure.
- **Yorik:** Email the active wiki contributors to gather ideas on how to use the remaining 2,500 euros from the canceled documentation donation.
- **Chris Hennes (@chennes):** Set up a sandbox ERP Next instance for Brad to test CRM and accounting migration.
- **Yorik:** Prepare the voter budget for the FOSDEM/FreeCAD Day meetup early.
- **Yorik:** Investigate sourcing bicolor pencils for meetup merchandise.
- **Chris Hennes (@chennes):** Draft a stern letter regarding trademark violation to send to the domain registrar or hosting provider of freecad-app.com and document the attempt.

## Proposals and objections

- **Frank (mnesarco)** (proposal): Proposed using a grant program for the wiki where contributors receive small payments (e.g., $10) per page update instead of hiring a single person.
- **Yorik** (proposal): Proposed paying someone to work on the wiki specifically during release times to bring documentation up to date, similar to the release manager role.
- **Chris Hennes (@chennes)** (proposal): Proposed inverting the hiring process by announcing a 2,500 euro grant pool for the wiki without a predefined job description, allowing community members to submit proposals.
- **sliptonic** (proposal): Suggested adding an agenda item for the next meeting to revisit trademark issues and document a formal process for handling infringement claims.
