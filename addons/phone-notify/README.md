# Add-on: phone notification

Sends a short alert to the lead's phone when a memo is urgent (work cannot continue without the answer, or a deadline is less than 48 hours away), and when a weekly health check is red. Batched memos and green or amber health checks never trigger an alert.

**Needs:** a push notification tool in the session (in Claude Code, the push notification tool).

## Message

One line, under 120 characters:

`<project> <WPn>: <EM-NNN> needs your decision by <date>. <issue, shortened>`

Leave out the work package for a memo on the project as a whole.

For a red health check:

`<project>: health check red. <the red flag, shortened, e.g. D-021 changed scope without a memo>`

## Rules

- At most one alert per memo, and one per red health check.
- No alerts for routine status, checkpoints or batched memos.
- If the tool is not available, note it in the trace and put the memo at the top of the run's final message.
