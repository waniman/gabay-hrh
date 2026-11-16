Project: Gabay HRH
Started: 2026-11-16
Stage: frame
Lead: Juhani Capeding
Partners: Hazel Ivy M. Jeremias (ACRI; role on this team to be confirmed, EM-001); Municipality of Paracelis; DOH HHRDB; LGUs in talks for GabayHRH 2.0 (none committed)
Order: by number

## Work packages

Each work package keeps its own state in `project/wp/<WPn-name>/state.md`. `python3 tools/team.py wp list` prints them in the order of work, with stage, status, what each waits for, deadline and last checkpoint.

## Waiting on the lead

- EM-001. Gate: approve the project frame (needed by 2026-11-18). It also asks nine facts (2.0 funder and deadline, URC grant terms, ethics status, outcome dates, people, baseline version, style, overlap of the two tracks, repository privacy) and carries the compliance findings.

## Lessons in force

- None yet. Apply-now lessons the lead approves at a gate are copied here (`core/learning-and-oversight.md`).

## Notes for the next run

- Frame drafted on 2026-11-16 and sent as EM-001 (`project/brief.md`, `project/results.md`). Checkpoint `cp-project-frame-01`.
- After the lead approves: record the answer (`memo close`, D-004), set `Approved by the lead:` in the brief and the results chain, set `Stage: delivery`, create WP2 to WP5 with `wp add --ref EM-001` (or as the lead chooses), then start the WP1 brief stage. `project/wp/WP1-gabayhrh-2-0-proposal/brief.md` holds a first fill.
- The 2.0 draft in Drive (id `1-OqvCfhvrR9_0KpOYIZYVo-adgOhIeCK`) is edited by the ACRI team. Do not edit it. Compare its size and checksum with `project/sources/index.md` before any WP1 work, and ask the lead which version to freeze if it differs.
- Sources: the Drive connector reads text only. Binary copies of the URC proposal and the response to reviewers are not in the repository (`project/sources/index.md`).
- Branch: the project files are on `claude/hopeful-rubin-gntgwb`. They are not on `main` until the lead merges the branch. Memo links use the branch.
- Scheduled task: `trig_01THneWsQ4G79ZYBYridvaLq`, "Agent team: gabay-hrh", daily at 04:24 Asia/Manila, a new session at each run. It stores no connectors, so a scheduled run cannot reach Drive, Sheets or Docs; it logs the Drive sync as failed and leaves it for a run the lead starts. The lead can re-create it from the claude.ai routines page to add connectors.
- Compliance check on the frame: `project/reviews/compliance-frame-01.md`. Items 7.1 to 7.6 (policy instruments) go to the evidence checker at the first work package stage that cites them. The documents it lists as needed are asked of the lead in EM-001.
- Drive ids: `project/drive.json`. Register sheet tab `gabay-hrh`. The "All projects" tab keeps 14 columns; it shows this project's rows without the work package column.
- Tracker: task `agent-team-gabay-hrh-EM-001` on Juhani's Desk.
