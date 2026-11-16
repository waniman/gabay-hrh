---
description: Add a work package to the project, e.g. "/new-work-package policy brief for the workforce bureau, concept-note playbook"
argument-hint: <title, type of work, and what it waits for>
---

Add a work package: $ARGUMENTS

Adding a work package changes the project's scope, so the lead decides (`core/escalation-threshold.md`, item 2). Follow `core/project-and-work-packages.md`.

1. **Playbook.** Match the type of work to a file in `playbooks/` (ignore `_template.md`). If none fits, say so and offer to draft one with `/new-playbook` first. Stop until a playbook exists.
2. **Propose it to the lead** in a memo (`python3 tools/team.py memo new --wp project --issue "Add a work package: <title>?"`). State:
   - the output, and the outcome in `project/results.md` it serves; if it serves none, the memo also proposes the change to the results chain;
   - the intended user and use;
   - the playbook, the deadline, and what it waits for from other work packages;
   - where it falls in the order of work, and what it does to the deadlines of the other work packages.
   If the lead asked for the work package in this conversation, in words that settle these points, record that answer as the decision and skip the memo.
3. **After the lead's answer is recorded**, create it:
   `python3 tools/team.py wp add --title "<title>" --type <playbook> --ref <EM-NNN or D-NNN> --waits-for "<WPn and what is needed>"`
   The tool refuses a reference that is not a decided memo or an approved register row.
4. **Fill in the files.** Write the work package's `brief.md` with the lead. Add the output to `project/results.md`. If the order of work changes, set the `Order:` line in `project/state.md` and log the decision.
5. **Add-ons.** If Drive sync is on, create the work package's subfolder (`addons/drive-sync/README.md`).
6. Commit "Add <WPn>: <title>" and push. The work package starts at the brief stage of its playbook when its turn comes in the order of work; set `Status: active` then.

Reply to the lead in two lines: the work package id and folder, and what happens next.
