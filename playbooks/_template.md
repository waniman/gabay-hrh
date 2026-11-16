# Playbook: <type of work>

One sentence on what this type of work is and what it produces.

This playbook runs one work package. `<wp>/` stands for that work package's folder, for example `project/wp/WP2-<short-name>/` (`core/project-and-work-packages.md`). Checkpoint names below omit the work package; the tool adds it.

## Output and intended use

The output or outputs this playbook produces, who usually uses them, and the kind of outcome they usually serve (`core/results-chain.md`).

## Roles

Which of the default agent roles take part, any role added (for example, a second screener), and which roles are people.

## Evidence to check against

What counts as the outside evidence for this kind of work: sources, rules documents, datasets, templates, budgets.

## Master copy

Where the master copy lives at each stage (Markdown in `<wp>/work/`, a Word file, or a Google Doc), and the stage at which it moves, if it does (`core/documents.md`).

## Stages

For each stage:

### N. Stage name

- **Who:** roles involved
- **Do:** the work, and the files it produces, in `<wp>/work/` or `<wp>/reviews/`
- **Done when:** the condition that ends the stage
- **Gate:** only if the lead must approve before the next stage
- **Checkpoint:** `cp-<stage>-NN`

## Gates

| Gate | Stage | What the lead approves |
| --- | --- | --- |

The first gate approves the work package brief (`<wp>/brief.md`): the output, the outcome it serves, and the intended user and use. The last gate approves the version a person will send; its memo names the outcome the output serves.

At each gate, before the gate memo is sent, the after-action reviewer runs in gate mode on the stages since the last gate. Its lessons are listed in the gate memo, and the lead approves the apply-now lessons with the gate (`core/learning-and-oversight.md`). Start the issue of each gate memo with "Gate:".

## Differences from the core

Any change to the escalation threshold, timing or checks for this type of work, with the reason. Keep this short; most playbooks need none.
