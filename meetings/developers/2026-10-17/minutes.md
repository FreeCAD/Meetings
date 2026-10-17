# Developers Meeting: 2026-10-17

> Crow, an automated notetaker, made these minutes. They may contain mistakes or inaccuracies and are for reference only.
>
> Model: Qwen/Qwen3.5-397B-A17B-FP8  
> Source code: <https://github.com/FreeCAD/Meetings/tree/main/bot>

## Attendees

- 3
- Billy (aka Connor)
- Max
- tester
- Jackson Oursland
- Chris Hennes (@chennes)
- John O’Shaughnessy (JohnOCFII)
- shai
- adrianinsaval
- Chris Rozario
- Kacper Donat (kadet)

## Topics

### Bounty issue identification

This standing agenda item was reviewed. No issues were proposed for bounties during the meeting.

### FreeCAD 26.3 release

The release manager confirmed plans to cut the second release candidate (RC2) the following day. The team reviewed the status with no questions or concerns raised.

### Meetings repo and Crow AI note taker

A new custom AI note taker developed by sliptonic, running on a private Qwen instance via Infomaniak, has been introduced. It automatically joins meetings, generates transcripts and summaries based on the agenda, and posts them as pull requests to the new `FreeCAD/meetings` repository. Consequently, future agendas and minutes will be hosted in this new repository, and the old developer meetings repository will be shut down and migrated.

### Digital Ocean migration

Due to Digital Ocean discontinuing their open source credit program and rising costs, the infrastructure team plans to migrate all services to OVH cloud over the next one to two months. This move will reduce monthly costs significantly while maintaining data residency in Frankfurt, EU. The migration will involve brief, scheduled outages for the wiki and forum services to facilitate database backups and transfers, though the website cutover is expected to be transparent.

### Lens Server compromise

An administrative account on the Lens test server (lens.freecad.org) was compromised earlier in the week due to a software flaw. The server has been taken offline while a mitigation is developed and reviewed. Once a fix is ready, a new release of the Ondsel server software will be issued, accompanied by three security advisories. Users are warned that email addresses and files stored on the server should be treated as exposed. Other running instances are unknown as registration is not required.

### Internal library framework

A participant inquired about a previous discussion regarding an internal library framework. It was noted that while the topic was raised previously, no concrete decisions were made. Another participant mentioned having an independent proof of concept and ongoing discussions about registering library endpoints on the Addon Manager, aiming to coordinate efforts to avoid duplicating work.

### Wiki and Forum maintenance

The wiki is currently experiencing high load due to a Meta crawler stuck on translation pages, which will be blocked shortly. Additionally, the forums are scheduled for a two-hour downtime later in the day to apply a PHPBB upgrade addressing a security vulnerability.

## Decisions

None recorded.

## Action items

- **Max:** Cut the RC2 release for FreeCAD 26.3.
- **Chris Hennes (@chennes):** Block Meta's crawler from the wiki to resolve high server load.
- **Chris Hennes (@chennes):** Review and finalize mitigation for the Lens server compromise with Amrit Paul, then release a new version of the Ondsel server and publish security advisories. *(review)*
- **Chris Hennes (@chennes):** Take the forums offline for approximately two hours to perform a PHPBB security upgrade.
