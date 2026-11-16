# Playbook: revision

A revision of an existing document in response to comments: a report or country profile reviewed by a government office, or a manuscript going through co-author and journal review. It produces a revised version in which every change traces to a comment and every new fact to a verified source, and a response to each reviewer.

This playbook runs one work package. `<wp>/` stands for that work package's folder, for example `project/wp/WP1-country-profile/` (`core/project-and-work-packages.md`). Checkpoint names below omit the work package; the tool adds it, so `cp-triage-NN` is saved as `cp-wp1-triage-01`.

Built from two projects: the edit pass on the Human Resources for Health Country Profile of the Philippines 2025 (Department of Health comments and validation workshop findings), and the Post-Residency Placement Program manuscript for BMC Health Services Research (co-author rounds).

## Output and intended use

Two outputs: the revised version, and the response to each reviewer. The intended users are the reviewers and the office or journal that clears or accepts the document. It usually serves an outcome of the form "the office clears the report" or "the journal accepts the manuscript" (`project/results.md`).

## Roles

All six default agent roles. The coordinator applies edits to the master copy. The blind reviewer reads the baseline at the diagnose stage and the revised version at the check stage. The lead, co-authors, reviewers and partners are people; their comments enter the comment log.

## Evidence to check against

- The baseline document, and every file of comments (comment matrices, returned Word files, workshop findings), in `project/sources/`
- The sources the document cites, and the sources needed to answer the comments
- The recipient's rules: journal guidelines and reporting checklists, a funder's template, or a government office's clearance requirements
- Analysis scripts and outputs, where the document reports data (`core/methods-rules.md`)

## Master copy

The brief stage sets one of two forms, and the lead approves it:

- **Word master.** For an existing report or profile. The master is a working copy of the baseline, `<wp>/work/master/<name>_v<N>.docx`, and every edit is a tracked change. If the lead moves the review to Google Docs, the Google Doc becomes the master (`core/documents.md`).
- **Markdown master.** For a manuscript the team rebuilds. The master is `<wp>/work/manuscript.md`, built to Word with `tools/build_docx.py`. Co-authors' Word files are merged back into the Markdown, and redlines are made with `tools/redline.py` against the copy that was sent.

## Stages

A checkpoint is saved at the end of each stage. Files go in `<wp>/work/` unless stated.

### 1. Brief and baseline

- **Who:** coordinator with the lead; compliance check reads the recipient's rules.
- **Do:** fill `<wp>/brief.md`: the output, the outcome it serves, the intended user and use, the purpose of the revision, the recipient and deadline, scope decisions the lead has already made, style guide (the voice guide for a technical product such as a report or country profile; the journal's guidelines for a manuscript), citation style, version naming, and who reviews. Save the baseline file in `project/sources/` unchanged. Record in the brief its SHA-256 checksum and its counts: pages, tables, comments and tracked changes. If the file later differs from these, stop and ask which version to use. Choose the master form and set the `Master copy:` line in `<wp>/state.md`.
- **Gate:** the lead approves the brief, the baseline and the master form. Log the master form as a decision.
- **Checkpoint:** `cp-brief-NN`

### 2. Diagnose

- **Skip when:** the lead limits the revision to the comments received. Record that as a decision.
- **Who:** blind reviewer (baseline and brief only); evidence checker (draft check on the baseline); compliance check; coordinator.
- **Do:** the coordinator lists each analysis and each inferential statement in the baseline, and whether the design supports it (`core/methods-rules.md`). From the three reviews and that list, write `diagnosis.md`: a one-line verdict, the five most important fixes ranked by risk, and facts only the authors or partners can supply. Log each finding in the comment log (`type finding`, round `diagnose`).
- **Gate:** the lead approves the diagnosis and its fixes, in one memo. Record it with `comment approve`.
- **Checkpoint:** `cp-diagnose-NN`

### 3. Log and triage

- **Who:** coordinator.
- **Do:** log every comment of the round (`core/comment-log.md`). Compare each returned file with the copy sent for that round, and log untracked edits. Set the tier, proposed action and proposed response of each row. A comment that changes the scope, the central claim, the method, authorship or a named stakeholder gets its own option in the memo.
- **Gate:** the lead approves the proposed actions for the round, in one memo. Record it with `comment approve`.
- **Checkpoint:** `cp-triage-NN`

### 4. Research and verify

- **Who:** evidence checker in scan mode, then a separate evidence checker call in verify mode.
- **Do:**
  1. For each tier B comment, and each approved comment that needs a source, state in one line the question the comment requires answered.
  2. Scan: findings go into `evidence.md` as **first pass**.
  3. The coordinator writes `claims-to-verify-NN.md` (ID, claim, source, link or file, location) and calls a fresh evidence checker in verify mode with only that file.
  4. Update each finding's status from `<wp>/reviews/verification-NN.md`. Only verified and corrected findings may be used.
  5. If no source answers a question, the text states the data gap in one sentence. Never estimate.
  6. A conflict that changes a headline figure goes to the lead. A new analysis goes to the lead as a method memo before it runs.
- **Done when:** every claim the approved responses need is verified or corrected, or is stated as a data gap.
- **Checkpoint:** `cp-research-NN`

### 5. Draft the changes

- **Who:** writer.
- **Do:** write the text for each approved comment in `edits-<round>.md`, labeled with its comment-log id, citing only verified or corrected findings. Keep each change to what its comment requires.
- **Checkpoint:** `cp-edits-NN`

### 6. Apply and reconcile

- **Who:** coordinator.
- **Do:**
  - **Word master:** apply each change as a tracked change, with a margin comment naming the comment-log id and the source. Or edit a clean copy and turn the edits into tracked changes with `tools/redline.py` against the previous version. Either way, follow `core/documents.md`: author `track_changes_author`, actual time, the document preserved.
  - **Markdown master:** edit `manuscript.md`, rebuild with `tools/build_docx.py`, and make a redline against the last sent copy.
  - **Reconcile:** every tracked change maps to an approved comment. Every approved comment maps to a change, a data-gap sentence, or a "not applied" entry with the reason. Mark each comment done or not applied, with its outcome.
- **Checkpoint:** `cp-apply-NN`

### 7. Check

- **Who:** evidence checker (draft check on the changed passages and on every number that moved), blind reviewer (revised version and brief only), compliance check.
- **Do:** each writes its review in `<wp>/reviews/`. The coordinator also confirms that:
  - the master opens and converts to PDF;
  - the count of tracked changes in this round matches the change entries;
  - the comments that were in the file before this round are still there;
  - every margin comment the team added names a valid comment-log id;
  - the baseline in `project/sources/` still matches its checksum.
- **Checkpoint:** `cp-check-NN`

### 8. Revise

- **Who:** coordinator and writer.
- **Do:** for each major finding, decide accept or reject with a reason and log it. Fix or remove any mismatch or not-found citation. Disagreements still open after one round go to the lead.
- **Done when:** no citation is marked mismatch or not found, and no compliance item on eligibility, ethics, authorship or a commitment is unresolved.
- **Checkpoint:** `cp-revise-NN`

### 9. Responses and sign-off

- **Who:** coordinator and writer; the lead.
- **Do:** draft the response to each reviewer from the comment-log outcomes (a matrix or a letter), using the formats below. Build the clean version and the redline against the last sent copy, each with a PDF.
- **Gate:** the lead approves the revised version, the redline and the responses. The gate memo names the outcome the revision serves.
- **Note:** a person sends. Afterwards, record what was sent with `sent add`. When files come back, the next round starts at stage 3. When the office or journal gives its decision, log it in the outcome log (`core/results-chain.md`), and set `Status: signed off (<date>)` in `<wp>/state.md` once no further round is expected.
- **Checkpoint:** `cp-final-NN`

### 10. After-action review

- **Who:** after-action reviewer.
- **Do:** in final mode for this work package, write `<wp>/after-action.md` with proposed playbook changes. It reads `project/lessons.md` and states what happened to each carry-forward lesson from this work package. The lead approves or rejects each change. Approved changes are applied in the agent-team template repository, not in this project.

## Rounds

Stages 3 to 9 repeat for each round of comments: from the lead, co-authors, a government office, or a journal's reviewers. Each round is compared with the copy that was sent for it, and has its own `round` value in the comment log.

## Response formats

One to three formal sentences per comment, stating what was done and where:

- **Accepted.** "Accepted. Section 4.3 now references the WHO Global Code of Practice on the International Recruitment of Health Personnel."
- **Accepted in part.** "Accepted in part. [What was done.] [What was not done and why, in one sentence.]"
- **Data gap.** "Accepted. No publicly available source reports [X]; Section [Y] states this as a data gap."
- **Later.** "Noted for the next edition. [Reason in one sentence.]"
- **Declined.** "Not adopted. [Reason and evidence in one or two sentences.]"

## Gates

| Gate | Stage | What the lead approves |
| --- | --- | --- |
| Brief | 1 | Output, outcome served, purpose, baseline file, master form |
| Diagnosis | 2 | Verdict and fixes (unless skipped) |
| Triage | 3 | Proposed action for each comment in the round |
| Final | 9 | Revised version, redline and responses |

At each gate, before the gate memo is sent, the after-action reviewer runs in gate mode on the stages since the last gate. This includes the triage and final gates of every round. Its lessons are listed in the gate memo, and the lead approves the apply-now lessons with the gate (`core/learning-and-oversight.md`). Start the issue of each gate memo with "Gate:".

Creating anything outside `project/`, and moving the master copy, also wait for the lead.

## Differences from the core

- **More stop-and-ask points.** Ask the lead before deleting more than one paragraph or any table or figure, before reorganizing a section or changing section numbering, and before applying a conflict that changes a headline figure. In an existing document these changes are hard to reverse once reviewers have seen the new version.
- **Tier C comments.** They get a response; the text does not change.
