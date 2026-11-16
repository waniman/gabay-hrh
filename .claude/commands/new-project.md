---
description: Start a project, e.g. "/new-project concept note: task-shifting cost study for PCHRD"
argument-hint: <type of the first work package>: <project name and funder>
---

Start a new project: $ARGUMENTS

1. **Settings.** If `team.config.yaml` is missing, run `/setup` first.
2. **Work packages and playbooks.** Ask the lead, in one message, which outputs the project must deliver. Each output, or closely tied set of outputs, is a work package (`core/project-and-work-packages.md`). A project with one output has one work package. Match the type of each work package to a file in `playbooks/` (ignore `_template.md`). If none fits a work package, list the available playbooks and offer to draft one with `/new-playbook` before that work package starts. The project can start with the work packages that have a playbook.
3. **Where am I?**
   - If `git remote get-url origin` points to the `template_repo` in `team.config.yaml`, this is the template. The project needs its own repository (step 4).
   - Otherwise this is already a project repository made from the template. Skip to step 6.
4. **List what will be created and wait for "go".** Propose a short repository name in lowercase with hyphens (for example `task-shifting-concept-note`). Then list, in a short table:
   - GitHub: a new private repository `<github_owner>/<name>`, made from the template
   - Google Drive: a project folder (Read me, Memos, Sources, Previous versions) and a tab in the register sheet (only if drive sync is on)
   - Task tracker: a task "Approve the brief" (only if tracker tasks are on)
   - Scheduled task: a daily run at the configured time (only if scheduled runs are on)
   Create nothing until the lead says go. The lead may rename or drop items.
5. **Create the repository.** Try in order, stopping at the first that works:
   - `gh repo create <owner>/<name> --private --template <template_repo>`
   - A GitHub repository-creation tool available in this session
   - If neither works, ask the lead to open the template on GitHub, click **Use this template**, name it `<name>`, choose Private, and tell you when done.
   Then attach and clone the new repository and continue there.
6. **Initialize.** In the project repository: `python3 tools/team.py init --name "<project name>" --type <playbook of the first work package> --wp-title "<title of the first work package>"`. This creates `project/` and WP1. Set the `Lead:` line in `project/state.md` from the settings. Commit "Start project" and push.
7. **Add-ons.** Set up each switched-on add-on by following its `addons/<name>/README.md`, using the items the lead approved in step 4.
8. **Write the project frame** with the lead (`core/project-and-work-packages.md`, `core/results-chain.md`):
   - `project/brief.md`: purpose, audience, funder and call, the funder's terms for results, limits, partners. Ask for the call document to be saved in `project/sources/`.
   - The work packages: title, playbook, output, what each waits for, deadline, and the order of work.
   - `project/results.md`: the impact, two or three outcomes with dates, the outputs and the outcome each serves, the assumptions, and the signals.
   Send the frame to the lead in one memo, issue "Gate: approve the project frame" (`memo new --wp project`). On a project with one work package, the same memo may carry the work package's brief gate.
9. **After the lead approves the frame:** record the answer, save `cp-project-frame-NN`, set `Stage: delivery` in `project/state.md`, and create each further work package with `python3 tools/team.py wp add --title "<title>" --type <playbook> --ref <the frame memo> --waits-for "<WPn and what is needed>"`. Then begin the brief stage of the first work package's playbook. For a revision, ask for the baseline file and the files of comments.
