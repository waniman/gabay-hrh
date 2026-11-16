# Proposal: projects with several work packages, and a results chain from outputs to impact

Status: approved by the lead on 2026-11-10, as recommended. Applied on branch `claude/cool-galileo-j5v6zi`.
Date: 2026-11-10
Prepared by: coordinator, at the lead's request
Applies to: the agent-team template repository (`CLAUDE.md`, `core/`, `playbooks/`, `.claude/`, `tools/`, `project-template/`, `addons/`)

## What is being asked?

The lead is asked to approve, amend or reject one change to the template, in two parts:

1. **Part A, work packages.** A project holds one or more work packages. Each work package follows one playbook and delivers one or more outputs.
2. **Part B, results chain.** Each project states, on one page, the outputs it delivers, the outcomes it aims to influence, the impact it contributes to, and the assumptions outside its control.

The six rules in `CLAUDE.md` stay as they are. Rule 6 is extended: one project may use several playbooks, one per work package.

No file outside `proposals/` has been edited. The edits listed below are applied only after the lead approves them.

## Why is the change needed?

The template currently assumes one output per project. `CLAUDE.md` describes "one undertaking: a concept note, a proposal, an article, a review". `project/state.md` holds one `Type:` line, one `Stage:` line and one `Master copy:` line. `tools/team.py init` accepts one playbook and refuses a second project in the same repository.

A project that needs several outputs has two options today, and both lose information. Running each output as a separate project splits the decision register, so a decision made for one output cannot be traced when it shapes another. Running all outputs under one playbook removes the gates and checks the other outputs need.

The template also stops at delivery. The brief asks who will read the output and "what should they decide or do after reading it" (`project-template/brief.md`), but no file records whether that happened. The last stage of both playbooks is the after-action review, which reviews the team's process.

## Which terms do the standard frameworks use?

The lead proposed two levels above outputs: intermediate outcomes, which the project influences in part, and outcomes, which lie outside the project's influence. The standard frameworks keep the same logic and use different names. They also place a third category, assumptions, outside the chain.

The table below sets the lead's terms beside three published frameworks. The headline difference is that the highest level is named impact or ultimate outcome, and the project contributes to it. The first three row labels are Mayne's; the fourth is added here.

| Degree of control (Mayne, 2008) | OECD (2023) | Global Affairs Canada (2022, 2025) | Horizon Europe (2026) | The lead's term |
| --- | --- | --- | --- | --- |
| Direct control | Outputs | Outputs | Results, deliverables | Outputs |
| Direct influence | Outcomes | Immediate outcomes; intermediate outcomes | Outcomes | Intermediate outcomes |
| Indirect influence | Impacts | Ultimate outcome | Impacts | Outcomes |
| Outside the project | Assumptions | Assumptions, risks | Critical risks (closest term) | Non-controllable factors |

Three points follow from the sources.

- **The highest level is contributed to.** The Organisation for Economic Co-operation and Development (OECD) defines outcomes as "the short-term and medium-term effects of an intervention's outputs" and impacts as "the higher-level effects of an intervention's outcomes" (OECD, 2023). Global Affairs Canada defines the ultimate outcome as "the highest-level change to which an organization, policy, program, or project contributes" (Global Affairs Canada, 2025). A level the project cannot influence at all would give the project no reason to exist.
- **Control declines by degrees.** Mayne (2008) describes three circles: direct control, "typically at the output level"; direct influence, "typically the immediate outcomes and perhaps some intermediate outcomes"; and indirect influence, where the program "can exert significantly less influence". Global Affairs Canada states that outcomes "are not entirely within the control of a single organization, policy, program or project; instead they are within the area of the organization's influence" (Global Affairs Canada, 2025).
- **Factors fully outside the project are assumptions.** The OECD defines assumptions as "the conditions necessary for the cause-and-effect relationships between the different levels of results" (OECD, 2023). The lead's "non-controllable factors" belong here. They are written beside the chain, and the team watches them.

The frameworks draw the lower boundary differently. The OECD counts "changes in knowledge, skills, or abilities produced by the activities" as outputs (OECD, 2023). Global Affairs Canada counts a "change in capacities of intermediaries or beneficiaries" as an immediate outcome (Global Affairs Canada, 2025). A project therefore needs one vocabulary, fixed at the start, and a note of the funder's equivalent terms.

The term "work package" is standard. The Horizon Europe application form asks that "each work package should be a substantial part of the work plan" and that the number of work packages "be proportionate to the scale and complexity of the project" (European Commission, 2026). The same form numbers each deliverable by its work package: deliverable 4.2 is the second deliverable of work package 4.

The claim a project can make about outcomes is a contribution claim. The OECD defines contribution as "the role or part played by an intervention, together with other interventions, in bringing about an observed (or expected) result" (OECD, 2023). Outcome Mapping takes the same position: a program "is not claiming the achievement of development impacts; rather, the focus is on its contributions to outcomes" (Earl, Carden and Smutylo, 2001).

## What is recommended?

Five terms are recommended for the template, each used for one thing only. They follow the OECD glossary, with Mayne's degrees of control attached.

| Term | Meaning in the template | Degree of control | What the team does |
| --- | --- | --- | --- |
| Work package | A substantial part of the project's work, following one playbook | Direct control | Plans and runs it |
| Output | A product the project delivers: a concept note, a report, a manuscript, a dataset | Direct control | Delivers it through the playbook's stages, checks and gates |
| Outcome | A change in what the intended users know, decide or do, to which the outputs contribute | Direct influence | Designs each output for a named user and use; records what is observed |
| Impact | The change in people's conditions or well-being to which the project contributes | Indirect influence | States the contribution and its assumptions; makes no claim of attribution |
| Assumption | A condition outside the project that must hold for one level to lead to the next | None | Lists it; reports to the lead when one fails |

When a funder's template splits outcomes into immediate and intermediate, the project brief records the funder's terms beside the template's terms.

---

## Part A: How would work packages change a project?

### What would happen?

A project would hold one or more work packages, numbered WP1, WP2 and so on. Each work package has its own brief, playbook, stages, gates, master copy and checkpoints. The project keeps one lead, one decision register, one comment log, one sent log, one set of memos, one lessons file and one weekly health check.

A project with a single output would have one work package, WP1. One layout serves both cases, so the tool and the rules need one path.

### How would the project folder be laid out?

```
project/
  state.md                 the project: lead, partners, the work package table, what waits on the lead, lessons in force
  status.md                five lines after each run, as now
  brief.md                 the project brief: purpose, audience, funder, limits, partners
  results.md               the results chain (Part B)
  lessons.md               as now
  register/                decisions.csv, comments.csv, sent.csv, each with a work_package column
  escalations/  health/  sources/  trace/      as now
  wp/
    WP1-<short-name>/
      brief.md             what this work package must deliver, for whom, and by when
      state.md             Type, Stage, Master copy, Open tasks, as state.md holds today
      work/                outline, drafts, evidence file, final version; frozen/ and sent/
      reviews/             evidence checks, blind reviews, compliance checks
    WP2-<short-name>/
      ...
```

### What rules would apply?

- **Project frame gate.** Before any work package starts, the lead approves the project brief, the list of work packages with their playbooks, order and due dates, and the results chain. One memo covers all three.
- **Adding, dropping or merging a work package** changes scope. It goes to the lead under item 2 of `core/escalation-threshold.md`.
- **Dependencies are written down.** The work package table in `project/state.md` names what each work package waits for, for example "WP3 waits for the WP2 evidence file at `cp-wp2-evidence-01`".
- **A run works on one work package at a time.** It takes the first work package, in the approved order, that has a task not waiting on the lead or on another work package. When that work package stops, the run moves to the next until the time limit.
- **Checkpoints carry the work package.** Tags take the form `cp-wp2-outline-01`. A rollback restores one work package's `work/` folder and marks only that work package's later decisions as rolled back.
- **Independent checks keep their limits.** The blind reviewer receives the draft and that work package's `brief.md` only. The process monitor receives the facts file, `project/state.md`, `project/brief.md` and the register.
- **Verified evidence is shared.** A finding verified in one work package can be cited in another. A finding still marked first pass cannot.

### Example: a project with three work packages

This example is illustrative. The project, dates and ids are hypothetical.

| WP | Title | Playbook | Output | Waits for | Due |
| --- | --- | --- | --- | --- | --- |
| WP1 | Evidence summary | (new playbook needed) | Evidence summary, 10 pages | None | 2027-01-15 |
| WP2 | Concept note | `concept-note` | Concept note to the funder, 5 pages | WP1 evidence file | 2027-02-01 |
| WP3 | Journal article | (new playbook needed) | Manuscript | WP1 sign-off | 2027-04-30 |

The example shows a limit of the present template. Two of the three work packages need playbooks that do not yet exist. `/new-playbook` drafts them, and the lead approves each one.

### Which files would change?

| # | File | Change |
| --- | --- | --- |
| A1 | `core/project-and-work-packages.md` | New. The terms, the folder layout, the project frame gate, the order of work, dependencies, and how to add or drop a work package. |
| A2 | `CLAUDE.md` | Opening paragraph and "Start of every session": a project holds work packages; read the project state, then each active work package's state. Rule 6 extended. Link to A1. |
| A3 | `project-template/` | `state.md` becomes the project state with the work package table. New `wp-template/` with `brief.md`, `state.md`, `work/` and `reviews/`. `brief.md` becomes the project brief. A `work_package` column in the three CSV files. |
| A4 | `tools/team.py` | `init` creates the project and WP1. New `wp add` and `wp list`. `--wp` on `register add`, `comment add`, `sent add`, `checkpoint` and `rollback`. `status` and `health` report each work package. Python standard library only. |
| A5 | `core/run-rules.md`, `core/checkpoint-rules.md`, `core/register-schema.md`, `core/comment-log.md`, `core/documents.md` | Paths, the `work_package` field, tag names, and the order of work in a run. |
| A6 | `core/learning-and-oversight.md` | Health measures computed for each work package. Two measures added: a work package past its due date, and a work package blocked by another for more than a set number of days. |
| A7 | `playbooks/_template.md`, `concept-note.md`, `revision.md` | Paths point to the work package folder. A line states which output the playbook produces. |
| A8 | `.claude/commands/` | `/new-project` asks for the project frame. New `/new-work-package`. `/continue` and `/status` take an optional work package. |
| A9 | `.claude/agents/` | File paths in each agent's instructions. The after-action reviewer runs in final mode at each work package sign-off and once at project close. |
| A10 | `addons/*/README.md`, `README.md` | One Drive subfolder for each work package; tracker task titles carry the work package id; the README describes the new layout. |

### What would it cost?

- One additional gate at the start of each project, the project frame.
- One additional folder level, including on single-output projects.
- A change to most commands in `tools/team.py`, which gain a work package argument. The repository holds no automated tests for the tool today, so tests are written with this change.
- Projects already made from the template keep the version they were made from. No project is migrated.

---

## Part B: How would the results chain be used?

### What would happen?

Each project would hold a one-page file, `project/results.md`, approved at the project frame gate. It states:

1. **Impact.** One sentence: whose conditions should change, and in what way.
2. **Outcomes.** Two or three. Each names who should know, decide or do what, and by when.
3. **Outputs.** Each output, its work package, and the outcome it serves.
4. **Assumptions.** The conditions outside the project that must hold between outputs and outcomes, and between outcomes and impact.
5. **Signals.** For each outcome, what would show that it happened, and where the team or the lead would see it.

### What would the team do at each level?

- **Outputs: deliver.** The playbook's stages, checks and gates apply as now.
- **Outcomes: design for use, then record what is observed.** Each work package brief names the intended user and the use expected of the output. The blind reviewer already sees the brief, so its review tests the draft against that use. After a person sends an output, observed signals are logged with their source: a reply from the funder, a citation, an invitation, a change in a policy instrument.
- **Impact: state the contribution.** The team writes how the outcomes are expected to contribute to the impact and lists the assumptions. It records no measurement of impact and makes no claim that the project caused it.
- **Assumptions: watch.** An assumption that fails is reported to the lead in a memo, because it can change scope (`core/escalation-threshold.md`, item 2).

### What limits would apply?

- The team still never sends, submits or publishes (`CLAUDE.md`, rule 4). Steps that promote use of an output are drafted by the team and carried out by a person.
- An outcome is logged only with a source. `CLAUDE.md` already forbids inventing a citation, number, quotation or partner commitment; an outcome with no source falls under the same rule.
- Every outcome row carries a note on other factors that may explain the observation. Mayne (2008) makes identifying "the other key influencing factors" a step of contribution analysis.
- Outcomes often arrive after the last work package is signed off. The Horizon Europe form notes that impacts "generally occur some time after the end of the project" (European Commission, 2026). The project close therefore states which outcomes were observed, which were not, and which could not yet be observed.

### Example: a results chain

This example is illustrative and continues the hypothetical project above.

> **Impact.** People in rural municipalities receive primary care from an adequately staffed health workforce.
>
> **Outcomes.**
> - O1. The funder invites a full proposal by March 2027.
> - O2. The national health department's workforce bureau uses the cost estimates in its next staffing standard.
>
> **Outputs.** Evidence summary (WP1, serves O1 and O2). Concept note (WP2, serves O1). Journal article (WP3, serves O2).
>
> **Assumptions.** The funder's call stays open. The bureau revises the staffing standard in 2027. Local governments have budget room to hire.
>
> **Signals.** O1: a written invitation from the funder. O2: the estimates cited in a draft or issued standard.

An outcome row would then read: "O-001, 2027-03-04, O1, written invitation received from the funder, source `project/sources/invitation.pdf`, reported by the lead, other factors: the funder widened the call in February."

### Which files would change?

| # | File | Change |
| --- | --- | --- |
| B1 | `core/results-chain.md` | New. The five terms, the degrees of control, what the team does at each level, the limits, and the sources cited in this proposal. |
| B2 | `project-template/results.md` | New. The five headings above, with one line of guidance each. |
| B3 | `project-template/wp-template/brief.md` | Two lines added: the outcome this output serves, and the intended user and use. |
| B4 | `project-template/register/outcomes.csv`, `tools/team.py` | New outcome log and `outcome add`, `outcome show`. Fields: id, date, outcome, what was observed, source, reported by, other factors. |
| B5 | `.claude/agents/blind-reviewer.md`, `.claude/agents/after-action-reviewer.md` | The blind reviewer tests the draft against the intended use in the brief. The after-action reviewer, at project close, reports on outcomes observed, not observed and not yet observable, and on each assumption. |
| B6 | `core/decision-memo-template.md` | An optional line in gate memos: "Outcome this output serves". |
| B7 | `core/learning-and-oversight.md` | One health measure added: an outcome whose date has passed with no row in the outcome log (amber). |

### What would it cost?

- One page to write and approve at the start of each project.
- One row for each observed signal. The lead or a partner supplies most of them, because they receive the replies.
- There are no adequate data yet on how much time the outcome log takes. The first project that uses it would report this in its after-action review.

---

## What does this proposal leave out?

- **Programs.** A program groups several projects. Each project keeps its own repository; no program level is proposed.
- **New playbooks.** Evidence summaries, journal articles, slide decks and analyses each need a playbook. They are drafted one at a time with `/new-playbook`.
- **Budgets and person-time for each work package.** The template does not track resources today, and this proposal does not add it.
- **Impact evaluation.** The team states a contribution and does not measure impact.

## Which decisions are the lead's, and which can be delegated?

### For the lead's decision

1. **Approve, amend or reject Part A (work packages).**
2. **Approve, amend or reject Part B (results chain).** Part B depends on Part A for the work package brief. Part A can be approved alone.
3. **Vocabulary.** The recommendation is the OECD's three levels: outputs, outcomes and impact. The alternative is the four levels of Global Affairs Canada: outputs, immediate outcomes, intermediate outcomes and ultimate outcome. The three-level form matches the OECD glossary and the Horizon Europe form, and it is shorter for a project of a few outputs. The four-level form is closer to the lead's own wording.
4. **Single-output projects.** The recommendation is that every project has at least WP1. The alternative keeps today's flat layout for single-output projects and needs two code paths in the tool.
5. **Outcome log.** The recommendation is to add it, with the fields in B4. The alternative is to state outcomes in `results.md` and review them only at project close.

### Delegable to the coordinator once approved

- The exact wording of the edits listed in A1 to A10 and B1 to B7.
- Tests for the changes to `tools/team.py`.
- Default thresholds for the three new health measures. The lead can change them in `team.config.yaml`.

## How would the lead answer?

Reply in chat, for example:

- "Approve A and B as recommended."
- "Approve A and B. Use the four outcome levels."
- "Approve A. Hold B."

After an approval, the coordinator applies the edits on a branch and lists the changed files for review before merging.

## What did the lead decide?

On 2026-11-10 the lead answered "Approve A and B as recommended":

1. Part A, work packages: approved as recommended.
2. Part B, results chain: approved as recommended.
3. Vocabulary: the three levels of the OECD glossary (outputs, outcomes, impact). Agreed.
4. Single-output projects: every project has at least WP1. Agreed.
5. Outcome log: added. Agreed.

The lead deferred the playbooks for evidence summaries and journal articles. They are drafted later with `/new-playbook`.

## What was applied?

The rules are in `core/project-and-work-packages.md` and `core/results-chain.md`. Edits A1 to A10 and B1 to B7 were applied as listed, on top of the change merged to the default branch in the meantime ("Let the team run inside an existing repository"). Eight points differ from the lists above or add to them:

- **The work package table is generated.** `python3 tools/team.py wp list` builds the table from each work package's `state.md`, and the health facts file and `status` include it. `project/state.md` holds the order of work and points to the command. One source for stage and status means the table and the state files cannot disagree.
- **Observed outcomes are numbered OB-001, OB-002.** The outcomes stated in `results.md` are numbered O1, O2. The example row in Part B used O-001, which reads too much like O1.
- **A work package's deadline is the `- Deadline:` line of its brief.** The state file holds no second date. Its `Due:` line stays optional, for the current stage.
- **`wp add` needs the lead's answer.** The tool refuses to create a work package unless `--ref` names a decided memo or an approved register row.
- **Each memo names its work package.** The memo template gained a `Work package:` line, filled by `memo new --wp`.
- **`project/reviews/` is kept** for checks of the project frame. Reviews of a work package are in its own `reviews/` folder.
- **The project frame gate has no gate review,** because no stage comes before it.
- **Waiting is dated.** A work package stopped for another carries `Status: waiting (since <date>)`, so the tool can count the days. Waiting with no date is flagged amber.

The three new health measures use these defaults, set in `team.config.yaml`: a work package past its deadline, amber at 1 day and red at 7; a work package waiting on another, amber at 7 days and red at 14; an outcome past its date with nothing observed, amber. The tracker mapping in `team.config.yaml` now puts the work package in each task title.

`tools/test_team.py` holds 18 tests of the tool, run with `python3 tools/test_team.py`. They cover the first work package, adding a work package, the `--wp` argument in each log, checkpoint names, a rollback that changes one work package only, the export check for an outside master, the outcome log, and the health measures.

Two limits remain. Projects made from the template before this change keep the earlier layout, and no project was migrated. A work package of a type other than a concept note or a revision cannot start until its playbook exists.

## Sources

Each source was opened on 2026-11-10. Quotations are verbatim.

- Earl S, Carden F, Smutylo T (2001). *Outcome Mapping: Building Learning and Reflection into Development Programs*. Ottawa: International Development Research Centre. https://idrc-crdi.ca/sites/default/files/openebooks/959-3/index.html
- European Commission (2026). *Standard Application Form (HE RIA and IA): Project proposal, Technical description (Part B)*. Version 5.1, 22 January 2026. https://ec.europa.eu/info/funding-tenders/opportunities/docs/2021-2027/horizon/temp-form/af/af_he-ria-ia_en.pdf
- Global Affairs Canada (2022). *Results-Based Management for International Assistance Programming at Global Affairs Canada: A How-to Guide*. Updated June 2022. https://international.gc.ca/world-monde/funding-financement/results_based_management-gestion_axee_resultats-guide.aspx?lang=eng
- Global Affairs Canada (2025). *Results-Based Management Tip Sheet 2.1: Results Chains and Definitions*. Date modified 2025-08-21. https://www.international.gc.ca/world-monde/funding-financement/rbm-gar/tip_sheet_2-1-fiche_conseil_2-1.aspx?lang=eng
- Mayne J (2008). *Contribution analysis: An approach to exploring cause and effect*. ILAC Brief 16. Institutional Learning and Change Initiative. https://cgspace.cgiar.org/items/fdcce0f6-ad3b-4d8a-9b7f-8d1c7c820405
- OECD (2023). *Glossary of Key Terms in Evaluation and Results Based Management for Sustainable Development* (Second edition). Paris: OECD Publishing. Read from the copy held by ALNAP: https://alnap.org/help-library/resources/glossary-key-terms-evaluation-and-rbm-2023/

Two limits on the sources apply. The How-to Guide of Global Affairs Canada was read in part; the definitions quoted from Global Affairs Canada come from Tip Sheet 2.1, which was read in full. *Outcome Mapping* was read in its first section only, which holds the quoted sentence.
