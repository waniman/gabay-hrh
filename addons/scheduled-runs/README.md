# Add-on: scheduled runs

Starts a run of the project every day at the time in `addons.scheduled_runs`, covering all its work packages in the order of work, so work moves while the lead is elsewhere and memos are waiting when the day begins.

**Needs:** a scheduling tool in the session that starts a new session on a schedule with the project repository attached.

## Setting it up (at project start, after the lead's "go")

Create one scheduled task:

- **Name:** `Agent team: <project repository>`
- **Schedule:** daily at `time`, in `timezone`
- **Prompt:** "Open the repository `<owner>/<repo>`. Follow its CLAUDE.md and run /continue. Never pass a gate, never answer a memo for the lead, and never create anything outside project/ without the lead's approval."

Record the scheduled task's id in `project/state.md` under Notes.

## Ending it

When the lead signs off the final version of the last work package, ask the lead whether to stop the daily run. Outcomes that arrive later are logged in a run the lead starts. On yes, delete the scheduled task and note it in the trace.

## Safeguards

- A scheduled run follows `core/run-rules.md`. If everything waits on the lead, it stops at once.
- On the health-check day (`health_check.day`), the scheduled run starts with the weekly health check, before any other work (`core/learning-and-oversight.md`). The health check runs even when everything else waits on the lead.
- It never passes a gate or takes an action that `CLAUDE.md` rule 4 holds for approval.
