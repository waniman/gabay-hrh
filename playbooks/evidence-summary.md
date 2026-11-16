# Playbook: evidence summary

A summary of the best available research evidence on one policy or practice question, prepared in weeks for a named decision-maker, with its methods and their shortcuts stated.

This playbook runs one work package. `<wp>/` stands for that work package's folder, for example `project/wp/WP1-evidence-summary/` (`core/project-and-work-packages.md`). Checkpoint names below omit the work package; the tool adds it, so `cp-protocol-NN` is saved as `cp-wp1-protocol-01`.

## Output and intended use

One output in two layers: a short summary that leads with key messages, and a technical annex with the methods, search log, study flow, evidence tables and certainty ratings. The intended users are officials who must decide or advise on the question: a Department of Health bureau, a WHO country office, a local government, a funder. It usually serves an outcome of the form "the office uses the evidence in deciding X" (`project/results.md`).

## Which form of evidence summary?

The brief sets one of three forms, and the lead approves it.

| Form | What it synthesizes | Typical time | Basis |
| --- | --- | --- | --- |
| **A. Summary of reviews** (default) | Existing systematic reviews and guidelines; primary studies only where no review covers a question | Days to 5 weeks | Khangura et al. (2012); Lavis et al. (2009); Cochrane overviews of reviews (Pollock et al., 2024) |
| **B. Rapid review** | Primary studies, with systematic review methods streamlined and the shortcuts stated | 5 to 12 weeks | WHO (Tricco et al., 2017); Cochrane Rapid Reviews Methods Group (2023 to 2025) |
| **C. Evidence brief for policy** | Form A or B, set out as the problem, options and implementation considerations, with local evidence | Form A or B, plus a merit review | Lavis et al. (2009); WHO Regional Office for Europe (2020) |

- **Form A** fits most requests. Khangura et al. (2012) called their rapid syntheses "evidence summaries" and placed emphasis "on locating and summarizing evidence from relevant and high quality systematic reviews". They report the meta-analyses that included reviews contain, and do not pool data again.
- **Form B** fits when reviews are missing, out of date or do not cover the setting. Most rapid reviews take "5–12 weeks" (Tricco et al., 2017).
- **Form C** is a way of setting out form A or B for a decision. An evidence brief describes the problem, options and implementation considerations, and "recommendations should never be provided" (WHO Regional Office for Europe, 2020).

**Out of scope.** A new systematic review, a meta-analysis, a scoping review and an evidence and gap map each need their own playbook. A systematic review takes "an average of 12–24 months" (Tricco et al., 2017). Meta-analysis is "the statistical combination of results from two or more separate studies" (Deeks et al., 2026): it is a method used inside a systematic review, not a type of review. In this playbook, a new pooled estimate is a new analysis, and it goes to the lead as a method memo first (`core/methods-rules.md`).

## Roles

All six default agent roles. The evidence checker searches, screens, extracts and appraises in scan mode; separate evidence checker calls verify claims. A named person acts as second screener and verifier at stages 4 and 5. The brief names this person, and their screening and verification decisions are recorded under their name. The blind reviewer reads as the intended user would. Knowledge users, such as an official from the office that asked the question, help set the question and outcomes. For form C, a merit review panel reviews the draft. Lavis et al. (2009) suggest that the review "could involve at least one policymaker, at least one other stakeholder, and at least one researcher". They are people; their comments enter the comment log.

## Evidence to check against

- The request and any terms from the commissioning office (`project/sources/`).
- The protocol approved at stage 2.
- The included reviews, guidelines and studies, each with a recorded location for every figure used.
- Local data and policy instruments, for form C and for applicability (`core/policy-instruments.md`).

## Master copy

Markdown in `<wp>/work/` from the draft stage to sign-off (`Master copy: <wp>/work/summary.md`, written with the full path). Word and PDF copies are built with `tools/build_docx.py`. The style guide in `team.config.yaml` applies: evidence summaries are among the technical products it covers.

## Stages

A checkpoint is saved at the end of each stage. Files go in `<wp>/work/` unless stated.

### 1. Brief

- **Who:** coordinator with the lead and, where possible, a knowledge user; compliance check reads the request.
- **Do:** fill `<wp>/brief.md`: the question; the decision it informs and who makes it; the intended users; the deadline; the form (A, B or C); the populations, settings, years and languages in scope; the outcomes that matter most to the decision, including harms; the person who acts as second screener and verifier, and the time they can give; and who reviews the draft. Check that a rapid approach fits: if the decision needs a full systematic review, say so to the lead.
- **Gate:** the lead approves the brief and the form.
- **Checkpoint:** `cp-brief-NN`

### 2. Protocol

- **Who:** coordinator and evidence checker.
- **Do:** write `protocol.md` before any search:
  - the question in a structured form, such as population, intervention, comparison and outcomes for effects;
  - eligibility criteria, and the order of preference for evidence types (form A: systematic reviews and guidelines first);
  - information sources: at least two, because "searching MEDLINE alone is not a viable option" (Klerings et al., 2023); plus WHO and government sources and local data where the question needs them;
  - the search strings, date limits and languages for each source;
  - the screening procedure (stage 4);
  - the data items to extract, and the appraisal tool for each type of source;
  - the synthesis approach, and how certainty is rated (stage 6);
  - each shortcut taken, compared with a full systematic review, and why.
  If the summary may be published, the lead decides whether to register the protocol.
- **Gate:** the lead approves the protocol. Afterwards, any change to it is a deviation, logged in the register with its reason.
- **Checkpoint:** `cp-protocol-NN`

### 3. Search

- **Who:** evidence checker in scan mode.
- **Do:** run the searches exactly as the protocol sets them. Record each one in `search-log.md`: source, date, string, limits and number of records. Save the records in `records.csv` and remove duplicates.
- **Done when:** every source in the protocol has been searched, or the reason it was not is logged.
- **Checkpoint:** `cp-search-NN`

### 4. Screen

- **Who:** evidence checker in scan mode; the named second screener, a person.
- **Do:**
  1. Screen titles and abstracts against the eligibility criteria, recording each decision in `screening.csv`.
  2. The second screener screens a random 20% of the records against the criteria, without seeing the agent's decisions. Compute the agreement. If it is 80% or more, the agent screens the rest alone; if not, the second screener also screens every remaining record. This follows the Cochrane Rapid Reviews Methods Group (Nussbaumer-Streit et al., 2023), which advises against one reviewer screening all titles and abstracts because that approach "has been shown to miss 13% of relevant studies".
  3. Settle each disagreement against the criteria with the second screener, and log it. A disagreement the criteria cannot settle goes to the lead.
  4. Screen the full texts, recording the reason for each exclusion. Count the records at each step for a flow diagram in the form of PRISMA 2020.
- **Done when:** every record has a decision, and the flow counts add up.
- **Checkpoint:** `cp-screen-NN`

### 5. Extract and appraise

- **Who:** evidence checker in scan mode; the named verifier, a person.
- **Do:**
  1. **Extract.** The agent extracts the protocol's data items from each included source into `evidence-table.csv`, with the location of each figure. The named person checks every figure against the source and records it as verified or corrected. A separate evidence checker call may check the figures first, so that the person starts from a list of the discrepancies it found.
  2. **Appraise.** The agent appraises each source first, with the protocol's tool, and records its judgement and the reason for each item in `appraisal.csv`. The named person then appraises each source, starting from the agent's draft: they confirm or change each judgement, and their judgement is final. Each change is recorded with its reason.

  The Methods Group recommends that one person extracts and appraises and a second verifies; omitting the appraisal "is discouraged" (Nussbaumer-Streit et al., 2023).
- **Done when:** every extracted figure is verified or corrected, and the named person has made the final judgement on every appraisal.
- **Checkpoint:** `cp-extract-NN`

### 6. Synthesis and certainty

- **Who:** coordinator and evidence checker.
- **Do:** write `findings.md`, one section for each question or outcome:
  - what the evidence shows, from how many sources of which types;
  - the certainty of the evidence. For effects, use the GRADE levels (high, moderate, low, very low). For qualitative findings, use the confidence levels of GRADE-CERQual. In form A, report the certainty ratings the included reviews give, and rate only where they give none. Rate only the outcomes the brief marked as critical (Garritty et al., 2021);
  - how far the evidence applies to the setting: who was studied, where, and what differs locally;
  - what the evidence does not show, stated as gaps;
  - candidate interpretations and key messages: what the findings may mean for the decision. Agents may propose them, each marked as a proposal with the findings it rests on. The lead validates each one, changes or rejects it, and adds their own.
  Synthesize in words and tables. Report the pooled estimates of included reviews as they are; do not pool data again unless the lead has approved a method memo. For form C, add the options and their implementation considerations, drawing on local data and policy instruments.
- **Gate:** the lead approves `findings.md`: the findings, their certainty, the gaps, and the decision on each proposed interpretation and key message. These set the key messages, so this is the cheapest point to change direction.
- **Checkpoint:** `cp-findings-NN`

### 7. Draft

- **Who:** writer.
- **Do:** write `summary.md` from the approved findings:
  - key messages first, drawn only from the interpretations the lead validated or supplied, each with its certainty, in plain words for the intended user;
  - for form C, the graded entry the WHO manual describes: "one page of key messages, three pages for an executive summary and a maximum of 25 pages for the full EBP" (WHO Regional Office for Europe, 2020), with no recommendations;
  - the methods and every shortcut, in the annex, with the search log, flow diagram, evidence tables and certainty tables.
  The writer runs the style guide's self-check before reporting back.
- **Checkpoint:** `cp-draft-NN`

### 8. Check

- **Who:** evidence checker (draft check), blind reviewer (the summary and `<wp>/brief.md` only), compliance check. Run all three on the same draft.
- **Do:** each writes its review in `<wp>/reviews/`. The compliance check confirms that the summary meets the commissioning office's terms; that the annex reports the items of PRISMA 2020, and of the Preferred Reporting Items for Overviews of Reviews (PRIOR) for form A, that apply to its methods; that every shortcut is stated; and, for form C, that no recommendation is made. Interim guidance advises using "PRISMA 2020 as the foundation for reporting" until a rapid review extension exists (Stevens et al., 2025). The summary never claims to follow a "PRISMA-RR" checklist, because none has been published.
- **Checkpoint:** `cp-check-NN`

### 9. Revise and review

- **Who:** coordinator and writer; for form C, the merit review panel.
- **Do:** for each major finding, decide accept or reject with a reason and log it. The writer revises. For form C, a person sends the revised draft to the merit review panel; log their comments as a round of the comment log, and triage them for the lead (`core/comment-log.md`).
- **Done when:** no citation is marked mismatch or not found, and every merit review comment has an approved action.
- **Gate:** for form C, the lead approves the proposed action for each merit review comment, in one memo.
- **Checkpoint:** `cp-revise-NN`

### 10. Sign-off

- **Do:** build the Word and PDF copies from `summary.md`.
- **Gate:** the lead approves the final version. The gate memo names the outcome the summary serves.
- **Note:** a person sends. Record what was sent with `sent add`. When the office replies or uses the summary, log it in the outcome log (`core/results-chain.md`). If the brief set a date to search again, add it to `<wp>/state.md`.
- **Checkpoint:** `cp-final-NN`

### 11. After-action review

- **Who:** after-action reviewer.
- **Do:** in final mode for this work package, write `<wp>/after-action.md` with proposed playbook changes. It reads `project/lessons.md` and states what happened to each carry-forward lesson from this work package.

## Gates

| Gate | Stage | What the lead approves |
| --- | --- | --- |
| Brief | 1 | Question, decision, users, form |
| Protocol | 2 | Methods and shortcuts, before any search |
| Findings | 6 | Findings, certainty and gaps |
| Merit review | 9 | Proposed action for each reviewer comment (form C only) |
| Final | 10 | The version to send |

At each gate, before the gate memo is sent, the after-action reviewer runs in gate mode on the stages since the last gate. Its lessons are listed in the gate memo, and the lead approves the apply-now lessons with the gate (`core/learning-and-oversight.md`). Start the issue of each gate memo with "Gate:".

Creating anything outside `project/` also waits for the lead.

## Differences from the core

- **A protocol before the search.** The lead approves the methods before any source is searched, and every later change is logged as a deviation. This keeps the search from being shaped by what it finds.
- **A person as second screener and verifier.** In every summary, a named person screens the 20% sample, verifies the extraction, and makes the final appraisal of each source after an agent's first appraisal (lead's decisions, 11 November 2026). Agents built on one model share blind spots (`README.md`, Limits), so a separate AI call does not stand in for the second reviewer. The annex names who did each step.
- **Agents propose, the lead validates.** Agents may propose interpretations and key messages. The lead validates each one, changes or rejects it, and adds their own at the findings gate. Only validated and lead-supplied interpretations enter the summary, and the annex says that AI proposed some of them.
- **No new pooling.** A pooled estimate not already published in an included review is a new analysis (`core/methods-rules.md`).

## Sources

Each source was opened on 11 November 2026. The quotations were checked against the sources by a separate call that saw only the claim list, or directly against the saved text (`proposals/playbook-drafts/verification-evidence-summary.md`).

- Deeks JJ, Higgins JPT, Altman DG, McKenzie JE, Veroniki AA, Simmonds M (eds) (2026). Chapter 10: Analysing data and undertaking meta-analyses. In: *Cochrane Handbook for Systematic Reviews of Interventions*, version 6.5.1. Cochrane. https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-10
- Garritty C, Gartlehner G, Nussbaumer-Streit B, et al. (2021). Cochrane Rapid Reviews Methods Group offers evidence-informed guidance to conduct rapid reviews. *J Clin Epidemiol*. 130:13-22. https://doi.org/10.1016/j.jclinepi.2020.10.007
- Khangura S, Konnyu K, Cushman R, Grimshaw J, Moher D (2012). Evidence summaries: the evolution of a rapid review approach. *Syst Rev*. 1:10. https://doi.org/10.1186/2046-4053-1-10
- Klerings I, Robalino S, Booth A, et al. (2023). Rapid reviews methods series: guidance on literature search. *BMJ Evid Based Med*. 28(6):412-17. https://doi.org/10.1136/bmjebm-2022-112079
- Lavis JN, Permanand G, Oxman AD, Lewin S, Fretheim A (2009). SUPPORT Tools for evidence-informed health Policymaking (STP) 13: Preparing and using policy briefs to support evidence-informed policymaking. *Health Res Policy Syst*. 7(Suppl 1):S13. https://doi.org/10.1186/1478-4505-7-S1-S13
- Nussbaumer-Streit B, Sommer I, Hamel C, et al. (2023). Rapid reviews methods series: guidance on team considerations, study selection, data extraction and risk of bias assessment. *BMJ Evid Based Med*. 28(6):418-23. https://doi.org/10.1136/bmjebm-2022-112185
- Pollock M, Fernandes RM, Becker LA, Pieper D, Hartling L (2024). Chapter V: Overviews of Reviews (last updated August 2023). In: *Cochrane Handbook for Systematic Reviews of Interventions*, version 6.5. Cochrane. https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-v
- Stevens A, Hersi M, Garritty C, et al. (2025). Rapid review method series: interim guidance for the reporting of rapid reviews. *BMJ Evid Based Med*. 30(2):118-23. https://doi.org/10.1136/bmjebm-2024-112899
- Tricco AC, Langlois EV, Straus SE (eds) (2017). *Rapid reviews to strengthen health policy and systems: a practical guide*. Geneva: World Health Organization. https://iris.who.int/handle/10665/258698
- WHO Regional Office for Europe (2020). *Evidence briefs for policy. Using the integrated knowledge translation approach. Guiding manual*. Copenhagen. https://iris.who.int/handle/10665/337950

The current Cochrane guidance on rapid reviews (Garritty C, Hamel C, Trivella M, et al. 2024, *BMJ* 384:e076335) could not be opened. The recommendations above come from the 2021 guidance and the Methods Group's 2023 to 2025 series.
