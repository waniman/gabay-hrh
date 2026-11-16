---
description: Run the next piece of work on the project, following core/run-rules.md, e.g. "/continue" or "/continue WP2"
argument-hint: [work package]
---

Continue the project. Follow `core/run-rules.md` step by step:

1. Read `project/state.md`, the work packages (`python3 tools/team.py wp list`), the state file and playbook of each work package in progress, open memos, and memos answered since the last run. Record the answers. Follow the lessons in force. Run `python3 tools/team.py health --due`, and run the health check first if it is due (`core/learning-and-oversight.md`).
2. If everything remaining waits on the lead, stop and write `status.md`.
3. Otherwise take the first work package in the order of work that has a task waiting neither on the lead nor on another work package. If the lead named a work package below, start with that one. Continue its current stage until it ends, everything in it waits on a memo or on another work package, or the time limit in `team.config.yaml` is reached. At a gate, run the gate review before the gate memo is sent. When a work package stops before the time limit, move to the next one.
4. Checkpoint if a stage ended; send new memos through the add-ons; update the state files and `status.md`; commit and push.

Finish by telling the lead the Moved, Stopped, Waiting and Next lines of `status.md`, and the overall flag if a health check ran.

$ARGUMENTS
