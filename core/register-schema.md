# Decision register

The register is `project/register/decisions.csv`, one row per decision. It is the team's shared record: the lead reads it to explain the work to a reviewer, a funder or an official.

## What counts as a decision

A choice between options that changes the product, the scope, the method or the plan. Examples:

- Choosing a costing perspective, a comparator, a framework or a data source
- Choosing an analysis or a statistical test (`core/methods-rules.md`)
- Dropping, adding or reordering a section
- Accepting or rejecting a major review finding
- Resolving a disagreement between agents
- Moving the master copy, for example from Markdown to a Word file or a Google Doc (`core/documents.md`)
- Adding, dropping or merging a work package, or changing the order of work (`core/project-and-work-packages.md`)
- Changing the impact, an outcome or an assumption in the results chain (`core/results-chain.md`)
- The lead's answer to a memo, and the lead's approval at a gate
- The lead's approval of a round of comment responses: one row for the round

Not decisions: wording, formatting, typo fixes, routine file moves.

Comments received on the work are not register rows. Each one goes in the comment log (`core/comment-log.md`). A comment enters the register only when the choice it raises meets the definition above.

## Fields

| Field | Content |
| --- | --- |
| id | D-001, D-002 and so on, never reused (set by the tool) |
| project | Project name (set by the tool from `state.md`) |
| work_package | WP1, WP2 and so on, or `project` for a decision on the project as a whole (set by the tool from `--wp`) |
| date | Date of the decision |
| stage | Playbook stage in which it was made, or `frame` or `close` for a project decision |
| decision | The question, in one line |
| options | The options considered, separated by semicolons |
| choice | The option taken |
| reason | Why, in one or two sentences |
| evidence | Sources, files or checks behind the choice |
| decided_by | Agent role or person's name |
| reversible | yes or no |
| escalated | Memo id, if the lead decided it |
| status | proposed, approved, reversed by D-NNN, or rolled back |
| checkpoint | Tag of the checkpoint that contains it (set by the tool) |

## How to log

```
python3 tools/team.py register add --wp WP2 --stage outline \
  --decision "Which costing perspective?" \
  --options "Health system; societal" \
  --choice "Health system" \
  --reason "The funder asks for payer costs; societal costs lack local data." \
  --evidence "project/sources/call.pdf p.4; project/wp/WP2-concept-note/work/evidence.md#costs" \
  --by writer --reversible yes
```

- A project with one work package needs no `--wp`. Use `--wp project` for a decision on the project as a whole.
- A decision waiting for the lead is logged with `--status proposed` and `--escalated EM-NNN`. When the lead answers, set it with `register set --id D-NNN --status approved` (or log the lead's different choice as a new row and `register reverse` the old one).
- A partner's decision: the partner logs it, or you log it from their notes with `--by "<their name>"` and ask them to confirm.
- A changed decision gets a new row; then `register reverse --id <old> --by <new>`.
- Run `register check` before every checkpoint. It also checks the comment log, the sent log and the outcome log.

## Answering questions from the register

`python3 tools/team.py register show --search "<words>"`, `--wp <WPn>` or `--stage <stage>`. Answer with the ids, the reason and the evidence. Do not reconstruct reasons that are not in the register.
