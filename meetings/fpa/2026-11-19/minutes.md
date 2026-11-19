# FPA Meetup: 2026-11-19

> Crow, an automated notetaker, made these minutes. They may contain mistakes or inaccuracies and are for reference only.
>
> Model: Qwen/Qwen3.5-397B-A17B-FP8  
> Source code: <https://github.com/FreeCAD/Meetings/tree/main/bot>

## Attendees

- Billy (aka Connor)
- reqrefusion
- sliptonic
- Chris Hennes (@chennes)
- Yorik
- Max
- Jackson
- John ( PhoneDroid )
- Alexandre

## Topics

### Attendance and Contractor Updates

The meeting noted light attendance among contractors. Discussion covered open blockers, specifically the wait for OpenCascade 8.0.2, and the status of a video project which is nearly finished.

### Finances

Financial reports indicated the organization is over the average for the month with low expenses. The group confirmed staying on track for the 180,000 euro budget target for the next year. A large donation expected two weeks prior was clarified to occur next month.

### Q4-2026 Grants Voting

Voting is open for the Q4-2026 grants. The program is heavily oversubscribed against a 10,000 euro budget with many new applicants. The evaluation period is set to close by December 15th to allow announcements before the holidays.

### Robotics Team Sponsorship

A vote is open to renew a $500 sponsorship for Vector Space Robotics. In exchange for funding, the team will present at the meeting and produce a blog post rather than forum posts to increase visibility.

### Lens Server Security and Migration

The Lens server is back online following a compromise. A report on the incident will be shared with FPA members and publicly once three GitHub security reports regarding default installation settings are resolved. The server is being migrated from DigitalOcean to Infomaniak to reduce costs and improve capacity.

### Server Migration and Forum Software Update

As part of the migration to Infomaniak, the forums will be moved from phpBB to Discourse while the servers are offline for backup and restore. The wiki also requires maintenance to restore properly. The new infrastructure will use Ansible for management, with separate servers for forums, wiki, monitoring, and applications. Infomaniak provided 300 euros in free credits for the first three months.

### Grant Cancellation Policy

A vote is open regarding the grant cancellation policy, consisting of three short bullet points previously discussed. The policy does not affect the current grant holder who has been absent.

### CWG Bounty Program

Renewal of the CWG bounty program is on hold pending finalization of the budget.

### Contractor Reset and Payment Protocol

A previous vote established that no contracts auto-renew. Upcoming contract renewals require coordination between Yorik and Turan. A formal payment protocol involving checks and balances between Yorik and reqrefusion needs to be defined and documented.

### Meeting Recording Status

The automated meeting recording tool (Crow) is functioning well and integrated into the Ansible configuration. Discussion addressed the length of the generated minutes; while some found them short, they were deemed accurate and superior to manual notes. Transcripts are retained for seven days due to privacy considerations, though this policy can be adjusted.

Links from the meeting chat:

- <https://github.com/FreeCAD/Meetings/blob/main/meetings/developers/2026-10-17/minutes.md>

### Wiki Grant Ideas

Yorik contacted the wiki group and received a list of potential grant ideas from several contributors. These ideas will be condensed into a proposal for the budget vote.

### Task Lists and Workflows

Existing task lists broken out by role will be consolidated and refined into draft workflows and reports to facilitate feedback.

### Blocker Reward Program

Discussion focused on a reward claim for CAM workbench fixes. The group noted the need to verify the submissions and decide on renewing the reward program budget, as the current funds may be insufficient or expired. A vote will be initiated to reauthorize the program.

Links from the meeting chat:

- <https://github.com/FreeCAD/FPA/issues/516>
- <https://github.com/orgs/FreeCAD/projects/43/views/1>

### Upcoming Meetups (FOSDEM and North America)

For FOSDEM, a room has been reserved at the Hackerspace Brussels for the Thursday before the event. Plans for a North American meetup in the Bay Area are ongoing, with investigations into suitable makerspaces.

### 2026 Grant Program Reminder

A final reminder was issued for FPA members to submit votes for the 2026 grant program by the December 15th deadline.

## Decisions

None recorded.

## Action items

- **Yorik:** Review the pull request containing the trademark enforcement template letter and policy.
- **Chris Hennes (@chennes):** Finish the forums Ansible configuration for the server migration.
- **Yorik:** Organize a payment protocol with reqrefusion. *(review)*
- **Yorik:** Condense the list of wiki grant ideas into a proposal for the budget vote.
- **sliptonic:** Consolidate agenda items 5 and 6 regarding task lists into a more usable format with draft workflows.
- **sliptonic:** Review David's submission in issue #516 to verify the CAM workbench fixes are legitimate.
- **Chris Hennes (@chennes):** Initiate a vote to reauthorize the blocker reward program budget.
