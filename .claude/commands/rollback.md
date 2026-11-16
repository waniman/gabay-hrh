---
description: Return one work package's work to an earlier checkpoint, e.g. "/rollback WP2 to the approved outline"
argument-hint: <which checkpoint, and why>
---

Request: $ARGUMENTS

1. List the checkpoints (`git tag --list "cp-*"`) with the date and message of each, and identify the work package and the checkpoint the lead means. If more than one could fit, ask.
2. Tell the lead in two or three lines what will happen: which work package's files return to that state, which of its register decisions will be marked rolled back (`register show --wp <WPn>` for rows after that checkpoint), and whether another work package has used a file that will change. The other work packages stay as they are. Ask for "go" and the reason, if not given.
3. On "go": save any unsaved work as a checkpoint first, then run
   `python3 tools/team.py rollback --to <tag> --reason "<reason>" --by "<lead>"`.
4. Set the work package's `state.md` to the stage of that checkpoint, save a new checkpoint for it, and push.
