---
description: Record the lead's answer to a memo or gate, e.g. "/decide EM-003 approve" or "/decide EM-004 option B, because the call excludes societal costs"
argument-hint: <memo id> <approve | option and reason | question>
---

The lead's answer: $ARGUMENTS

1. Open the memo named. If the answer is unclear (for example, it names an option the memo does not have), ask one short question and stop.
2. If the lead returns it with a question, answer the question in the memo under a "Follow-up" heading and keep the memo open.
3. Otherwise record it, following "Recording the answer" in `core/escalation-threshold.md`:
   - `python3 tools/team.py memo close --id <id> --decision "<the lead's words>" --by "<lead>"`
   - Update the register: approve the proposed row, or log the lead's choice as a new row and reverse the old one.
   - Close the matching tracker task if the tracker add-on is on.
4. Update `project/state.md`, and the state file of the work package the memo belongs to. If the answer approves the project frame or a new work package, follow `core/project-and-work-packages.md`. If the answer unblocks work, say what the next run will do.

Reply to the lead in one or two lines: what was recorded, with the register id.
