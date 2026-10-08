# FPA Meetup: 2026-10-08

## Attendees

- Yorik
- Billy (aka Connor)
- reqrefusion
- Chris Hennes (@chennes)
- sliptonic
- Alexandre
- Max
- Christopher Rogers

## Topics

### Release Candidate and Windows on ARM Build

Discussion regarding the Windows on ARM build time approaching the six-hour timeout limit. It was noted that the build is experimental and the release manager does not need to wait for the fix to proceed with tagging the first release candidate.

### Terminating Grant 112

The meeting discussed Grant 112, which had received no response from the recipient for over a month. It was proposed to terminate the grant, removing the pending payment from the books, with the option for the recipient to resubmit a new grant in the future if they wish to pursue infrastructure work.

### CWG Bounty Program Budget Extension

The group reviewed the CWG bounty program, noting that only a portion of the originally allocated 5,000 euros was spent. It was agreed to extend the remaining budget (approximately 3,700 euros) into 2027 as a one-year extension rather than voting on a new grant, allowing the program to run until the funds are exhausted.

### Contractor Expectations Document

A document outlining expectations for contractors was reviewed and found satisfactory. The author agreed to put the document to a vote.

### IP Reputation Database Subscription

The subscription to the Thoth IP reputation database was canceled because the Anubis software is discontinuing Thoth support in favor of a new GOIP service integration. A free open source account for the new service has been secured, and systems will be updated once the new Anubis version is released.

### AI Meeting Note Taker

A new automated note-taking system was presented. The system joins meetings, records separate audio streams, generates transcripts via speech-to-text, creates minutes using a QN model, and submits them as a pull request for review. It currently runs on an Infomaniac cloud node. It was agreed to move all meeting agendas into a central 'Meetings' repository to facilitate this automated process.

Links from the meeting chat:

- <https://cloud.freecad.org/s/ZCJC5jLGC6SYrER>

### Wiki and Documentation Donation

Updates were given on outreach regarding a potential donation for wiki or documentation work. Further contact will be made with potential contributors and the original donor to clarify if the interest is specifically in the wiki or documentation in general.

### Strategic Direction Document

Work on the 'Where do we go from here' document is ongoing but was paused while the author focused on setting up the note-taking infrastructure.

### Swag Shop

The Swag Shop is operational and has generated approximately 450 USD. Plans include adding a link or QR code to the release video and introducing new t-shirt designs, including one with a humorous 'production use' warning and another featuring the old FreeCAD logo for Halloween.

### FreeCADWeb.org Domain Auction

The FreeCADWeb.org domain was sold at auction for 12,000 USD, likely to a domain squatter due to its backlink profile rather than a community member. The group acknowledged the value of the main FreeCAD.org domain and discussed efforts to remove backlinks pointing to the sold domain.

### Real World Meetups

Updates were provided on upcoming meetups: FOSDEM is under control, FAB 27 was noted, and a South American gathering in Peru is being planned. Responsibility for organizing and promoting the North American meetup (Bay Area) was transferred to another participant.

### Grant Program Deadlines and Naming

The next grant deadline was set for mid-November to allow voting to conclude before the holidays. Following feedback on a blog post, the group discussed renaming future grant cycles (e.g., 'Quarter 1 2027 grants') to better reflect that voting occurs in one quarter while funding execution happens in the next. It was also noted that the 2027 budget target is a minimum of 180k.

## Decisions

- Grant 112 is terminated, with the option for the recipient to resubmit a new grant in the future.
- The remaining budget for the CWG bounty program (approx. 3,700 euros) will be extended into 2027 as a one-year extension rather than creating a new grant.
- All meeting agendas will be moved to a central 'Meetings' repository to enable the automated AI note-taker to function hands-off across all meetings. *(review)*

## Action items

- **Max:** Tag the first release candidate.
- **Yorik:** Put the contractor expectations document to a vote.
- **Chris Hennes (@chennes):** Update systems to the new Anubis 1.28 release with GOIP integration once available.
- **Chris Hennes (@chennes):** Set up a DigitalOcean droplet for the meeting note-taker server.
- **Yorik:** Contact FEA Aang, FBLX5, and the original donor regarding the wiki/documentation donation.
- **Christopher Rogers:** Add a link or QR code for the Swag Shop to the end of the release video.
- **Christopher Rogers:** Add new t-shirt designs to the Swag Shop, including a 'production use' warning shirt and an old logo shirt.
- **sliptonic:** Take charge of organizing and promoting the North American (Bay Area) meetup.
- **Chris Hennes (@chennes):** Meet with Yorik to discuss individual line items for the 2027 budget.

---

A moderator removed the notetaker from the meeting before the end. These minutes contain only the part of the meeting before that time.

---

An automated agent made this draft from a transcript of the meeting. A maintainer reviews it before publication.
