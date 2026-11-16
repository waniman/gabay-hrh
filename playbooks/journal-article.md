# Playbook: journal article

An original research article for a peer-reviewed journal, taken from analyzed data, or from an existing draft, to submission and through peer review.

This playbook runs one work package. `<wp>/` stands for that work package's folder, for example `project/wp/WP3-journal-article/` (`core/project-and-work-packages.md`). Checkpoint names below omit the work package; the tool adds it, so `cp-findings-NN` is saved as `cp-wp3-findings-01`.

Built from the Post-Residency Placement Program (PRPP) manuscript for BMC Health Services Research (repository `waniman/PRDP-paper`, October and November 2026), and from the published standards listed under Sources.

## Output and intended use

One output: the article, with its submission package (cover letter, reporting checklists, additional files, figures). The first intended users are the journal's editor and peer reviewers; after publication, researchers and policymakers in the field. It usually serves an outcome of the form "the journal accepts the article", and through the article an outcome of the form "a named office uses the findings" (`project/results.md`).

## Roles

All six default agent roles. The blind reviewer reads as the journal's peer reviewer would. The lead is usually the first or corresponding author. Co-authors are people: their comments enter the comment log, and each one's approval of the version to submit enters the register. People who coded qualitative data confirm the themes. A person submits.

## Evidence to check against

- The journal's author guidelines for the article type, its editorial policies (authorship, AI use, data, ethics) and any collection or call page. Save each in `project/sources/` with the date it was read. Read them again at stage 10.
- The reporting guideline for the study design, chosen at stage 1 from the EQUATOR Network, with its checklist.
- The study protocol, the ethics approval, and the trial or review registration, if any.
- The data: analysis scripts and outputs, the codebook and coded data (`core/methods-rules.md`).
- The sources the article cites, each with a recorded passage.
- Authorship records: each author's contributions and written approval.

## Data protection

- Raw data that can identify a person (transcripts, survey responses with names or contacts, trackers) never enter the repository. They stay where the ethics approval says they are kept. Only de-identified, derived files are committed.
- Participants are coded (for example, KII-01, IMP-01). The key that links codes to names stays outside the repository.
- Excerpts are de-identified before they are written to any file: names, facilities and places below the level the brief allows are replaced by a bracketed label, such as [hospital].
- A file sent to co-authors that holds identifiable data is logged with `sent add --no-copy` (`core/documents.md`).

## Master copy

Markdown in `<wp>/work/manuscript.md` from the draft stage to acceptance, built to Word and PDF with `tools/build_docx.py` in the journal's format (for example, double spacing, line and page numbers). Co-authors' Word files are compared with the copy sent to them, and their edits are merged back into the Markdown (`playbooks/revision.md`, Markdown master).

When the work starts from an existing Word draft, stage 1 decides whether to rebuild it in Markdown or keep it as a Word master. Rebuild when the draft cannot carry tracked changes cleanly, for example a conversion from PDF with line numbers typed as text. Log the choice.

## Records kept in `<wp>/work/`

- `author-queries.md`: facts only the authors can supply, such as an ethics reference number, a grant number, a contribution or a prior presentation. Columns: ID (Q1, Q2 and so on), topic, query, who answers, blocking (yes or no), status. In the text, a missing fact is written `[AUTHOR QUERY Qn: what is needed]`. Agents never fill one.
- `ai-use.md`: each use of an AI tool on the work, including each interpretation an agent proposed: date, tool, purpose, output file, the trace file that holds the instructions given, and the person who checked the output. The coordinator adds rows from the trace at each checkpoint. The statement on AI use, in the article and in the cover letter, is written from this record. The tool's version is entered by the lead. The International Committee of Medical Journal Editors (ICMJE) asks that AI used to conduct a study be described in the Methods with "the tool used, version, and prompts where applicable" (ICMJE, 2026).
- `interpretations.md`: one row per interpretation or conclusion the article may make: ID (I-01, I-02 and so on), the statement, the findings and sources it rests on, the other explanations considered, who proposed it (an agent or a named author), and the authors' decision: validated, changed, rejected or author-supplied. Only validated, changed and author-supplied rows enter the text.
- `methods-trace.md`: one row per sentence of the Methods, with the protocol, script, codebook, log or source that records it. A Methods sentence with no record is a gap, not a fact.

## Stages

A checkpoint is saved at the end of each stage. Files go in `<wp>/work/` unless stated.

### 1. Brief

- **Who:** coordinator with the lead; compliance check reads the journal's rules.
- **Do:** fill `<wp>/brief.md` with the lead:
  - the output: article type, target journal and any collection, deadline; the outcome it serves; the intended users. Check the journal against the Think. Check. Submit. list before it is chosen;
  - the research question and aims, the design, and the data sources;
  - the reporting guideline: choose it from the EQUATOR Network library for the design, and confirm that each checklist item can be answered from the data. A mixed-methods study usually needs one guideline for the whole design and one for each strand, for example the Good Reporting of a Mixed Methods Study (GRAMMS) with the Consolidated Criteria for Reporting Qualitative Research (COREQ) and a survey guideline. Report sex and gender as the Sex and Gender Equity in Research (SAGER) guidelines ask. In the PRPP manuscript, a web-survey checklist was dropped late because several of its items could not be answered from the data;
  - the proposed authors, their order, and each author's contributions by the 14 roles of the Contributor Roles Taxonomy (CRediT); who will submit. The ICMJE asks authors to settle authorship "when planning the work" and lists four criteria, all of which each author must meet (ICMJE, 2026). The person who submits must be an author;
  - the ethics approval and its reference, the protocol and any registration;
  - where raw data are kept, and the level of place and role the article may name;
  - the expected uses of AI tools;
  - the journal's citation style and version naming. The journal's guidelines set format and citation style. The style guide in `team.config.yaml` does not apply to journal manuscripts. The lead's own prose rules apply where the journal is silent, if the brief says so.
  Start `author-queries.md` and `ai-use.md`. If the work starts from an existing draft, save it unchanged in `project/sources/` with its SHA-256 checksum, and decide the master form.
  The compliance check reads the author guidelines, editorial policies and call page: scope and excluded topics, article type, word and abstract limits, required sections and declarations, reporting checklist, AI policy, data policy, fees. If the journal's AI policy does not permit AI to propose claims or interpretations, even with disclosure, the coordinator sends the lead a memo before the outline: for this journal the authors supply every interpretation, or the lead chooses another journal.
- **Gate:** the lead approves the brief: journal, design, reporting guideline, authors and order, AI uses and master form. Log the authors and their roles as a decision.
- **Checkpoint:** `cp-brief-NN`

### 2. Diagnose

- **Skip when:** the work starts from data, with no draft. Record that as a decision.
- **Who:** blind reviewer (the draft and the brief only); evidence checker (draft check); compliance check; coordinator.
- **Do:** write `diagnosis.md`, an editor's report on the existing draft:
  1. a one-line verdict: the likely outcome if submitted as it stands, and the main reason;
  2. scope fit with the journal and any collection;
  3. a validity screen: question, design fit, sampling and denominators, instrument, analysis, qualitative procedures, internal consistency between abstract, text and tables;
  4. a compliance audit against the journal's rules, each item marked pass, fix or author query;
  5. a claim register: one row per statement, marked uncited, cited (to verify), likely mismatch, data (to reproduce), data conflict, overreach, out of scope or method gap;
  6. the disposition of any comments already in the draft;
  7. the five most important fixes, ranked by risk to acceptance.
  Log each finding in the comment log (type `finding`, round `diagnose`).
- **Gate:** the lead approves the diagnosis and its fixes, in one memo. Record it with `comment approve`.
- **Checkpoint:** `cp-diagnose-NN`

### 3. Analysis and findings

- **Who:** coordinator; evidence checker for claim checks; the people who coded the data.
- **Do:**
  - **Quantitative.** Scripts in `<wp>/work/analysis/` read the data and write every table and figure. When an earlier draft exists, reproduce each of its figures in `reproduction_check.csv` and explain each mismatch. Report descriptive statistics unless the lead has approved a test in a method memo (`core/methods-rules.md`). Record software and versions.
  - **Qualitative.** Write the codebook: codes from a named framework, plus inductive codes, each with a definition. Write the coding protocol: units coded, de-identification, translation (keep the original words beside the English), and what is recorded for each excerpt. Code every transcript. Each excerpt carries its participant code and location. Each count in the text ("9 of 12 physicians") comes from the coded data.
  - **Claims.** Check each claim of an earlier draft, or each planned finding, against the coded data or the script output. Record supports, partly, contradicts or no data, with the location.
  - **Themes.** Draft candidate themes for the coders, with the excerpts and counter-cases for each. A theme enters the text only after the coders confirm it.
  - **Mixed methods.** Build a joint display: one row per factor, with the survey finding, each qualitative finding, and the fit between them. Use fit labels from a cited methods source.
  Write `findings.md`: the headline findings, what the data support, what they do not support, and what changes from any earlier draft. Agents may add candidate interpretations of the findings to `interpretations.md`, as proposals.
- **Done when:** every table, figure and count is produced by a script or from the coded data, and every planned finding has a recorded check.
- **Gate:** the lead approves `findings.md`. The headline findings set the article's central claim, so this is the cheapest point to change direction. Record the coders' confirmation of the themes in the register.
- **Checkpoint:** `cp-findings-NN`

### 4. Evidence scan and verification

- **Who:** evidence checker in scan mode, then a separate evidence checker call in verify mode.
- **Do:**
  1. Scan: for each claim that needs an outside source, record the source and a passage of 50 words or fewer with its location, in `evidence.md`, as **first pass**. Also record: the source type; the country or region studied; whether only the abstract was read; any retraction or expression of concern; and whether the journal's editors or a collection's guest editors are authors. Cite such sources only where they are relevant, neither more nor less. Prefer primary studies and current guidelines to reviews that cite them. A claim that no study exists on the topic needs a documented search: databases, date and terms.
  2. The coordinator writes `claims-to-verify-NN.md` and calls a fresh evidence checker in verify mode with only that file.
  3. Update each finding from `<wp>/reviews/verification-NN.md`. Only verified and corrected findings may be cited.
  4. Write `literature-brief.md`: where this study's findings agree with the literature, where they conflict, and what they add.
- **Done when:** every outside claim the article needs has a verified or corrected source, or a gap is logged.
- **Checkpoint:** `cp-evidence-NN`

### 5. Outline

- **Who:** writer.
- **Do:** write `outline.md`: the title, stating the design; the central argument in two sentences; the aims; each section in the journal's order, with its length; the table or figure that carries each finding; the limitations; and the reporting checklist items each section must answer. For the Discussion and Conclusions, the writer proposes candidate interpretations and conclusions in `interpretations.md`, each with the findings and literature it rests on and the other explanations considered. The lead and co-authors validate each one, change or reject it, and add their own. The outline lists only the validated, changed and author-supplied rows.
- **Gate:** the lead approves the outline and the decision on each row of `interpretations.md`.
- **Checkpoint:** `cp-outline-NN`

### 6. Draft

- **Who:** writer; coordinator for the build.
- **Do:** write `manuscript.md` against the approved outline, with every declaration heading the journal requires. The Results report the approved `findings.md`. The Discussion and Conclusions draft only the validated, changed and author-supplied rows of `interpretations.md`. An interpretation that arises while drafting is added there as a proposal and waits for the authors. Write `methods-trace.md` alongside the Methods. Write the statement on AI use from `ai-use.md`, in the place the journal requires. Put each missing fact as an author query. Build the Word and PDF copies in the journal's format.
- **Checkpoint:** `cp-draft-NN`

### 7. Check

- **Who:** evidence checker (draft check), blind reviewer (the draft and `<wp>/brief.md` only), compliance check. Run all three on the same build.
- **Do:** each writes its review in `<wp>/reviews/`. The compliance check fills the reporting checklist with the location of each item, and checks the declarations, authorship, the statement on AI use, ethics, data availability, figures and tables against the journal's rules. The coordinator also confirms that:
  - the abstract, text and tables give the same numbers;
  - every sentence of the Methods has a record in `methods-trace.md`;
  - every author query in the text is in `author-queries.md`;
  - every interpretation and conclusion in the text traces to a validated, changed or author-supplied row of `interpretations.md`.
- **Checkpoint:** `cp-check-NN`

### 8. Revise

- **Who:** coordinator and writer.
- **Do:** for each major finding, decide accept or reject with a reason and log it. The writer revises. Any mismatch or not-found citation is fixed or removed. Disagreements still open after one round go to the lead.
- **Done when:** no citation is marked mismatch or not found; the reporting checklist has no unanswered item; and no compliance item on ethics, authorship, AI use or a commitment is unresolved, except author queries.
- **Gate:** the lead approves the version for co-authors, the author queries to send with it, and a change log if an earlier draft existed.
- **Checkpoint:** `cp-revise-NN`

### 9. Co-author rounds

- **Who:** coordinator and writer; the lead and co-authors.
- **Do:** a person sends the version, with the author queries and the change log. Record what was sent with `sent add`. When files come back, follow stages 3 to 8 of `playbooks/revision.md` for the round: compare each file with the copy sent, log every comment, tracked change and untracked edit, triage, verify, draft, apply and check. An addition by a co-author is checked like any other claim, against the data and verified sources. The recommendation is to hedge a claim where a supported hedge exists, and to decline it where none does. Answered author queries close in `author-queries.md`. Draft a reply to each co-author from the comment-log outcomes.
- **Gate:** the lead approves the proposed actions for each round, in one memo (`core/comment-log.md`).
- **Checkpoint:** `cp-coauthors-NN`

### 10. Submission package and sign-off

- **Who:** coordinator, writer and compliance check; the lead and co-authors.
- **Do:**
  1. Read the journal's guidelines and call page again, and record any change.
  2. Build the final manuscript, figures, reporting checklists with final page and line numbers, and additional files. The EQUATOR Network advises that checklists are "best used at the end of writing, before journal submission" (EQUATOR Network, n.d.).
  3. Draft the cover letter: fit with the journal or collection; policy matters (protocol, preprints, prior presentations, data restrictions, ethics, competing interests); the use of AI tools, which the ICMJE asks authors to describe in both the cover letter and the paper (ICMJE, 2026); any conflict with an editor; suggested reviewers. Leave reviewer names as author queries. Agents never propose a named person they have not been given.
  4. Write `run-sheet.md`: files to upload, fields to enter in the submission system, open author queries, and each author's approval.
  5. Confirm authorship: each author meets the journal's authorship criteria, the contributions statement matches the roles logged at stage 1, and each person named in the acknowledgements has given written permission (ICMJE, 2026). Some publishers do not allow authors to be added, removed or reordered after acceptance (BMC, n.d.), so any change is settled now.
  6. Send the final version to all authors for written approval. Log each approval in the register, by that author's name, with their reply saved in `project/sources/`.
- **Done when:** no author query is open, and every author has approved the final version in writing.
- **Gate:** the lead approves the submission package.
- **Note:** an author submits. Afterwards, record each file submitted with `sent add` (purpose: submission).
- **Checkpoint:** `cp-final-NN`

### 11. Peer review

- **Who:** coordinator and writer; the lead and co-authors.
- **Do:** when the journal's decision arrives, save it with the reviewers' reports in `project/sources/`, and log the decision in the outcome log (`core/results-chain.md`).
  - **Revisions requested.** Log every reviewer comment in the comment log, with the round named after the decision (for example, `journal-R1`). Run stages 3 to 9 of `playbooks/revision.md` for the round, including its response formats and its final gate. Answer every comment point by point; give line numbers and say which version they refer to; explain each change declined (Noble, 2017). An analysis a reviewer asks for goes to the lead as a method memo before it runs (`core/methods-rules.md`). Some journals publish reviewer reports with the article, so write each response for a public reader. Co-authors approve the revised version before resubmission, as at stage 10. An author resubmits.
  - **Rejected.** A new journal changes the work package's brief, so it goes to the lead as a memo. On approval, update the brief and return to stage 10.
  - **Accepted.** Check the proofs against the accepted version, and log any change the journal made. Set `Status: signed off (<date>)` in `<wp>/state.md`.
- **Checkpoint:** `cp-review-NN`

### 12. After-action review

- **Who:** after-action reviewer.
- **Do:** in final mode for this work package, write `<wp>/after-action.md` with proposed playbook changes. It reads `project/lessons.md` and states what happened to each carry-forward lesson from this work package.

## Gates

| Gate | Stage | What the lead approves |
| --- | --- | --- |
| Brief | 1 | Journal, design, reporting guideline, authors and order, AI uses, master form |
| Diagnosis | 2 | Verdict and fixes (only when starting from a draft) |
| Findings | 3 | The headline findings and what the data do not support |
| Outline | 5 | Title, argument, section plan, and the decision on each proposed interpretation |
| Co-author version | 8 | The version and queries to send to co-authors |
| Co-author round | 9 | Proposed action for each comment, each round |
| Submission | 10 | The submission package, with every author's approval |
| Peer review | 11 | Proposed action for each reviewer comment, and the resubmission, each round |

At each gate, before the gate memo is sent, the after-action reviewer runs in gate mode on the stages since the last gate. Its lessons are listed in the gate memo, and the lead approves the apply-now lessons with the gate (`core/learning-and-oversight.md`). Start the issue of each gate memo with "Gate:". The final gate memos (stages 10 and 11) name the outcome the article serves.

Creating anything outside `project/`, and moving the master copy, also wait for the lead.

## Differences from the core

- **The journal sets the style.** Format, structure and citation style follow the journal's guidelines, not `style_guide` in `team.config.yaml`.
- **More stop-and-ask points.** Any change to the author list or order, the title, the aims or a headline finding goes to the lead. So does any change to the statement on AI use.
- **Author queries.** Facts only the authors hold are asked, never supplied. They are tracked in `author-queries.md`, not in memos, because co-authors answer most of them.
- **Agents propose, authors validate.** Agents may propose candidate scientific claims, interpretations and conclusions. The lead and co-authors validate each one, change or reject it, and add their own. Only validated, changed and author-supplied rows of `interpretations.md` enter the text. The statement on AI use says that AI proposed candidate interpretations and that the authors validated them. Journal policies differ on this. Springer Nature lists "generating scientific claims or interpretations" among AI uses it does not permit, and states that "the argument, interpretation, and conclusions must be author-led" (Springer Nature, n.d.). Stage 1 therefore checks the target journal's policy, and a conflict goes to the lead before the outline.
- **Two checks on the record.** `methods-trace.md` ties each Methods sentence to a record, and `ai-use.md` ties the statement on AI use to the trace. In the PRPP manuscript, a translation method was written into the Methods with no record, and it was wrong. The statement on AI use was cut in review and had to be restored, because the journal requires every use to be described.

## Sources

Each source was opened on 11 November 2026. Quotations are verbatim.

- BMC (n.d.). *Editorial policies*. https://link.springer.com/brands/bmc/editorial-policies
- BMC Health Services Research (n.d.). *Submission guidelines: Research article*. https://link.springer.com/journal/12913/submission-guidelines/research-article
- EQUATOR Network (n.d.). *Reporting guidelines, writing guides, and checklists*; and the library entries for GRAMMS, COREQ, the Standards for Reporting Qualitative Research (SRQR), the Strengthening the Reporting of Observational Studies in Epidemiology (STROBE), the Consensus-Based Checklist for Reporting of Survey Studies (CROSS) and SAGER. https://www.equator-network.org/
- ICMJE (2026). *Recommendations for the Conduct, Reporting, Editing, and Publication of Scholarly Work in Medical Journals*. Updated January 2026. Sections II.A (authorship and AI-assisted technology) and IV.A.3.d (Methods). https://www.icmje.org/icmje-recommendations.pdf
- NISO (2022). *CRediT, Contributor Roles Taxonomy* (ANSI/NISO Z39.104-2022). https://credit.niso.org/
- Noble WS (2017). Ten simple rules for writing a response to reviewers. *PLoS Comput Biol*. 13(10):e1005730. https://doi.org/10.1371/journal.pcbi.1005730
- Springer Nature (n.d.). *AI use in manuscript preparation*. https://www.springernature.com/gp/policies/editorial-policies/ai-manuscript-preparation
- Think. Check. Submit. (2023). *Journals checklist*. https://thinkchecksubmit.org/journals/
