# Add-on: tracker task

Turns each decision memo and each gate into a task in the lead's own task tracker, so decisions reach the lead where they already work. The memo file stays the record.

**Needs:** a tool in the session that can write to the tracker named in `addons.tracker_task.tracker`. For a claude.ai artifact that keeps its data in a database, use the artifact data tools (list the collections, read a few existing tasks, write a new one in the same shape).

## First use

1. Open the tracker and read a few existing tasks to learn their fields.
2. Propose a mapping to the lead in a short table:
   - title: `<EM-NNN> (<WPn>): <issue>` (or `Gate (<WPn>): approve the <stage>`); a memo on the project as a whole carries no work package
   - link: the memo file on GitHub, `https://github.com/<owner>/<repo>/blob/main/project/escalations/EM-NNN.md`
   - due date: the memo's "Needed by"
   - priority or flag: urgent memos marked urgent
   - project or tag: the project name
3. After the lead agrees, record the mapping in `team.config.yaml` under `mapping`, so later runs do not ask again.

## For each memo or gate

- Create the task when the memo is sent (batched or urgent).
- When the lead answers, through the task, chat or the memo file, record the answer as `core/escalation-threshold.md` sets out, then mark the task done.
- If the lead answers in the tracker, copy their words into the memo exactly.

## Weekly health check

- Create one item for each digest: `Weekly health check: <overall>. <count> red flag(s). Open project/health/<date>.md.`, with the link to the digest file. No due date.
- Mark the previous week's item done when the new one is created.
- A recommendation that needs the lead's decision becomes its own memo, and so its own task.

## If it fails

The memo file still stands. Note the failure in the trace and in `status.md`, and list the memo in the run's final message to the lead.
