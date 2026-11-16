---
description: Draft a playbook for a new type of work, e.g. "/new-playbook systematic review"
argument-hint: <type of work>
---

Draft a new playbook for: $ARGUMENTS

Run this in the agent-team template repository, so every future project can use it.

1. Check `playbooks/`. If a playbook already fits, say so and stop.
2. Ask the lead three short questions, in one message:
   - What does a finished piece of this work look like, and who receives it?
   - Which steps does it always go through, in order?
   - At which points must the lead approve before work continues?
3. Look up the recognised standard for this kind of work, if one exists (for example PRISMA for systematic reviews, a funder's proposal guide, a journal's reporting guideline). Open it; do not rely on memory.
4. Draft `playbooks/<type>.md` from `playbooks/_template.md`. A playbook runs one work package: state the output it produces, its usual user, and the kind of outcome it serves. Then give the roles agents hold, evidence to check against, where the master copy lives at each stage, stages (who, do, done when, gate, checkpoint), a gates table, and any difference from the core rules with its reason. Keep the verification step after every evidence scan.
5. Show the lead a short summary: the stages, the gates, and anything that differs from the closest existing playbook (concept note for new writing, revision for work on an existing document). Ask for "go".
6. On "go", commit it ("Playbook: <type>") and push.

New playbooks also come from experience: the after-action review at the end of each project proposes changes to the playbook used, and the lead approves them before they are applied here.
