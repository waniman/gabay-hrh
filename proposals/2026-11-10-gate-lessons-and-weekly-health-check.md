# Proposals: lessons at each gate and a weekly health check

Status: approved by the lead on 2026-11-10, as recommended. Applied on branch `claude/hopeful-shannon-qcqrg4`.
Date: 2026-11-10
Prepared by: coordinator, at the lead's request
Applies to: the agent-team template repository (`playbooks/`, `core/`, `.claude/agents/`, `tools/`, `project-template/`)

## What is being asked?

The lead is asked to approve, amend or reject two changes to the template:

1. **Proposal A, gate lessons.** A short lessons review at each approval gate, so the team learns during a project as well as at the end.
2. **Proposal B, weekly health check.** A weekly check of pacing and process, run by a call that does not share the coordinator's context, so the coordinator's own work is also checked.

Both proposals leave the six rules in `CLAUDE.md` unchanged. Neither proposal lets an agent pass a gate, answer a memo or edit a playbook during a project.

No file outside `proposals/` has been edited. The edits listed under each proposal are applied only after the lead approves them.

## Why are these changes needed?

Learning currently happens once. The after-action reviewer runs only after sign-off (`playbooks/concept-note.md`, stage 8; `playbooks/revision.md`, stage 10). On a project that runs for several months, a lesson from the evidence stage reaches the playbook only after the final version is approved. The current project cannot use it.

Oversight of the coordinator rests with the lead alone. The coordinator calls and checks every other agent (`CLAUDE.md`, "The team"). The only checks on the coordinator's pacing and judgment are `status.md` and the memos, and the coordinator writes both. `CLAUDE.md` rule 5 states that "a second opinion from an agent with the same context is not a check." No independent check of the coordinator exists today.

---

## Proposal A: What would a lessons review at each gate add?

### What would happen?

At each approval gate, before the gate memo goes to the lead, the after-action reviewer runs in a new **gate mode**. It reviews only the stages completed since the last gate. It writes one entry, of no more than one page, in a running file, `project/lessons.md`.

Each entry answers the same four questions as the final review, kept short:

1. What was supposed to happen in these stages?
2. What happened?
3. Why was there a difference?
4. What should change?

Each lesson is sorted into one of two kinds:

- **Apply now.** A change to how the team works for the rest of this project, such as an extra source to check or a different order of tasks. It is listed in the gate memo, and the lead approves it with the gate. A lesson that touches scope, the central claim, budget, authorship, ethics or method follows the escalation threshold (`core/escalation-threshold.md`) and gets its own memo.
- **Carry forward.** A change to the playbook or core rules for future projects. It waits in `lessons.md`. The final after-action review reads every carry-forward lesson and decides which to propose.

### What limits would apply?

- No more than three lessons per gate. An entry with no lesson says "No lessons at this gate" in one line.
- Each lesson cites the register ids, memo ids or review files it rests on.
- The reviewer never edits the playbook, core files or the work.
- An "apply now" lesson takes effect only after the lead's approval is recorded in the register.

### Example: an outline gate on a concept note

This example is illustrative. The project, ids and counts are hypothetical.

> **Gate: outline. Project: task-shifting cost study (hypothetical). Stages reviewed: 2 Evidence, 3 Outline.**
>
> 1. **Plan.** The evidence scan was to find verified figures for every claim the brief needs, then the writer was to build the outline.
> 2. **What happened.** The verify call corrected 4 of 11 claims (`reviews/verification-01.md`). Three of the four came from one secondary review, which had misquoted the national survey. The outline was written in one pass.
> 3. **Why.** The scan took figures from the secondary review without opening the primary source it cited.
> 4. **Lessons.**
>
> | # | Kind | Lesson | Basis |
> | --- | --- | --- | --- |
> | L-01 | Apply now | For the rest of this project, the evidence checker opens the primary source of any figure taken from a review article. | D-009, `reviews/verification-01.md` |
> | L-02 | Carry forward | Add to the scan step of `concept-note.md`: "Cite the primary source of every figure. A review article is cited for its own synthesis only." | Same |

The gate memo would then carry one extra line: "Lessons at this gate: L-01 (apply now, approve with the outline); L-02 (carried to the after-action review)."

### Example: a triage gate on a revision

This example is also hypothetical.

> **Gate: triage. Stages reviewed: 2 Diagnose, 3 Log and triage.**
>
> | # | Kind | Lesson | Basis |
> | --- | --- | --- | --- |
> | L-03 | Apply now | Log untracked edits found by comparing the returned file with the sent copy before triage starts. In this round, 6 untracked edits were found after the triage memo was drafted, and the memo had to be redone. | EM-004, `comments.csv` rows C-031 to C-036 |
> | L-04 | Carry forward | None. | |

### Which files would change?

| # | File | Change |
| --- | --- | --- |
| A1 | `.claude/agents/after-action-reviewer.md` | Add a gate mode: inputs, the four short questions, the three-lesson limit, the two kinds of lesson, and output to `project/lessons.md`. |
| A2 | `playbooks/concept-note.md`, `playbooks/revision.md`, `playbooks/_template.md` | At each gate, add the step "Run the after-action reviewer in gate mode; list its lessons in the gate memo." |
| A3 | `playbooks/concept-note.md` stage 8, `playbooks/revision.md` stage 10 | The final review reads `project/lessons.md` and states what happened to each carry-forward lesson. |
| A4 | `core/decision-memo-template.md` | Add an optional line: "Lessons at this gate: (ids and kind)." |
| A5 | `project-template/lessons.md` | New file with a header and an empty entry. |

### What would it cost?

One extra agent call at each gate. That is three calls on a concept note and four on a revision. The gate memo grows by one line.

---

## Proposal B: How would a weekly health check oversee the process?

### What would happen?

Once a week, the scheduled run starts with a health check before any other work. It has two parts.

1. **Facts, computed by a tool.** A new command, `python3 tools/team.py health`, reads the project files and lists the measures in the table below. It uses fixed rules, so the coordinator cannot shade the result.
2. **A reading, by an independent call.** A fresh **process monitor** agent sees only the tool output, `state.md`, `brief.md` and the register. It does not see the coordinator's trace or reasoning. It writes `project/health/<YYYY-MM-DD>.md`: what is on track, what is flagged, and one recommendation for each flag.

The coordinator then sends the digest to the lead's tracker as a single item. A flag that needs the lead's decision becomes a memo under the usual threshold. A red flag also goes to the phone, through the phone-notify add-on. Green and amber items do not.

### What would the check measure?

The thresholds below are proposed defaults. The lead can change them in `team.config.yaml`.

| Measure | Amber | Red |
| --- | --- | --- |
| Memo open past its "Needed by" date | 1 day past | 5 days past |
| Gate waiting on the lead | 5 days | 10 days |
| Days since the last checkpoint while tasks are open | 7 days | 14 days |
| Scheduled runs in a row that moved nothing | 2 | 4 |
| Runs in a row that hit the time limit on the same task | 2 | 3 |
| Agent decisions marked "not reversible" and logged without a memo | | Any |
| Register rows left "proposed" with no memo | Any | |
| `register check` errors | | Any |
| Comments open after their round's triage memo was decided | Any | |
| Days to the next deadline in the brief, against stages left | Fewer than 3 days per stage left | Fewer than 1.5 days per stage left |

Two of these measures check the coordinator directly:

- **Decisions logged without a memo** tests whether the coordinator kept to the escalation threshold. A "not reversible" decision made by an agent should have reached the lead (`core/escalation-threshold.md`, item 1).
- **Runs that moved nothing, or hit the time limit on the same task** tests whether the coordinator is stuck and not reporting it.

### Example: a weekly digest

This example is illustrative. The project, ids, dates and counts are hypothetical.

> **Health check, 2026-11-16. Project: task-shifting cost study (hypothetical). Stage: draft.**
>
> **Overall: amber.** Work is moving. One memo is overdue, and one decision should have reached the lead.
>
> | Measure | Value | Flag |
> | --- | --- | --- |
> | Memos past "Needed by" | EM-006, 2 days past | Amber |
> | Gates waiting | None | Green |
> | Days since last checkpoint | 4 (`cp-outline-01`) | Green |
> | Runs in a row that moved nothing | 0 | Green |
> | Runs hitting the time limit on one task | 2 (section 3 costing table) | Amber |
> | Non-reversible agent decisions without a memo | D-021: "Drop the provincial comparison" | Red |
> | Days to deadline per stage left | 31 days, 4 stages left: 7.8 per stage | Green |
>
> **Recommendations**
>
> 1. **D-021.** The coordinator should raise a memo. Dropping the provincial comparison changes scope (escalation item 2) and was logged as not reversible.
> 2. **EM-006.** The coordinator should resend the memo with the decision it blocks: the costing table in section 3.
> 3. **Section 3.** The coordinator should split the costing table into two tasks so that a run can finish one of them.

The tracker item would read: "Weekly health check: amber. 1 red flag (D-021 needs a memo). Open `project/health/2026-11-16.md`." Because one flag is red, the phone alert would read: "Health check: a scope decision (D-021) was made without your approval."

### Example: a quiet week

> **Health check, 2026-11-23. Overall: green.** No flags. Next check on 2026-11-30.

A quiet week produces a tracker item but no phone alert.

### Which files would change?

| # | File | Change |
| --- | --- | --- |
| B1 | `tools/team.py` | Add `health`, which prints the measures and flags as Markdown, with thresholds read from `team.config.yaml`. Python standard library only, like the rest of the tool. |
| B2 | `.claude/agents/process-monitor.md` | New agent with Read and Write access only. It writes only to `project/health/`. Its inputs are the tool output, `state.md`, `brief.md` and the register. It never sees the trace. |
| B3 | `core/run-rules.md` | Add: "On the health-check day, the first scheduled run calls `team.py health`, then the process monitor, before any other work." |
| B4 | `addons/scheduled-runs/README.md`, `addons/tracker-task/README.md`, `addons/phone-notify/README.md` | Describe the weekly digest item and the rule that only red flags go to the phone. |
| B5 | `team.config.example.yaml` | Add a `health_check` block with `day: Monday` and the thresholds. |
| B6 | `CLAUDE.md` | Add the process monitor to "The team" table. Capability: Stewardship. |
| B7 | `project-template/health/` | New, empty folder. |

### What would it cost?

One tool run and one agent call each week. On a project of four months, that is about 17 calls. A quiet week adds one tracker item.

---

## Which decisions are the lead's, and which can be delegated?

### For the lead's decision

1. **Approve, amend or reject Proposal A.**
2. **Approve, amend or reject Proposal B.**
3. **Proposal B: who reads the facts.** The recommendation is a new process-monitor agent. The alternative is to reuse the after-action reviewer in a third mode. A separate agent keeps the Renewal role and the oversight role apart, and its narrow inputs make it independent of the coordinator.
4. **Proposal B: the red-flag rule.** Should a red flag alert the phone? The recommendation is yes, for red flags only.

### Delegable to the coordinator once approved

- The exact wording of the playbook and core edits listed in A1 to A5 and B1 to B7.
- Tests for `team.py health`.
- The default thresholds. The lead can change them in `team.config.yaml` at any time.

## How would the lead answer?

Reply in chat, for example:

- "Approve A and B as recommended."
- "Approve A. Approve B with the health check on Friday and memo thresholds of 2 and 7 days."
- "Approve A. Hold B."

After an approval, the coordinator applies the edits in this repository on a branch and lists the changed files for review before merging.

## What did the lead decide?

On 2026-11-10 the lead answered:

1. Proposal A: approved as recommended.
2. Proposal B: approved as recommended.
3. Who reads the facts: a new process-monitor agent. Agreed.
4. Red flags to the phone: yes, red flags only. Agreed.

## What was applied?

The rules are in `core/learning-and-oversight.md`. Edits A1 to A5 and B1 to B7 were applied as listed, with three additions the measures need:

- Gate memos start their issue with "Gate:", so the tool can tell how long a gate has waited (`core/escalation-threshold.md`).
- `status.md` grows from three lines to five: `Run:` and `Stopped:` are added, so the tool can count runs that moved nothing and runs that hit the time limit (`core/run-rules.md`).
- `state.md` gains a "Lessons in force" section, so approved apply-now lessons reach every later run (`project-template/state.md`).

A memo with no "Needed by" date is flagged amber, so every memo carries one.

