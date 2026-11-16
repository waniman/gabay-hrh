Project: Gabay HRH
Started: 2026-11-16
Stage: delivery
Lead: Juhani Capeding
Partners: Hazel Ivy M. Jeremias (ACRI; role on this team to be confirmed, EM-001); Municipality of Paracelis; DOH HHRDB; LGUs in talks for GabayHRH 2.0 (none committed)
Order: by number

## Work packages

Each work package keeps its own state in `project/wp/<WPn-name>/state.md`. `python3 tools/team.py wp list` prints them in the order of work, with stage, status, what each waits for, deadline and last checkpoint.

## Waiting on the lead

- Nothing open. EM-001 (project frame) approved on 2026-11-16 (D-004, D-005, D-006). The WP1 brief gate memo goes out once the DOH guide scan is verified.

## Work packages approved in the frame, not yet created

WP2 Paracelis LGU HRH diagnostic profile; WP3 Guide for LGU health workforce planning and investment; WP4 Journal article (journal-article playbook); WP5 Policy brief. `wp add` needs a playbook for each, and WP2, WP3 and WP5 have none. Create all four together, in this order, once their playbooks exist, so the numbers match the frame (EM-001). Each waits for the pilot's data in 2027.

## Lessons in force

- None yet. Apply-now lessons the lead approves at a gate are copied here (`core/learning-and-oversight.md`).

## Notes for the next run

- Frame approved 2026-11-16 (EM-001). Checkpoint `cp-project-frame-02`. Stage: delivery.
- WP1 is at its brief stage. Open: the evidence scan on the DOH guide for LGUs (D-006), its verification by a separate call, then the brief gate memo (EM-002) with the facts EM-001 asked and the lead did not supply: 2.0 funder and deadline, URC grant terms, ethics status, Hazel Jeremias's role, holder of the master copy, baseline version, how the two tracks share staff and costs, repository privacy.
- The lead's answer "Agree with all" is read as approving every proposal in EM-001: Option A, the brief fixes, the AI-use section, the three outcome dates, APA 7th edition and `<name>_v<YYYY-MM-DD>`. The O3 wording is kept as written.
- The 2.0 draft in Drive (id `1-OqvCfhvrR9_0KpOYIZYVo-adgOhIeCK`) is edited by the ACRI team. Do not edit it. Compare its size and checksum with `project/sources/index.md` before any WP1 work, and ask the lead which version to freeze if it differs.
- Sources: the Drive connector reads text only. Binary copies of the URC proposal and the response to reviewers are not in the repository (`project/sources/index.md`).
- Branch: the project files are on `claude/hopeful-rubin-gntgwb`. They are not on `main` until the lead merges the branch. Memo links use the branch.
- Scheduled task: `trig_01THneWsQ4G79ZYBYridvaLq`, "Agent team: gabay-hrh", daily at 04:24 Asia/Manila, a new session at each run. It stores no connectors, so a scheduled run cannot reach Drive, Sheets or Docs; it logs the Drive sync as failed and leaves it for a run the lead starts. The lead can re-create it from the claude.ai routines page to add connectors.
- Compliance check on the frame: `project/reviews/compliance-frame-01.md`. Items 7.1 to 7.6 (policy instruments) go to the evidence checker at the first work package stage that cites them. The documents it lists as needed are asked of the lead in EM-001.
- Drive ids: `project/drive.json`. Register sheet tab `gabay-hrh`. The "All projects" tab keeps 14 columns; it shows this project's rows without the work package column.
- Tracker: task `agent-team-gabay-hrh-EM-001` on Juhani's Desk.
