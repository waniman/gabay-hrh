# Runs

The team works only while a session runs. A run is one session of work on the project, started by the lead ("continue the concept note", `/continue`) or by a scheduled task.

## Each run

1. Read `project/state.md`, the work packages (`python3 tools/team.py wp list`), the state file and playbook of each work package in progress, open memos and memos the lead has answered since the last run. Record each answer (see `core/escalation-threshold.md`). If the Drive add-on is on, also read new comments on the mirrored Docs and new files in the Sources inbox (`addons/drive-sync/README.md`).
   - Check the `Master copy:` line of each work package you will work on. If this session does not hold the master, do not edit it; propose changes to the holder (`core/documents.md`).
   - If a reviewed file has come back, compare it with the copy that was sent and log what it holds in the comment log, before any other work on that round.
   - Follow the "Lessons in force" in `project/state.md`.
   - If an outcome's date in `project/results.md` is near or past, ask the lead whether a signal was seen, and log what is reported (`core/results-chain.md`).
   - Run `python3 tools/team.py health --due`. If a health check is due, run it before any other work (`core/learning-and-oversight.md`).
2. If every remaining task waits on the lead, stop at once: write `status.md`, commit and push it, and change nothing else.
3. Take the first work package, in the order of work, that has a task waiting neither on the lead nor on another work package (`core/project-and-work-packages.md`). Continue its current stage until one of these happens:
   - the stage ends, and the next stage starts with a gate (run the gate review before the gate memo is sent: `core/learning-and-oversight.md`);
   - every remaining task of that work package waits on a memo or on another work package;
   - the run's time limit in `team.config.yaml` is reached.

   When a work package stops before the time limit, move to the next one in the order of work. Work on one work package at a time.
4. Save a checkpoint if a stage ended (`core/checkpoint-rules.md`).
5. Send new memos through the switched-on add-ons.
6. Update the state files. In each work package worked on, `<wp>/state.md`: stage, status, open tasks, notes for the next run. In `project/state.md`: what waits on the lead, lessons in force, notes for the next run.
7. Write `status.md` in five lines:
   - Run: the date and time the run started, and how (`scheduled` or `by the lead`)
   - Moved: what changed in this run, naming each work package, or `nothing.`
   - Stopped: `stage end`, `waiting on the lead`, or `time limit (<the work package and task in progress>)`
   - Waiting on the lead: memos and gates, by id
   - Next: what the next run will do

   The weekly health check reads these lines from the history of `status.md`, so keep their labels exact.
8. Commit and push.

## Scheduled runs

A scheduled run follows the same steps. It never passes a gate, never answers a memo for the lead, and never takes an action that rule 4 in `CLAUDE.md` holds for approval. If it hits one, it writes the memo and stops that line of work.

## State files

The state files are the hand-over between runs. Keep them short and current.

- `project/state.md` holds the project name, start date, stage (`frame`, `delivery` or `close`), lead, partners, the order of work, what waits on the lead, lessons in force, and notes for the next run. The tool reads the `Project:`, `Stage:` and `Order:` lines; keep their labels exact and `Project:` as the first line.
- `<wp>/state.md` holds one work package's title, playbook, stage, status, what it waits for, the master copy and who holds it, the stage's due date where the playbook dates its stages, open tasks, and notes for the next run. The tool reads the `Title:`, `Type:`, `Started:`, `Stage:`, `Status:`, `Waits for:`, `Master copy:` and `Due:` lines and the "Open tasks" list (`core/project-and-work-packages.md`).
