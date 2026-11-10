# BIM Meetup: 2026-11-10

> Crow, an automated notetaker, made these minutes. They may contain mistakes or inaccuracies and are for reference only.
>
> Model: Qwen/Qwen3.5-397B-A17B-FP8  
> Source code: <https://github.com/FreeCAD/Meetings/tree/main/bot>

## Attendees

- Roy
- Tom (semhustej)
- Markko Martin Loris De Rosso
- Max

## Topics

### Audio issues and attendance

The meeting started with audio difficulties for Roy, who could not get his microphone working. Participants discussed the issue while waiting. Roy communicated via chat that he would listen and provide feedback there. The meeting proceeded with Max presenting topics while Roy followed in the chat.

### Proposal for additional maintainers for Draft and BIM workbenches

Max proposed establishing a workflow similar to the CAM workbench team for the Draft and BIM workbenches. This would involve adding more maintainers (such as @tritao, @furgo16, and @marcuspollio) who could review and merge their own PRs and those of others, reducing the bottleneck on the core maintainers. Max noted that Tritao had expressed interest in returning under this model. @roy-043 agreed in principle but emphasized the need for double-checking and noted risks with self-merging large PRs. Tom added that some PRs involve C++ code which current BIM/Draft maintainers might not be able to review.

### Meeting frequency

Participants discussed changing the meeting schedule from weekly to bi-weekly (or bi-monthly) due to low developer attendance in recent weeks. Roy proposed the change in chat, and the group agreed. Max updated the calendar accordingly.

### FreeCAD 0.26.3 and 0.27.x release status

Max provided an update on the upcoming 26.3 release, noting one remaining release-blocking issue regarding expressions and units that Peter is fixing. Once resolved, Release Candidate 3 will be issued, with a stable release potentially following a week later. Max also looked ahead to 27.2, mentioning the expected integration of OCCT 8.1 which will improve fillets, chamfers, and thickness operations, as well as a new topological naming algorithm being developed by @drwho495.

### Meeting minutes repository

Roy asked where recent meeting notes could be found. Max located the repository where an AI chatbot automatically uploads minutes and shared the link. It was noted that the bot had missed some previous meetings due to scheduling changes.

Links from the meeting chat:

- <https://github.com/FreeCAD/Meetings/tree/main/meetings>

### Testing Tritao's code

Max suggested Roy test code from Tritao. Since it was unclear if a PR existed, Max explained how to build branches from a fork using GitHub Actions to generate test binaries for Windows, Mac, and Linux without needing local compilation.

### New FreeCAD website and DevTalk forum

Max introduced the staging version of the new FreeCAD website, primarily developed by Markus, which aims to replace the current site with a more modern design better suited for mobile devices. Max also mentioned DevTalk, a Discourse-based forum intended for development discussions and testing forum migration, sharing links for both.

Links from the meeting chat:

- <https://staging.freecad.org/>
- <https://devtalk.freecad.org/>

### Wiki versioning challenges

The group discussed the difficulty of maintaining the Wiki with a faster release cycle (three stable releases per year). Roy noted that a fully versioned Wiki would require significantly more work and volunteers. Tom mentioned that Blender uses Furo for documentation, sharing a link to the project, though no decision was made to switch tools.

Links from the meeting chat:

- <https://github.com/pradyunsg/furo>

### AI-generated fixes in AstoCAD fork

Max discussed a fork by paddlestroke (AstoCAD) where many issues were addressed via AI-generated commits without human review. Max described adding a 'fixed in fork' label to track these issues for potential cherry-picking or inspiration, while avoiding spamming the original issues.

### Maintainer communication channels

Max asked Roy about joining the maintainers' Telegram group for easier communication. Roy explained he does not have a smartphone and has had trouble regaining access to his desktop Telegram account. Max suggested it might be possible to register using a non-smartphone number to receive an SMS code, and Roy agreed to try again.

## Decisions

- The BIM Meetup will change from a weekly to a bi-weekly (bi-monthly) schedule.

## Action items

- **Max:** Talk to other maintainers about Roy's agreement to have more maintainers for Draft and BIM.
- **Roy:** Try to regain access to Telegram desktop to join the maintainers' group.
- **Roy:** Invest more time in preparing agenda items for the next BIM meeting.
