# Agent Team

A project team of AI agents and people for one project of knowledge work. A project holds one or more work packages, and each delivers an output: a concept note, a proposal, an article, a systematic review. A person leads; agents draft, check and keep the record. Every decision is logged, every stage can be restored, and the decisions that matter reach the lead as memos ready to approve.

Four playbooks: the concept note, for new writing; the revision, for an existing document revised in response to comments; the journal article, from analyzed data to submission and peer review; and the evidence summary, a summary of the best available evidence on one question for a decision-maker. Runs in [Claude Code](https://claude.com/claude-code).

## How it works

- **Roles follow six team capabilities.** The lead holds Direction. Agents cover Delivery (coordinator), Value creation (writer, evidence checker), Learning (blind reviewer), Stewardship (compliance check, process monitor) and Renewal (after-action reviewer). Partners join as people.
- **Work packages.** A project holds one or more work packages, numbered WP1, WP2 and so on. Each follows one playbook and has its own brief, stages, gates, master copy and checkpoints. The project keeps one lead, one register and one health check. The lead approves the project frame, which lists the work packages, before work starts, and approves any work package added or dropped later.
- **Results chain.** One page states the outputs the project delivers, the outcomes it aims to influence, the impact it contributes to, and the assumptions outside its control. Each output names the outcome it serves and its intended user. Observed outcomes are logged with their source, and the project claims contribution, never attribution.
- **Decision register.** One row per decision, by agents and people alike, in `project/register/decisions.csv`. It tells the lead why each choice was made and on what evidence.
- **Checkpoints.** A git tag at the end of every stage of every work package. Any stage of a work package can be restored without changing the others; the register keeps a record of what was rolled back.
- **Escalation.** Six kinds of decision go to the lead: hard to reverse; scope, claim or budget; authorship, ethics or a named stakeholder; open disagreements between agents; anything an agent marks uncertain; and any new analysis or statistical test, before it runs. Each arrives as a decision memo with a recommendation.
- **Comment log.** Every comment received on the work (from the lead, co-authors, reviewers, a funder or a government office) gets a row in `project/register/comments.csv`, with a proposed response. The lead approves each round in one memo, and only approved comments change the text.
- **Lessons at each gate.** At every approval gate, the after-action reviewer looks back over the stages since the last gate and records up to three lessons. Lessons to apply now are approved with the gate and followed for the rest of the project. Lessons for the playbook wait for the final after-action review.
- **Weekly health check.** Once a week, `team.py health` measures pacing with fixed rules: overdue memos, gates waiting, days since each work package's last checkpoint, work packages past their deadline or waiting on another, runs that moved nothing, hard-to-reverse decisions made without a memo, and outcomes whose date has passed with nothing observed. A process monitor that never sees the coordinator's reasoning reads the facts and writes a digest. The digest goes to the lead's tracker; red flags also go to the phone.
- **Independent checks.** Every claim found in an evidence scan is verified, before it enters the text, by a separate call that sees only the claim list. A blind reviewer sees only the draft and the brief. An evidence checker matches every citation and number in the draft.
- **Master copy and sent versions.** Each work package's `state.md` names the one copy the team edits, whether Markdown, a Word file or a Google Doc. When it is outside the repository, each checkpoint saves a DOCX and PDF export. Each version a person sends is stored as an exact copy, and returned files are compared with it to find edits made without Track Changes.
- **Word files.** Word copies are built from Markdown, and redlines made, with the tools in `tools/`. Tracked changes and comments carry the lead's name (`track_changes_author`) and the actual time.
- **Plain files, optional add-ons.** Everything lives in the project repository. Add-ons give you Google Drive folders to read and comment in, copy the register to Google Sheets, turn memos into tracker tasks, alert the lead's phone, and run the team on a schedule.

## Quick start

1. Make this repository a template on GitHub (Settings, then tick **Template repository**).
2. Open it in Claude Code and run `/setup`. Answer five questions; the settings are saved for every new project.
3. Run `/new-project concept note: <project name and funder>`. The coordinator asks which outputs the project must deliver, lists what it will create and waits for your go.
4. Write the project frame with the coordinator and approve it: the project brief, the work packages and the results chain. A project with one output has one work package, and its frame takes about two pages.
5. Let the team work. Answer memos with `/decide`, check progress with `/status`, and approve each work package's brief, outline and final version at the gates.
6. After a person sends an output, tell the coordinator what came back. It logs each observed outcome with its source.

## Using the team in an existing repository

A project that already has its own repository can take the team without starting from the template:

1. Copy `core/`, `playbooks/`, `tools/`, `addons/`, `style/` and `project-template/` into one subfolder, such as `agent-team/`. The tool finds its rules beside itself, so they work from there.
2. In the copied files, prefix paths such as `core/` and `tools/team.py` with the subfolder name, so every reference points to the copy. Copy the agents and commands into the repository's own `.claude/`, with the same prefix.
3. Put `team.config.yaml` at the repository root, and run `python3 agent-team/tools/team.py init --name "<project>" --type <playbook of the first work package>`.
4. Add the coordinator's instructions to the repository's `CLAUDE.md`, and say which rules apply where the two differ.

Master copies anywhere in the repository count as internal, so files in folders such as `outputs/` need no frozen export. `register show --md` writes the register as a readable Markdown page, and `sent add --no-copy` logs a file that must not be committed.

## Commands

| Command | What it does |
| --- | --- |
| `/setup` | Guided setup; writes `team.config.yaml` |
| `/new-project <type>: <name>` | Starts a project in its own private repository |
| `/new-work-package <title and type>` | Adds a work package, after your approval |
| `/continue [work package]` | Runs the next piece of work |
| `/status` | Each work package's stage, what waits on you, last checkpoint, outcomes observed |
| `/decide <memo> <answer>` | Records your answer to a memo or gate |
| `/why <topic>` | Explains a decision from the register |
| `/rollback <checkpoint and reason>` | Returns one work package's work to an earlier checkpoint |
| `/new-playbook <type of work>` | Drafts a playbook for a new type of work, for your approval |

## What is in the repository

```
CLAUDE.md                  rules the coordinator follows every session
team.config.example.yaml   settings, written to team.config.yaml by /setup
.claude/agents/            writer, evidence checker, blind reviewer, compliance check, after-action reviewer, process monitor
.claude/commands/          the commands above
core/                      projects and work packages, results chain, register schema, comment log, escalation threshold,
                           memo template, methods rules, documents and versions, checkpoint and run rules, learning and oversight
playbooks/                 concept-note.md, revision.md, journal-article.md, evidence-summary.md; _template.md for new ones
style/                     voice-technical-writing.md, the writing style for technical products (not journal manuscripts)
addons/                    Google Drive folders and register, tracker task, phone notification, scheduled runs
project-template/          copied to project/ when a project starts; wp-template/ is copied for each work package
tools/team.py              work packages, register, comment log, sent log, outcome log, checkpoints, rollback, memos,
                           health check and status (Python standard library)
tools/test_team.py         tests for team.py: python3 tools/test_team.py
tools/build_docx.py        Word and PDF from Markdown, with numbered citations (needs pandoc; PDF needs LibreOffice)
tools/redline.py           tracked-change redline between two Word files (needs LibreOffice)
```

Each project gets its own private repository made from this template, holding:

```
project/
  state.md                 project stage, order of work, what waits on the lead, lessons in force
  status.md                five lines after each run: run, moved, stopped, waiting on the lead, next
  lessons.md               lessons from each gate review
  brief.md                 the approved project brief
  results.md               the results chain: impact, outcomes, outputs, assumptions, signals
  register/decisions.csv   the decision register, with the work package of each decision
  register/comments.csv    the comment log: every comment received, its response and outcome
  register/sent.csv        the sent log: what left the team, when, to whom, with a checksum
  register/outcomes.csv    the outcome log: each observed outcome, its source and other factors
  escalations/             decision memos
  health/                  weekly health check facts and digests
  reviews/                 checks of the project frame
  sources/                 call documents and files the lead provides
  trace/                   one log per session, for audit
  wp/WP1-<short-name>/     one folder for each work package
    brief.md               the output, the outcome it serves, the intended user and use, limits
    state.md               playbook, stage, status, what it waits for, master copy, open tasks
    work/                  outline, drafts, evidence file, final version
      frozen/              exports of a master copy kept outside the repository, one set per checkpoint
      sent/                exact copies of every version a person sent
    reviews/               evidence checks, blind reviews, compliance checks
```

## Limits

- Agents built on the same model share blind spots. The checks reduce errors; the lead's sign-off is the last check.
- The team never sends, signs, submits, publishes or spends. A person does.
- The team delivers outputs. It can influence outcomes and can only contribute to impact, and it records an outcome only when a person reports a signal with a source. It does not measure impact.
- Playbooks exist for concept notes, revisions, journal articles and evidence summaries. A work package of another type, such as a systematic review or a scoping review, needs a playbook drafted with `/new-playbook` before it starts.
- Disclose AI assistance where a funder or journal requires it. The compliance check reads the policy at the brief stage. Tracked changes and comments drafted by agents carry the lead's name, so the disclosure must cover them.
- Before making a copy of this repository public, remove `team.config.yaml` and any project content.
