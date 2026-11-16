# Playbook: concept note

A concept note of two to five pages that asks a funder to invite a full proposal or fund a small study.

This playbook runs one work package. `<wp>/` stands for that work package's folder, for example `project/wp/WP2-concept-note/` (`core/project-and-work-packages.md`). Checkpoint names below omit the work package; the tool adds it, so `cp-outline-NN` is saved as `cp-wp2-outline-01`.

## Output and intended use

One output: the concept note. Its intended user is the funder's program officer or review panel. It usually serves an outcome of the form "the funder invites a full proposal" or "the funder funds the study" (`project/results.md`).

## Roles

All six default agent roles. The project lead and any partners are people.

## Evidence to check against

- Sources the note cites
- The funder's call document and template (`project/sources/`)
- The budget sheet, if the note carries a budget
- The institution's prior outputs, where the note cites them
- Analysis scripts and outputs, if the note reports new data (`core/methods-rules.md`)

## Master copy

Markdown in `<wp>/work/` from outline to sign-off (`Master copy: <wp>/work/draft.md`, written with the full path). Word and PDF copies are built from it with `tools/build_docx.py`. Comments from the lead or partners on a draft go in the comment log (`core/comment-log.md`).

## Stages

A checkpoint is saved at the end of each stage. Files go in `<wp>/work/` unless stated.

### 1. Brief

- **Who:** coordinator with the lead; compliance check reads the call.
- **Do:** fill `<wp>/brief.md` with the lead: the output, the outcome it serves, the intended user and use, question, funder and call, limits, style (the voice guide in `team.config.yaml`, unless the funder's template sets another), must-include, must-avoid, partners. Run the compliance check on the call (eligibility, format, budget rules, AI-use policy).
- **Gate:** the lead approves the brief. Record it as a decision by the lead and mark the brief approved.
- **Checkpoint:** `cp-brief-NN`

### 2. Evidence scan and verification

- **Who:** evidence checker in scan mode, then a separate evidence checker call in verify mode.
- **Do:**
  1. Scan: build `evidence.md` with the size of the problem, evidence on the proposed approach, local data and the funder's stated priorities. Each finding starts as **first pass**.
  2. The coordinator writes `claims-to-verify-NN.md` (ID, claim, source, link or file, location) and calls a fresh evidence checker in verify mode with only that file.
  3. Update each finding's status from `<wp>/reviews/verification-NN.md`. Only verified and corrected findings may be cited. A conflict that changes a headline figure goes to the lead.
- **Done when:** every claim the brief needs has at least one verified or corrected finding, or a gap is logged.
- **Checkpoint:** `cp-evidence-NN`

### 3. Outline

- **Who:** writer.
- **Do:** write `outline.md`: the central argument in two sentences, the section plan following the funder's template, the key evidence for each section, and the length of each section.
- **Gate:** the lead approves the outline. This is the cheapest point to change direction.
- **Checkpoint:** `cp-outline-NN`

### 4. Draft

- **Who:** writer.
- **Do:** write `draft.md` against the approved outline.
- **Checkpoint:** `cp-draft-NN`

### 5. Check

- **Who:** evidence checker (draft check), blind reviewer, compliance check. Run all three on the same draft. The blind reviewer gets only `draft.md` and `<wp>/brief.md`.
- **Do:** each writes its review in `<wp>/reviews/`.
- **Checkpoint:** `cp-check-NN`

### 6. Revise

- **Who:** coordinator and writer.
- **Do:** for each major finding, decide accept or reject with a reason and log it. The writer revises. Any mismatch or not-found citation is fixed or removed. Disagreements still open after one round go to the lead.
- **Done when:** no citation is marked mismatch or not found, and no compliance item on eligibility, ethics, authorship or a commitment is unresolved.
- **Checkpoint:** `cp-revise-NN`

### 7. Sign-off

- **Do:** build `final.docx` and a PDF from `final.md` with `tools/build_docx.py`, in the funder's format.
- **Gate:** the lead approves the final version: `final.md` and its Word and PDF copies. The gate memo names the outcome the note serves.
- **Note:** submission is done by a person. The team never submits. Afterwards, record the exact file that was submitted with `python3 tools/team.py sent add` (`core/documents.md`), and set `Status: signed off (<date>)` in `<wp>/state.md`. Log the funder's reply in the outcome log when it arrives (`core/results-chain.md`).
- **Checkpoint:** `cp-final-01`

### 8. After-action review

- **Who:** after-action reviewer.
- **Do:** in final mode for this work package, write `<wp>/after-action.md` with proposed playbook changes. It reads `project/lessons.md` and states what happened to each carry-forward lesson from this work package. The lead approves or rejects each change. Approved changes are applied in the agent-team template repository, not in this project.

## Gates

| Gate | Stage | What the lead approves |
| --- | --- | --- |
| Brief | 1 | Output, outcome served, intended user and use, question, limits |
| Outline | 3 | Argument and section plan |
| Final | 7 | The version to submit |

At each gate, before the gate memo is sent, the after-action reviewer runs in gate mode on the stages since the last gate. Its lessons are listed in the gate memo, and the lead approves the apply-now lessons with the gate (`core/learning-and-oversight.md`). Start the issue of each gate memo with "Gate:".

Creating anything outside `project/` (a repository, a sheet, a tracker task) also waits for the lead, as `CLAUDE.md` rule 4 sets out.
