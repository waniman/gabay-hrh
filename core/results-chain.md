# Results chain

Each project states, on one page, what it delivers, the outcomes it aims to influence, the impact it contributes to, and the assumptions outside its control. The page is `project/results.md`. The lead approves it at the project frame gate (`core/project-and-work-packages.md`).

Approved by the lead on 2026-11-10 (`proposals/2026-11-10-work-packages-and-results-chain.md`).

## Terms

The team uses five terms, each for one thing only. The first three follow the glossary of the Organisation for Economic Co-operation and Development (OECD, 2023). The degrees of control follow Mayne (2008).

| Term | Meaning | Degree of control | What the team does |
| --- | --- | --- | --- |
| Work package | A substantial part of the project's work, following one playbook | Direct control | Plans and runs it |
| Output | A product the project delivers | Direct control | Delivers it through the playbook's stages, checks and gates |
| Outcome | A change in what the intended users know, decide or do, to which the outputs contribute | Direct influence | Designs each output for a named user and use; records what is observed |
| Impact | The change in people's conditions or well-being to which the project contributes | Indirect influence | States the contribution and its assumptions; makes no claim of attribution |
| Assumption | A condition outside the project that must hold for one level to lead to the next | None | Lists it; reports to the lead when one fails |

The OECD defines outcomes as "the short-term and medium-term effects of an intervention's outputs", impacts as "the higher-level effects of an intervention's outcomes", and assumptions as "the conditions necessary for the cause-and-effect relationships between the different levels of results" (OECD, 2023). Mayne (2008) places outputs under direct control, and immediate and some intermediate outcomes under direct influence. Results that depend on people the project does not reach directly, or on other factors, fall under indirect influence.

### When a funder uses other terms

Frameworks draw the levels differently. Global Affairs Canada splits outcomes into immediate, intermediate and ultimate (Global Affairs Canada, 2025). The Horizon Europe application form uses results, outcomes and impacts (European Commission, 2026). Write the funder's terms beside the team's terms in the project brief, under "Terms for results". The output for that funder uses the funder's terms; the project files keep the team's terms.

## What goes in `project/results.md`

1. **Impact.** One sentence: whose conditions should change, and in what way.
2. **Outcomes.** Two or three, numbered O1, O2 and so on. Each names who should know, decide or do what, and ends with `By: YYYY-MM-DD`.
3. **Outputs.** Each output, its work package, and the outcome it serves.
4. **Assumptions.** Numbered A1, A2 and so on.
5. **Signals.** For each outcome, what would show that it happened, and where it would be seen.

Write each outcome on one line that starts `- O1.`, so the tool can read it. An outcome is a change in a person or an office, not a product: "The funder invites a full proposal" is an outcome; "A concept note is submitted" is an output.

## What the team does at each level

### Outputs: deliver

The playbook's stages, checks and gates apply. Each work package brief names the outcome its output serves, and the intended user and use. The blind reviewer tests the draft against that use.

### Outcomes: design for use, then record what is observed

- **Before sending.** At a work package's final gate, the gate memo names the outcome the output serves. The team may draft what promotes its use: a cover note, a summary for a named office, a list of people to brief. A person sends each of them (`CLAUDE.md`, rule 4).
- **After sending.** When the lead, a partner or the team sees a signal, log it:

```
python3 tools/team.py outcome add --outcome O1 \
  --observed "The funder invited a full proposal, due 30 April." \
  --source "project/sources/invitation-2027-03-04.pdf" \
  --by "<who reported it>" \
  --other-factors "The funder widened the call in February."
```

- **At each run.** Ask the lead for signals when an outcome's date is near. `python3 tools/team.py outcome show` lists each outcome with what has been observed.

### Impact: state the contribution

Write, in `results.md`, how the outcomes are expected to contribute to the impact, and the assumptions this rests on. The team records no measurement of impact. In any output, the claim is that the project contributes to the impact with others.

### Assumptions: watch

When an assumption fails or is in doubt, send a memo to the lead. It can change scope (`core/escalation-threshold.md`, item 2). Examples: a funder closes a call; an office postpones the policy the output was written for.

## The outcome log

The log is `project/register/outcomes.csv`, one row per observed signal.

| Field | Content |
| --- | --- |
| id | OB-001, OB-002 and so on, never reused (set by the tool) |
| date | The date the signal was observed |
| outcome | The outcome it relates to, as numbered in `results.md` |
| observed | What was observed, in one sentence |
| source | The file, link or message that shows it |
| reported_by | Who reported it |
| other_factors | Other factors that may explain what was observed, or "none identified" |

## Rules

- **Log an outcome only with a source.** An outcome with no source is not logged. `CLAUDE.md` forbids inventing a citation, number, quotation or partner commitment; the same holds for an outcome.
- **Name the other factors.** Every row states what else may explain the observation. Mayne (2008) makes identifying "the other key influencing factors" a step of contribution analysis.
- **Claim contribution, never attribution.** The OECD defines contribution as "the role or part played by an intervention, together with other interventions, in bringing about an observed (or expected) result" (OECD, 2023). Write "contributed to", with the source, and name the other factors where the reader needs them.
- **A missing signal is a finding.** At project close, the after-action reviewer reports each outcome as observed, not observed, or not yet observable. Outcomes often arrive after the last output is sent.
- **Never edit or delete a row.** A signal later found to be wrong is corrected by a new row that says so.
- **Changing an outcome changes scope.** A change to the impact, an outcome or an assumption in `results.md` goes to the lead.

## Health check

The weekly health check flags an outcome whose date has passed with no row in the outcome log (`core/learning-and-oversight.md`). The flag asks the coordinator to ask the lead whether anything was observed. It does not mean the project failed.

## Sources

- European Commission (2026). *Standard Application Form (HE RIA and IA): Project proposal, Technical description (Part B)*. Version 5.1, 22 January 2026. https://ec.europa.eu/info/funding-tenders/opportunities/docs/2021-2027/horizon/temp-form/af/af_he-ria-ia_en.pdf
- Global Affairs Canada (2025). *Results-Based Management Tip Sheet 2.1: Results Chains and Definitions*. Date modified 2025-08-21. https://www.international.gc.ca/world-monde/funding-financement/rbm-gar/tip_sheet_2-1-fiche_conseil_2-1.aspx?lang=eng
- Mayne J (2008). *Contribution analysis: An approach to exploring cause and effect*. ILAC Brief 16. Institutional Learning and Change Initiative. https://cgspace.cgiar.org/items/fdcce0f6-ad3b-4d8a-9b7f-8d1c7c820405
- OECD (2023). *Glossary of Key Terms in Evaluation and Results Based Management for Sustainable Development* (Second edition). Paris: OECD Publishing. https://alnap.org/help-library/resources/glossary-key-terms-evaluation-and-rbm-2023/
