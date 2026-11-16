# Projects and work packages

A project holds one or more work packages. Each work package follows one playbook and delivers one or more outputs. The project keeps one lead, one decision register, one comment log, one sent log, one outcome log, one set of memos, one lessons file and one weekly health check.

Approved by the lead on 2026-11-10 (`proposals/2026-11-10-work-packages-and-results-chain.md`).

## Terms

| Term | Meaning |
| --- | --- |
| Project | The whole undertaking the lead owns. One repository, one `project/` folder. |
| Work package | A substantial part of the project's work, following one playbook. Numbered WP1, WP2 and so on; a number is never reused. |
| Output | A product the project delivers: a concept note, a report, a manuscript, a dataset. |
| Project frame | The project brief, the list of work packages and the results chain, approved together before work starts. |

Outcomes, impact and assumptions are defined in `core/results-chain.md`.

A project with a single output has one work package, WP1. The rules below are the same for one work package or several.

## Where files live

```
project/
  state.md                 the project: stage, lead, partners, order of work, what waits on the lead, lessons in force
  status.md                five lines after each run
  brief.md                 the project brief
  results.md               the results chain
  lessons.md               lessons from each gate review
  after-action.md          the review at project close
  register/                decisions.csv, comments.csv, sent.csv, outcomes.csv
  reviews/                 checks of the project frame
  escalations/  health/  sources/  trace/
  wp/
    WP1-<short-name>/
      brief.md             what this work package delivers, for whom, and by when
      state.md             title, playbook, stage, status, what it waits for, master copy, open tasks
      work/                outline, drafts, evidence file, final version; frozen/ and sent/
      reviews/             evidence checks, blind reviews, compliance checks
      after-action.md      the review at this work package's sign-off
```

In playbooks, agent instructions and the other core files, `<wp>/` stands for the folder of the work package in hand, for example `project/wp/WP2-concept-note/`. When the coordinator calls an agent, it gives the full path.

## The project's stages

1. **Frame.** With the lead, write the project brief (`project/brief.md`), the list of work packages and the results chain (`project/results.md`). The compliance check reads the funder's rules that apply to the whole project, and writes its review in `project/reviews/`.
   - **Gate:** the lead approves the project frame in one memo, issue "Gate: approve the project frame". The memo lists each work package with its playbook, output, the outcome it serves, what it waits for and its deadline.
   - **Checkpoint:** `python3 tools/team.py checkpoint --wp project --stage frame`, giving `cp-project-frame-NN`.
   - After approval, set `Stage: delivery` in `project/state.md`, and create each further work package with `wp add` (below).
2. **Delivery.** Each work package runs through the stages and gates of its playbook.
3. **Close.** After the last work package is signed off, the after-action reviewer runs in final mode for the project (`.claude/agents/after-action-reviewer.md`). It reports on the outcomes observed, not observed and not yet observable, and on each assumption. Set `Stage: close`, and save `cp-project-close-NN`.

On a project with one work package, the frame is short: the project brief and the results chain take a page each, and the work package brief holds the detail. The frame gate and the work package's brief gate may go to the lead in one memo.

## The work package's state file

`<wp>/state.md` holds the lines the tool reads. Keep their labels exact.

| Line | Content |
| --- | --- |
| `Work package:` | WP1, WP2 and so on |
| `Title:` | A short name for the work package |
| `Type:` | The playbook it follows |
| `Started:` | The date it was created |
| `Stage:` | The current stage of its playbook |
| `Status:` | `planned`, `active`, `waiting (since YYYY-MM-DD)`, `signed off (YYYY-MM-DD)` or `dropped (YYYY-MM-DD)` |
| `Waits for:` | What it needs from another work package, for example `WP1 evidence file (cp-wp1-evidence-01)`, or `none` |
| `Master copy:` | The one copy the team edits, and who holds it (`core/documents.md`) |
| `Due:` | Optional: the current stage's due date |

The work package's deadline is the `- Deadline:` line of its brief. The file also holds the "Open tasks" list and "Notes for the next run".

- **planned:** approved in the frame, not yet started.
- **active:** work is under way.
- **waiting:** it stopped because it needs something from another work package. Write the date it stopped. The health check counts the days.
- **signed off:** the lead approved its final version.
- **dropped:** the lead removed it from the project. Its folder and its register rows stay.

## Adding, dropping or merging a work package

Each of these changes scope, so each goes to the lead (`core/escalation-threshold.md`, item 2).

- **Add.** After the lead's answer is recorded:
  `python3 tools/team.py wp add --title "<title>" --type <playbook> --ref <EM-NNN or D-NNN> --waits-for "<WPn and what is needed>"`
  The tool refuses a reference that is not a decided memo or an approved register row. Then fill the work package's brief, and add its output to `project/results.md`.
- **Drop.** Set `Status: dropped (<date>)` and note the memo. Never delete the folder.
- **Merge.** Drop one work package and widen the brief of the other, in one memo.

If no playbook fits the work package's type of work, draft one with `/new-playbook` before the work package starts.

## The order of work

- Work packages are worked in number order, unless `project/state.md` has an `Order:` line that lists them in another order, for example `Order: WP2, WP1, WP3`. The lead approves the order in the frame; changing it is a decision for the register.
- A run takes the first work package, in that order, with a task that waits neither on the lead nor on another work package. When that work package stops, the run moves to the next one until the time limit (`core/run-rules.md`).
- `python3 tools/team.py wp list` prints the work packages in the order of work, with stage, status, what each waits for, deadline and last checkpoint.

## Dependencies between work packages

- Write what a work package needs on the `Waits for:` line of its state file and in its brief, naming the other work package and, once it exists, the checkpoint that provides it.
- A finding verified in one work package may be cited in another. Cite it by its id and the file that holds it, for example `E-014 in project/wp/WP1-evidence-summary/work/evidence.md`. A finding still marked first pass may not be cited anywhere.
- A work package never edits another work package's files. It reads them at a named checkpoint.
- When a work package stops for another, set its status to `waiting (since <date>)`. When the wait ends, set it back to `active`.

## Naming the work package in commands

Commands that act on one work package take `--wp WPn`: `register add`, `comment add`, `comment import`, `sent add`, `memo new`, `checkpoint` and `rollback`. A project with one work package needs no `--wp`. Use `--wp project` for a decision, comment, memo or checkpoint that belongs to the project as a whole: the frame, the results chain, the order of work, the close.

## Using the team's independent checks

The limits on what each checking agent may read stay as `CLAUDE.md` rule 5 sets them, applied to one work package at a time:

- The blind reviewer receives the draft and `<wp>/brief.md` only. The work package brief therefore states the intended user and use in full.
- The evidence checker in verify mode receives the claim list only.
- The process monitor receives the facts file, `project/state.md`, `project/brief.md` and the register. The facts file carries the table of work packages.
