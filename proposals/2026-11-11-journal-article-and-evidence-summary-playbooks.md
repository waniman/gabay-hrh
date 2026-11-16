# Proposal: playbooks for journal articles and evidence summaries

Status: decided by the lead on 2026-11-11. Applied on branch `claude/cool-galileo-j5v6zi`: `playbooks/journal-article.md` (amended) and `playbooks/evidence-summary.md`.
Date: 2026-11-11
Prepared by: coordinator, at the lead's request
Applies to: `playbooks/`, `README.md`

## What is being asked?

The lead is asked to approve, amend or reject two draft playbooks, and to settle three choices inside them:

1. **Journal article** (drafted at `proposals/playbook-drafts/journal-article.md`; now `playbooks/journal-article.md`): an original research article, from analyzed data or an existing draft, to submission and through peer review.
2. **Evidence summary** (drafted at `proposals/playbook-drafts/evidence-summary.md`; now `playbooks/evidence-summary.md`): a summary of the best available evidence on one policy or practice question, prepared in weeks for a named decision-maker.

The drafts follow `playbooks/_template.md` and the work package rules approved on 2026-11-10. On approval, each moves to `playbooks/`. No file outside `proposals/` has been edited.

## What do the drafts answer?

`/new-playbook` asks the lead three questions before drafting. The drafts propose the answers below, taken from the PRPP manuscript and the published guidance. The lead may correct any of them.

| Question | Journal article | Evidence summary |
| --- | --- | --- |
| What does a finished piece look like, and who receives it? | A submitted article with its package: cover letter, reporting checklists, additional files. The journal's editor and reviewers receive it. | A short summary led by key messages, with a technical annex. An official who must decide or advise receives it. |
| Which steps does it always go through? | Brief; diagnosis of an existing draft; analysis and findings; evidence scan and verification; outline; draft; check; revise; co-author rounds; submission; peer review | Brief; protocol; search; screen; extract and appraise; synthesis and certainty; draft; check; revise and review; sign-off |
| Where must the lead approve? | Brief, diagnosis, findings, outline, version for co-authors, each co-author round, submission, each peer-review round | Brief, protocol, findings, merit review (evidence briefs only), final version |

## What was taken from the PRPP manuscript?

The PRPP repository (`waniman/PRDP-paper`) records the article in seven phases, from 24 October to 7 November 2026: setup, an editor's report, re-analysis, reference checks, revision, verification and the submission package. Several of its lessons are already in the template, through the revision playbook, the comment and sent logs, the methods rules and the Word tools. The draft adds the following.

| Lesson from the PRPP record | Where it is in the draft |
| --- | --- |
| The editor's report logged 71 statements, 39 comments and 14 author queries before any text changed (`review/editor_report.md`). | Stage 2, Diagnose |
| A script reproduced 45 of 46 figures in the earlier draft; the one difference was a province counted under three spellings (`analysis/PHASE2_QUANT.md`). | Stage 3, reproduction check |
| The headline claim, "strongest predictor", did not survive the re-analysis and was rewritten (`PHASE2_RESULTS.md`). | Stage 3 ends at a findings gate |
| Five themes entered the Discussion before the coders confirmed them, and their confirmation was still open at the submission run sheet (`manuscript/revised/CHANGE_LOG.md`, query Q19). | Stage 3: a theme enters the text only after the coders confirm it |
| Fit labels in the joint display had no recorded source, and were replaced by labels from a cited methods paper (`review/V3_JZC_REVIEW.md`, C40). | Stage 3: fit labels from a cited source |
| At stage 3 of the PRPP work, the evidence table held 100 sources and 217 claim-passage rows, each with a verdict, a retraction check and a note on whether a guest editor was an author (`HANDOFF.md`, `lit/EVIDENCE_PROTOCOL.md`). | Stage 4 |
| A translation method was written into the Methods with no record, and it was wrong (`review/V3_JZC_REVIEW.md`, C27). | `methods-trace.md` |
| Parts of the statement on AI use were cut in two review rounds and restored each time, because the journal requires every use to be described (`review/V3_JZC_REVIEW.md`, D1; `review/V10.31_COAUTHOR_REVIEW.md`, R4-D9). | `ai-use.md`, kept from the brief stage |
| A web-survey checklist was withdrawn because several items could not be answered from the data (`review/V3_JZC_REVIEW.md`, C16). | Stage 1: check each checklist item can be answered |
| 35 author queries were logged, each with who answers and whether it blocks submission (`review/author_queries.csv`). | `author-queries.md` |
| In the fourth review round, co-authors returned 34 comments, 143 tracked changes and 8 untracked edits. Some additions went beyond the data, and the lead's instruction was to hedge where a hedge works and decline only where it does not (`review/V10.31_COAUTHOR_REVIEW.md`). | Stage 9 |
| An author left the paper, a co-author's new affiliation was the institution of a guest editor, and written approval was needed from all eight authors (`submission/RUN_SHEET.md`). | Stage 10 |

## What do the publication standards add to the journal article?

- **Authorship.** The International Committee of Medical Journal Editors (ICMJE) sets four criteria, and states that "All those designated as authors should meet all four criteria for authorship, and all who meet the four criteria should be identified as authors" (ICMJE, 2026). It advises deciding authorship "when planning the work". BMC does not allow authors to be added, removed or reordered after acceptance (BMC, n.d.). The draft settles authors at the brief gate and confirms them at submission.
- **AI use.** The ICMJE asks authors to describe AI use "in both the cover letter and the submitted work", and, for AI used to conduct a study, "the tool used, version, and prompts where applicable" (ICMJE, 2026). BMC Health Services Research asks for all use of a large language model in the Methods (BMC Health Services Research, n.d.).
- **Who interprets.** Springer Nature lists "generating scientific claims or interpretations" among AI uses it does not permit, and states that "the argument, interpretation, and conclusions must be author-led" (Springer Nature, n.d.). The draft therefore has the lead and co-authors supply the interpretation and conclusions at the findings and outline gates. The writer drafts from them.
- **Reporting checklists.** The EQUATOR Network advises that checklists are "best used at the end of writing, before journal submission" (EQUATOR Network, n.d.). For surveys, EQUATOR lists the Consensus-Based Checklist for Reporting of Survey Studies (CROSS) for "both web- and non-web-based surveys" (EQUATOR Network, n.d.).
- **Peer review.** Responses should answer every point and "specify whether you refer to the line numbers from the original or the revised manuscript" (Noble, 2017). An analysis a reviewer requests still goes to the lead as a method memo before it runs, as `core/methods-rules.md` requires.

The statement of the Committee on Publication Ethics (COPE) on authorship and AI tools could not be opened, and is not cited.

## What is an evidence summary, and how does it relate to systematic reviews and meta-analyses?

An evidence summary sits downstream of systematic reviews. It uses them as its main inputs, or borrows their methods in a shortened form. A meta-analysis is not a type of review: it is a statistical step inside a systematic review.

### What do the main types of synthesis do?

The names overlap. Grant and Booth (2009) found that "Few review types possess prescribed and explicit methodologies and many fall short of being mutually exclusive". A 2025 overview treats "rapid" and "living" as modes that can be applied to several types of synthesis (Nussbaumer-Streit et al., 2025). The table sets out the types this proposal relies on.

| Type | What it answers | Inputs | Typical time | Reporting standard |
| --- | --- | --- | --- | --- |
| Systematic review | All the evidence that fits set criteria, on a specific question, found and appraised with explicit methods | Primary studies | 12 to 24 months (Tricco et al., 2017) | PRISMA 2020 |
| Meta-analysis | A pooled estimate across studies, inside a systematic review or overview | Results of two or more studies | Part of a review | PRISMA 2020 |
| Overview of reviews | What existing systematic reviews show; also called an umbrella review | Systematic reviews | Not stated in the sources read | PRIOR |
| Rapid review | A systematic review question, answered faster with stated shortcuts | Primary studies, sometimes reviews | 5 to 12 weeks on average (Tricco et al., 2017) | PRISMA 2020 as the base; no rapid review extension yet |
| Evidence summary | A rapid review that mainly summarizes existing systematic reviews | Systematic reviews first | 5 weeks or less, in one program (Khangura et al., 2012) | As for a rapid review |
| Evidence brief for policy | A problem, options and implementation considerations, for a decision | Systematic reviews and local evidence | Days and weeks (Lavis et al., 2009) | WHO guiding manual |
| Scoping review | What evidence exists on a topic, and its gaps | Any source | Not stated in the sources read | PRISMA for Scoping Reviews |
| Evidence and gap map | Where evidence exists and where it does not, shown visually | Reviews and studies | 6 to 12 months (White et al., 2020) | Campbell guidance |

Four points follow from the sources.

- **A systematic review is the full method.** It "attempts to collate all the empirical evidence that fits pre-specified eligibility criteria in order to answer a specific research question" (Lasserson et al., 2024). A new one takes "an average of 12–24 months" (Tricco et al., 2017).
- **A meta-analysis is optional inside a review.** It is "the statistical combination of results from two or more separate studies", and "A systematic review need not contain any meta-analyses" (Deeks et al., 2026). It is appropriate only when studies are similar enough to give a meaningful summary.
- **An evidence summary reuses reviews.** Khangura et al. (2012) placed emphasis "on locating and summarizing evidence from relevant and high quality systematic reviews". Their summaries report the meta-analyses in included reviews but "do not undertake this level of quantitative synthesis". In an overview of reviews, "the unit of searching, inclusion and data analysis is the systematic review rather than the primary study" (Pollock et al., 2024).
- **A rapid review shortens named steps.** The WHO guide defines a rapid review as one in which "systematic review processes are accelerated and methods are streamlined" (Tricco et al., 2017). The Cochrane Rapid Reviews Methods Group recommends at least two information sources (Klerings et al., 2023). It also recommends screening 20% of records by two reviewers, then continuing with one if agreement is about 80%; and one reviewer extracting data and appraising studies, with a second checking (Nussbaumer-Streit et al., 2023).

### Where does this team fit?

The draft playbook offers three forms, chosen at the brief:

- **A. Summary of reviews (default).** Existing systematic reviews and guidelines first, with primary studies only where reviews are missing. It reports the reviews' pooled estimates and certainty ratings and does not pool data again.
- **B. Rapid review.** Primary studies, with the Methods Group's shortcuts stated in the annex.
- **C. Evidence brief for policy.** Form A or B, set out as the problem, options and implementation considerations for a decision. The WHO manual uses one page of key messages, three pages of executive summary and up to 25 pages of full text, and states that "recommendations should never be provided" (WHO Regional Office for Europe, 2020).

A new systematic review, a meta-analysis, a scoping review and an evidence and gap map are out of scope. A systematic review takes 12 to 24 months (Tricco et al., 2017) and an evidence and gap map 6 to 12 months (White et al., 2020), well beyond the weeks a summary allows. Each would need its own playbook. Any new pooled estimate is a new analysis under `core/methods-rules.md`.

There is no published reporting guideline for rapid reviews. Interim guidance advises using "PRISMA 2020 as the foundation for reporting" (Stevens et al., 2025), and the PRISMA website lists a rapid review extension as under development. The draft forbids claiming compliance with a "PRISMA-RR" checklist.

## Which decisions are the lead's?

1. **Approve, amend or reject the journal-article playbook.**
2. **Approve, amend or reject the evidence-summary playbook.**
3. **The second screener in an evidence summary.** The Methods Group's checks assume a second person. The sources read do not say whether an AI call can fill that role.
   - Option A (recommended): a separate AI call screens the 20% sample and verifies extraction, and the annex says so. The lead names a person for the 20% sample when the summary is meant for publication in a journal. This keeps a summary for an office within weeks, and is honest about who checked what.
   - Option B: a named person screens the 20% sample in every summary. This is closer to the guidance, and adds a person's time to every work package.
4. **Who interprets in a journal article.** Recommended: apply the rule to every journal: the lead and co-authors supply the interpretation, Discussion points and conclusions, and the writer drafts from them. The alternative is to apply it only where a journal's AI policy requires it, as Springer Nature's does.
5. **Other synthesis playbooks.** Recommended: draft a systematic review or scoping review playbook only when a project needs one.

## How would the lead answer?

Reply in chat, for example:

- "Approve both as recommended."
- "Approve both; option B for the second screener."
- "Approve the journal article; hold the evidence summary."

On approval, the coordinator moves each draft to `playbooks/`, commits it as "Playbook: <type>", updates the playbook list in `README.md`, and pushes.

## What did the lead decide?

On 2026-11-11 the lead answered:

1. **Journal article: amended.** Agents may generate possible scientific claims and interpretations. The lead and co-authors validate them, and supply further interpretation and conclusions.
2. **Evidence summary: approved,** with the same amendment on interpretation.
3. **Second screener: a person every time.** The lead disagreed with the recommendation. A named person screens the 20% sample and verifies the extraction in every evidence summary.
4. **Who interprets: not as recommended.** Decision 1 replaces the recommendation that authors supply every interpretation.
5. **Other synthesis playbooks:** drafted only when a project needs one. Agreed.

## What was applied?

- **Interpretations.** The journal-article playbook keeps a new record, `interpretations.md`: one row per proposed or author-supplied interpretation, with the findings it rests on, who proposed it and the authors' decision. Only validated, changed and author-supplied rows enter the text, and the check stage traces each interpretation to its row. The statement on AI use says that AI proposed interpretations the authors validated. The evidence-summary playbook applies the same rule at its findings gate.
- **Journal policies.** Springer Nature lists "generating scientific claims or interpretations" among AI uses it does not permit (Springer Nature, n.d.). The journal-article playbook therefore has the compliance check read the target journal's AI policy at stage 1. Where the policy does not permit AI-proposed interpretations, the lead receives a memo before the outline: for that journal the authors supply every interpretation, or the lead chooses another journal. This keeps the lead's rule as the default, and puts any conflict with a journal in front of the lead early.
- **Second screener.** The evidence-summary brief names the person, with the time they can give. At stage 4 that person screens the 20% sample; if agreement is below 80%, they screen every remaining record. At stage 5 they verify each extracted figure; a separate AI call may list discrepancies first. For quality appraisal, the lead decided on 2026-11-11 that an agent appraises each source first and the named person then appraises it, starting from the agent's draft; the person's judgement is final, and each change is recorded with its reason.
- **Files.** Both playbooks moved from `proposals/playbook-drafts/` to `playbooks/`. `README.md` lists four playbooks. `tools/test_team.py` gained two tests: every playbook's stages are numbered in order with distinct checkpoints, and `init` accepts the two new playbooks. All 20 tests pass.

## Sources

The sources of each playbook are listed at its end. This proposal also draws on the following. Each was opened on 11 November 2026, except where marked.

How the sources were checked: two research calls found the sources and quoted them. A separate call that saw only the claim list then verified 23 claims on evidence synthesis: 19 verified, 4 corrected, none unfound. Only the corrected wording is used (`proposals/playbook-drafts/verification-evidence-summary.md`). The journal standards and the two WHO documents were checked by matching each quotation against the saved source text.

- Grant MJ, Booth A (2009). A typology of reviews: an analysis of 14 review types and associated methodologies. *Health Info Libr J*. 26(2):91-108. Abstract only. https://doi.org/10.1111/j.1471-1842.2009.00848.x
- Lasserson TJ, Thomas J, Higgins JPT (2024). Chapter 1: Starting a review (last updated August 2021). In: *Cochrane Handbook for Systematic Reviews of Interventions*, version 6.5. Cochrane. https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-01
- Nussbaumer-Streit B, Booth A, Garritty C, Hamel C, et al. (2025). Overview of evidence synthesis types and modes. *J Clin Epidemiol*. 187:111970. Abstract only. https://doi.org/10.1016/j.jclinepi.2025.111970
- Page MJ, McKenzie JE, Bossuyt PM, et al. (2021). The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. *BMJ*. 372:n71. https://doi.org/10.1136/bmj.n71
- PRISMA Statement (n.d.). *Extensions*. https://www.prisma-statement.org/extensions
- White H, Albers B, Gaarder M, et al. (2020). Guidance for producing a Campbell evidence and gap map. *Campbell Syst Rev*. 16(4):e1125. https://doi.org/10.1002/cl2.1125
- The PRPP manuscript repository, `waniman/PRDP-paper`, at commit `0e78242` (7 November 2026). Files as cited above.
