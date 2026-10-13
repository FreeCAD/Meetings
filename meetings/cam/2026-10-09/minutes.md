# CAM Meetup: 2026-10-09

## Attendees

- 3
- Fae
- sliptonic
- Billy (aka Connor)
- Alan Grover
- Carl
- kk

## Topics

### Simulator development and PR strategy

Discussion on breaking down the simulator and workholding changes into discrete, layered pull requests (PRs) due to their interdependencies. The goal is to consolidate multiple simulators into one while retaining the ability to toggle back to the original simulation for lower-end hardware.

### PR #33229 (SLCAM) review and CMake issues

Review of PR #33229 revealed that new files were missing from the CMake configuration, preventing installation. Additionally, a test suite failure was reported, which the author could not fully diagnose due to GUI crashes; switching to command-line testing was suggested.

### PR #33255 (Machine Editor update)

Updates to the machine editor were discussed, including the removal of unused code. The PR was identified as fixing a regression caused by previous changes. It was agreed to rebase the PR and have it merged after a final check.

### PR #33226 (Tool change format refactoring)

A proposal to refactor tool change formats (M6, T codes) into a dropdown with tooltips was discussed. Concerns were raised about mixing output generation semantics with the capture of tool change semantics. The group discussed whether parameters should reside in the tool head or post-processor, noting that different machine types (e.g., laser vs. spindle) may require different handling. Specific machine requirements for Maso and Carvera were noted as needing custom solutions.

### Haas post-processor and inheritance structure

Discussion on creating a generic base class for Haas and Fanuc-based machines to avoid code copy-pasting. The name 'generic multi-axis industrial' was suggested and accepted. The long-term goal is to move all machines to the machine-based post-processor system and deprecate legacy versions.

### Post-processor inheritance documentation

A suggestion was made to create a visual representation (e.g., a Mermaid graph) of the post-processor inheritance hierarchy to clarify the relationships between legacy, refactored, and machine-based post-processors.

### Lathe and mill-turn support roadmap

Support for lathes and mill-turn machines is currently blocked by the need to change the internal path command structure to include tool orientation vectors. A proposal was made to implement Cutter Location (CL) data as an intermediate representation to improve efficiency and enable these features.

### Dynapath post-processor (PR #33174)

Feedback on the Dynapath post-processor was addressed. The PR includes cherry-picked code from previous contributions, and a follow-up commit is planned to fix remaining issues before merging.

### LinuxCNC post-processor fix (PR #33254)

PR #33254 addresses a breakage in the LinuxCNC post-processor and includes support for tilted work planes. It was prioritized for immediate review and merging.

### Code style and Python imports

A discussion on Python import styles concluded that the modern convention `from x import a` is preferred over `import x as x` for brevity and linting compliance.

Links from the meeting chat:

- <https://docs.astral.sh/ruff/rules/manual-from-import/>

### New contributor and AI usage policy

A new contributor submitted a PR with a large C++ test suite, raising suspicions of AI-generated code without attribution. The group discussed the need for contributors to disclose AI usage per community policy, ensure proper file naming, and engage with the community to build trust.

### CAM Simulator and Workholding demo

A demonstration showed new features including locking setup sheets, snapping vices and fixtures to tables, T-slot support, and shank collision detection. The simulator now supports automatic selection between CPU and GPU rendering based on performance tests. The workholding system uses a custom 'snap solver' rather than the Assembly workbench to keep the workflow self-contained within CAM.

### Roadmap and Epic documentation

It was agreed that epics should be drafted for the simulator and the path command/CL data changes to define scope and allow for community feedback before major merges.

## Decisions

- The name 'generic multi-axis industrial' was accepted for the new base class for Haas and Fanuc machines.
- PR #33254 (LinuxCNC fix) is to be reviewed and merged immediately.

## Action items

- **sliptonic:** Provide review notes for PR #33229 regarding CMake and test failures.
- **Fae:** Fix CMake configuration for new files in PR #33229 and rebase the PR.
- **Billy (aka Connor):** Merge PR #33255 after Fae rebases it.
- **Carl:** Review PR #33226 (tool change refactoring) and provide feedback.
- **Carl:** Work with Fae to create machine definitions in the machines repo for specific models.
- **sliptonic:** Add a commit to PR #33174 (Dynapath) to address feedback on cherry-picked code.
- **Billy (aka Connor):** Re-review and merge PR #33254 (LinuxCNC fix).
- **Billy (aka Connor):** Run a full Camper check on the machine editor PR and reconcile findings.
- **Billy (aka Connor):** Contact Max (Release Manager) regarding failed backport merge requests.
- **Billy (aka Connor):** Move issue #33275 (boundary tolerance fix) to the 27.1 milestone.
- **Billy (aka Connor):** Move issue #33319 (operation start points bug) to the 26.3 milestone.
- **Billy (aka Connor):** Update Python import style in the relevant PR to use `from x import a`.
- **sliptonic:** Draft an EPIC for the simulator project defining scope and direction.
- **sliptonic:** Draft an EPIC for the tool orientation vector and path command changes (CL data).
- **sliptonic:** Add untagged CAM-related issues from Alan's search link to the project board.
- **Billy (aka Connor):** Request the new contributor to attribute AI usage, rename test files, and join the CAM meeting. *(review)*

## Proposals and objections

- **sliptonic** (objection): Objection/Concern regarding mixing output generation semantics with the capture of tool change semantics in the base post-processor.
- **Billy (aka Connor)** (proposal): Proposal to create a visual graph (Mermaid) of post-processor inheritance.
- **sliptonic** (proposal): Proposal to implement Cutter Location (CL) data as an intermediate representation to support lathe/mill-turn and improve efficiency.
- **Alan Grover** (proposal): Proposal to improve error messages for 'wire not closed' and 'not a DAG' errors to identify specific problematic elements.
- **Billy (aka Connor)** (proposal): Proposal to allow setting the work coordinate system directly in the work holding tab.
- **sliptonic** (proposal): Suggestion to try the work coordinate system change and demonstrate it rather than debating it theoretically.

---

An automated agent made this draft from a transcript of the meeting. A maintainer reviews it before publication.
