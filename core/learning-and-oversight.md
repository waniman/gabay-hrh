# Learning and oversight during a project

Two routines run while a project is under way:

- **Gate lessons.** At each approval gate of a work package, the after-action reviewer reviews that work package's stages since its last gate and records up to three lessons. The team learns during the project as well as at the end.
- **Weekly health check.** Once a week, a tool computes pacing and process measures for the project and each work package, and a process monitor that does not share the coordinator's context reads them. The coordinator's own work is checked this way.

Approved by the lead on 2026-11-10 (`proposals/2026-11-10-gate-lessons-and-weekly-health-check.md`).

## Gate lessons

### When does a gate review run?

At every gate a work package's playbook names, after the checkpoint before the gate is saved and before the gate memo is sent. On a revision, the triage and final gates repeat each round, so a review runs at each of them. The project frame gate has no gate review, because no stage comes before it.

### How does the coordinator run it?

1. Call the after-action reviewer in **gate mode**. Pass it the work package and its folder, the gate name, the checkpoint of that work package's previous gate (or none at its first gate), and the checkpoint just saved.
2. The reviewer appends one entry to `project/lessons.md`. It never edits the playbook, core files or the work.
3. List the entry's lessons in the gate memo, on the line "Lessons at this gate" (`core/decision-memo-template.md`). An entry with no lessons is listed as "none".
4. A lesson that touches scope, the central claim, budget, authorship, ethics or method gets its own memo under `core/escalation-threshold.md`. It is not approved with the gate.

### What kinds of lesson are there?

- **Apply now.** A change to how the team works for the rest of this project, such as an extra source to check or a different order of tasks. The lesson says whether it applies to one work package or to all of them.
- **Carry forward.** A change to the playbook or core rules for future projects. It waits in `lessons.md` for the final after-action review.

### What happens when the lead answers the gate memo?

- For each **apply now** lesson the lead approves, log a register row (work package: the gate's work package, or `project` when the lesson applies to all; stage: the gate's stage; decision: "Apply lesson L-NN for the rest of the project?"; escalated: the gate memo). Copy the lesson into the "Lessons in force" section of `project/state.md`, with the work packages it applies to, so every later run follows it.
- Set each lesson's status in `lessons.md`: `approved`, `rejected` or, for carry-forward lessons, `carried`.
- A lesson takes effect only after the lead's approval is recorded in the register.

### What does an entry look like?

```
## Gate: WP2 outline (2026-11-05). Stages reviewed: 2 Evidence, 3 Outline. Checkpoints: cp-wp2-brief-01 to cp-wp2-outline-01

1. Plan: ...
2. What happened: ...
3. Why: ...

| # | Kind | Lesson | Basis | Status |
| --- | --- | --- | --- | --- |
| L-01 | Apply now | For the rest of this project, the evidence checker opens the primary source of any figure taken from a review article. | D-009, reviews/verification-01.md | proposed |
| L-02 | Carry forward | Add to the scan step of concept-note.md: "Cite the primary source of every figure." | Same | proposed |
```

Lesson ids run through the whole project, across work packages: L-01, L-02 and so on, never reused.

## Weekly health check

### When is a health check due?

On the weekday set in `team.config.yaml` (`health_check.day`, Monday by default). The coordinator asks the tool at step 1 of every run:

```
python3 tools/team.py health --due
```

A check is due on the health-check day, unless a digest was already saved that day. If that day was missed, the check is due at the next run once the last digest is more than seven days old.

### How does the coordinator run it?

The health check comes before any other work in the run.

1. Save the facts:
   `python3 tools/team.py health --out project/health/<YYYY-MM-DD>-facts.md`
2. Call the process monitor with exactly four paths: the facts file, `project/state.md`, `project/brief.md` and `project/register/decisions.csv`. Never pass the trace, memo drafts or your own notes.
3. The process monitor writes `project/health/<YYYY-MM-DD>.md`. Do not edit it.
4. Send the digest:
   - **Tracker add-on:** one item, "Weekly health check: <overall>. <count> red flag(s). Open project/health/<date>.md."
   - **Phone add-on:** only when the overall flag is red. One line naming the red flag.
5. Act on the recommendations. A recommendation that needs the lead's decision becomes a memo under `core/escalation-threshold.md`. Anything else is done in the run and logged in the register.
6. Note the health check in the trace and in `project/state.md`.

### What does the tool measure?

`team.py health` reads only the project files. It uses fixed rules, so its results do not depend on the coordinator's judgment. The facts file opens with a table of the work packages: playbook, stage, status, what each waits for, deadline and last checkpoint. Measures marked "each work package" give one row for each work package whose status is active or waiting.

| Measure | Read from | Amber | Red |
| --- | --- | --- | --- |
| Memos past "Needed by" | `escalations/` | 1 day past | 5 days past |
| Open memos with no "Needed by" date | `escalations/` | Any | |
| Gates waiting on the lead (memos whose issue starts "Gate:") | `escalations/` | 5 days | 10 days |
| Each work package: days since its last checkpoint, with tasks open | git tags, `<wp>/state.md` | 7 days | 14 days |
| Runs in a row that moved nothing, not counting runs that stopped because everything waits on the lead | history of `status.md` | 2 | 4 |
| Runs in a row that hit the time limit on one task | history of `status.md` | 2 | 3 |
| Agent decisions marked "not reversible", logged without a memo | register | | Any |
| Register rows left "proposed" with no memo | register | Any | |
| `register check` errors | register, comment log, sent log, outcome log | | Any |
| Comments still open in a round the lead has already decided | comment log | Any | |
| Each work package: days to the current stage's due date, when its `state.md` has a `Due:` line | `<wp>/state.md` | Fewer than 3 | Fewer than 1.5 |
| Otherwise, each work package: days to its brief's deadline, per stage left | `<wp>/brief.md`, playbook | Fewer than 3 | Fewer than 1.5 |
| Work packages past their brief's deadline and not signed off, started or not | `<wp>/brief.md`, `<wp>/state.md` | 1 day past | 7 days past |
| Work packages waiting on another work package (`Status: waiting (since <date>)`) | `<wp>/state.md` | 7 days | 14 days |
| Outcomes whose `By:` date has passed with no row in the outcome log | `results.md`, outcome log | Any | |

The thresholds are set in `team.config.yaml` under `health_check`. A work package whose status is waiting with no date on the line is flagged amber. The stages-left count follows the work package's playbook from its current stage to sign-off. On a revision, a further round of comments adds stages that the count cannot foresee.

These measures depend on files the team already keeps, so keep them exact:

- Fill the "Needed by" date in every memo.
- Start the issue of every gate memo with "Gate:" (`core/escalation-threshold.md`).
- Write the `Stopped:` line of `status.md` in every run (`core/run-rules.md`).
- Keep the `Status:` line of each work package's state file current, with the date when it is waiting (`core/project-and-work-packages.md`).
- End each outcome in `results.md` with `By: YYYY-MM-DD` (`core/results-chain.md`).

### What does the digest look like?

```
# Health check, 2026-11-16

Project: <name>. Stage: delivery.

**Overall: amber.** One sentence on the state of the project.

| Measure | Value | Flag |
| --- | --- | --- |
(the rows of the facts file)

## Recommendations

1. **D-021.** The coordinator should raise a memo. Dropping the provincial comparison changes scope (escalation item 2) and was logged as not reversible.

Next health check: 2026-11-23.
```

A week with no flags gets a one-line digest: "**Overall: green.** No flags. Next check on <date>."
