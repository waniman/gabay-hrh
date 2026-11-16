# Escalation threshold

Six kinds of decision go to the project lead. All others are made by the team and logged in the register.

1. **Hard to reverse.** Anything that would be costly to undo once later work builds on it.
2. **Scope, central claim or budget.** Any change to what the work covers, what it argues, or what it costs or asks for. This includes adding, dropping or merging a work package, changing the results chain, and an assumption that fails (`core/project-and-work-packages.md`, `core/results-chain.md`).
3. **Authorship, ethics or a named stakeholder.** Who is credited; anything touching research ethics or consent; anything said about or committed on behalf of a funder, a government agency, a local government or a partner.
4. **Open disagreement.** Agents disagree and one round of resolution with evidence has not settled it.
5. **Uncertain.** The deciding agent marks its own decision as uncertain.
6. **Method.** A new analysis, an inferential test, or a change to how data are analyzed, before it runs. The memo states the sampling, the sample size and events per group, and the power or expected precision (`core/methods-rules.md`).

Approval gates set by a work package's playbook, and the project frame gate, also go to the lead, each as a memo whose issue starts with "Gate:", for example "Gate: approve the outline". The gate memo lists the lessons from the gate review (`core/learning-and-oversight.md`). Creations outside `project/` also go to the lead (rule 4 in `CLAUDE.md`). So do the proposed responses to each round of comments, in one memo per round (`core/comment-log.md`).

## Resolving a disagreement first

Give the agents involved one round: each states its position and its evidence in writing (in the work package's `reviews/` folder). If one position is better supported by evidence, decide and log it. If not, escalate with both positions side by side.

## Timing

- **Batched (default).** Collect memos during a stage and send them together when the stage ends.
- **Urgent.** Send at once when work cannot continue without the answer, or a deadline is less than 48 hours away. Use `memo new --urgent`.

Work that does not depend on a pending answer continues while it waits.

## Writing the memo

```
python3 tools/team.py memo new --wp WP2 --issue "Use a health system or societal costing perspective?"
```

A project with one work package needs no `--wp`; a memo on the project as a whole takes `--wp project`. Fill in the file it creates (`project/escalations/EM-NNN.md`) following `core/decision-memo-template.md`. Always set the "Needed by" date; the weekly health check flags memos without one. Then log the decision with `--status proposed --escalated EM-NNN`, and send the memo through the switched-on add-ons.

## Recording the answer

When the lead answers (in chat, in the memo file, or in the tracker task):

1. `python3 tools/team.py memo close --id EM-NNN --decision "<the lead's words>" --by "<lead's name>"`
2. Update the register row: approved, or a new row for a different choice plus `register reverse`.
3. Note it in the trace and in the state files.
