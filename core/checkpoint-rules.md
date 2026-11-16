# Checkpoints and rollback

A checkpoint is a git commit with a tag, named `cp-<work package>-<stage>-<number>`, for example `cp-wp2-outline-01`. A checkpoint of the project as a whole is named `cp-project-<stage>-<number>`, for example `cp-project-frame-01`.

## When to save one

- At the end of every playbook stage of a work package
- When the lead is asked to approve the project frame, and at project close (`core/project-and-work-packages.md`)
- Before every approval gate, so the lead approves a fixed version
- Before any large rewrite
- Just before the master copy moves (`core/documents.md`)

## How

1. `python3 tools/team.py register check` and fix any problem it reports. It checks the register, the comment log and the sent log.
2. If the master copy is outside the repository, save its exports first (next section).
3. Update the work package's `state.md`, `project/state.md` and `project/status.md`.
4. `python3 tools/team.py checkpoint --wp <WPn> --stage <stage> --message "<one line>"`

A project with one work package needs no `--wp`. For a checkpoint of the project as a whole, use `--wp project`. Playbooks write checkpoint names without the work package, as `cp-<stage>-NN`; the tool adds it.

The tool writes the new tag into every register row that has no checkpoint yet, whichever work package the row belongs to, commits everything with the message `Checkpoint <tag>`, and tags the commit. Push after each checkpoint with `git push`. Pushing tags is optional: some hosts reject them, so the tool rebuilds checkpoint tags from the commit messages whenever it needs them, including in a fresh or shallow clone.

## When the master copy is outside the repository

A master anywhere inside the repository, in `project/` or in another folder such as `outputs/`, is internal: git keeps its versions, and no export is needed.

A git tag cannot capture a Word file someone else holds, or a Google Doc. When a work package's `state.md` names a master outside the repository:

- Before the checkpoint, export the master as DOCX and PDF into `<wp>/work/frozen/`, named `<stage>-<YYYY-MM-DD>.docx` and `.pdf` (add `-2`, `-3` for a second export on the same day).
- For a Google Doc, export with suggestions and comments included. If the lead asks for a clean copy as well, save both and say which is which in the file names.
- The checkpoint tool refuses to save a checkpoint of that work package if nothing in its `work/frozen/` changed since its last checkpoint. If the master did not change, pass `--no-export "<reason>"`; the reason goes into the commit message.

## Rollback

Only on the lead's instruction, or as the outcome of a memo the lead approved.

```
python3 tools/team.py rollback --to cp-wp2-outline-01 --reason "<why>" --by "<lead's name>"
```

- A rollback acts on one work package, the one the checkpoint belongs to. Its work files in `<wp>/work/` return to the checkpoint, in a new commit. History is never rewritten.
- The other work packages, the project brief and the results chain stay as they are. To return a work package to the state it had at a project checkpoint or at another work package's checkpoint, add `--wp <WPn>`.
- Frozen exports (`<wp>/work/frozen/`) and sent copies (`<wp>/work/sent/`) are records. A rollback keeps them as they are.
- The register keeps every row. Decisions of that work package made after the checkpoint are marked rolled back. Decisions of other work packages are not changed.
- If another work package has used a file that the rollback changes, such as a verified finding, send the lead a memo before the rollback.
- The rollback itself is logged as a decision.
- The register as it stood at any checkpoint can be read with `git show <tag>:project/register/decisions.csv`.
- If the master is outside the repository, the rollback cannot change it. After the lead's go, the holder saves the current master as a frozen export, then restores the master from the frozen export of that checkpoint.

After a rollback, update the work package's `state.md` to the stage the checkpoint belongs to, then save a new checkpoint for that stage.
