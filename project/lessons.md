# Lessons

Lessons from the gate reviews, one entry per gate, newest last. The after-action reviewer writes each entry in gate mode; the coordinator updates the status of each lesson after the lead answers the gate memo. Rules and format: `core/learning-and-oversight.md`.

Kinds: **apply now** (for the rest of this project) or **carry forward** (for the playbook or core rules, decided at the final after-action review).
Status: `proposed`, `approved`, `rejected` or `carried`.

## Gate: WP1 brief (2026-11-16). Stages reviewed: 1 Brief and baseline. Checkpoints: none (WP1 began with "Start project", d5049b3; frame checkpoints cp-project-frame-01, cp-project-frame-02) to cp-wp1-brief-01

1. Plan: Stage 1 of `playbooks/revision.md`. Fill the WP1 brief. Save the baseline unchanged, with its SHA-256 and counts. Have the compliance check read the recipient's rules. Set the master form and the `Master copy:` line. The frame gate added a task: find the DOH guide for LGUs, scan it, then verify it in a separate call (D-006). Gate: the lead approves the brief, the baseline and the master form.
2. What happened: One run on 2026-11-16, started by the lead. No rollback.
   - Baseline: saved at setup (37,251 bytes, 7 comments). By 08:06 UTC the ACRI team had changed the Drive draft again (37,843 bytes, 6 comments). That version was exported to `work/frozen/`.
   - Brief: filled. Seven items are still "to be set by the lead": funder, deadline, page limit, budget ceiling, template, must include, and who holds the master. There is no "who reviews" line.
   - Evidence: the scan made 36 first-pass findings. The separate verify call verified 22, corrected 2 and could not find 12. All 12 had only Scribd copies (`reviews/verification-01.md`). `references.md` holds only verified and corrected rows. The brief limits what the proposal may say it adds to those rows. This was done well.
   - Compliance check: it did not run, because no recipient is named. The task was an open task at the checkpoint. It has since been dropped from WP1's `state.md`, and no register row records the skip.
   - Register: D-002 (master form, approved at setup) and D-007 (who holds the master and when the baseline is frozen; proposed).
   - Memo: EM-002. The trace and `status.md` record it as sent through the tracker while this review ran. Its "Lessons at this gate" line was still a placeholder.
   - Health check: today, Monday, it is due (`health --due`). It has not run: there is no digest in `project/health/` and no trace entry.
   - Comment log: empty. Comments are logged at stage 3.
   - First gate review, so there were no earlier apply-now lessons to check.
3. Why:
   - EM-001 asked nine facts. The lead answered "Agree with all", which settled the options but none of the facts. The facts came after the recommendation and had no default, so a one-line approval left them open.
   - EM-002 repeats that form. Only facts 1 and 2 say what happens without an answer, and neither gives a working deadline. Without a deadline the health check cannot pace WP1 ("No deadline in the work package brief", facts 2026-11-16). This will recur at every gate.
   - The tool kit the lead reported was found online only as Scribd uploads. The scan read their preview text. The verifier could not open them and, correctly, used no workaround. So a third of the claim list could never pass. The lead, ACRI or DOH contacts are more likely to hold the official copy than the open web.
   - The revision playbook assumes a finished baseline that comes back with reviewers' comments. Here the owners are still drafting, and the comments are their own notes. The draft changed three times during setup and again by 08:06 UTC. The playbook says only "stop and ask which version", so the coordinator had to build the freeze options in EM-002 itself.
   - The memo went out before the review, and the health check was skipped. Both are rules already in force (`core/learning-and-oversight.md`; `core/run-rules.md` step 1), broken in one long run that covered the frame answer, the scan, the verification and the gate.

| # | Kind | Lesson | Basis | Status |
| --- | --- | --- | --- | --- |
| L-01 | Apply now (all work packages) | Send a gate memo only when it is complete. It lists the gate review's lessons. Each fact it asks says what the team will do if the lead approves without answering: a default, or the work that waits. Where a fact touches budget or authorship, the default is a hold, not a choice. For EM-002, send one update on its tracker task with the lessons, defaults for facts 3 to 7, and a working deadline under fact 2. | EM-001 (nine facts, none answered); EM-002 (lessons line a placeholder; facts 3 to 7 with no default); WP1 `brief.md`; health facts 2026-11-16 | proposed |
| L-02 | Apply now (all work packages; next used in WP1's policy-instrument scan and in WP3) | When the scan reaches a source only as a user upload (Scribd and similar sites), log it as a lead, not a finding, and leave it off the claim list. The coordinator asks the lead or partners for the official copy in the next memo. Only the official copy, saved in `project/sources/`, is scanned and verified. | `reviews/verification-01.md` (E-002 to E-005, E-017 to E-022, E-032, E-033 not found); `work/evidence.md` ("Official copies not reached"); D-006; EM-002 fact 7 | proposed |
| L-03 | Carry forward | Add to stage 1 of `revision.md`: "Ask who is editing the document now. If its owners are still drafting it, the brief gate also sets the freeze date and who holds the master until then. The diagnosis starts only after the freeze." | Traces 2026-11-16-1135 and -1606; WP1 `brief.md` ("Baseline and master copy"); EM-001 fact 6; EM-002 options A to C; D-002, D-007 | proposed |
