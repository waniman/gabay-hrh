# Documents and versions

## The master copy

The master copy is the one version of a work package's output that the team edits. Every other copy is an export, a reading copy or a record. Each work package has its own master copy. In this file, `<wp>/` stands for the work package's folder, for example `project/wp/WP2-concept-note/`.

- The work package's `state.md` names the master on its `Master copy:` line, with who holds it. For example:
  - `Master copy: project/wp/WP2-concept-note/work/draft.md (held by the coordinator in this repository)`
  - `Master copy: Google Doc <link> (held by the coordinator's cloud session)`
  - `Master copy: project/wp/WP1-profile/work/master/profile_v5.docx (held by the coordinator in this repository)`
- A path inside the repository, in `project/` or in another folder, is internal. Any other value, such as a Google Doc link, is outside it, and the checkpoint tool then asks for exports (`core/checkpoint-rules.md`).
- The playbook says where the master lives at each stage, and when it moves.
- Only the holder edits the master. Another session or person proposes changes in a separate file, or as suggestions, and the holder merges them. In one project, two sessions produced two versions of the same supplement; this rule prevents that.
- When the master moves, save a checkpoint just before the move. Then update the `Master copy:` line and note the move in the trace.

## When the master is a Word file or a Google Doc

Funders, journals and government offices usually receive Word files, and the lead or partners may edit in Google Docs. Once the master is one of these:

1. **Read before writing.** Read the current text, comments and suggestions before every batch of edits. Never rely on an earlier read.
2. **Export before each batch.** Save a DOCX export to `<wp>/work/frozen/`. At checkpoints, save a PDF as well.
3. **Log edits by others.** If the text changed between reads, record what changed in the trace. Leave it as found unless the lead says otherwise.
4. **Track every edit.** Each edit is a tracked change or a suggestion, with a margin comment naming the comment-log id and the source, for example `[RC-083] CHED CMO No. 17, s. 2025`.
5. **Preserve the document.** Keep its styles, numbering, tables, figures, comments and tracked changes. Never accept or reject someone else's changes. Never rebuild an existing Word file from extracted text, and never convert it to Markdown and back.
6. **Check each batch.** Export again and confirm that each expected change is there and that no other paragraph changed. The count of tracked changes should match the log.

The repository keeps the logs, the frozen exports and the sent copies.

## Who is named as author of tracked changes and comments

- Every tracked change and comment the team writes into a Word file is attributed to `track_changes_author` in `team.config.yaml`, which is the lead. Never write one under another name or as "Claude".
- Use the actual time each change or comment is made. Never alter or randomize timestamps.
- Google Docs names the connected Google account as the author of suggestions and comments. Before editing a Google Doc, confirm that the Docs connector uses the lead's account. If it does not, tell the lead before editing.
- The compliance check confirms that the AI-use statement covers edits drafted by AI and recorded under the lead's name.

## Building and comparing Word files

- **Build from Markdown:** `python3 tools/build_docx.py --source <md> --out <docx>`. It numbers citations from a references CSV of verified entries (`--refs`), and adds journal formatting with `--font "Times New Roman" --size 12 --double-spacing --line-numbers --page-numbers`. It writes a PDF with `--pdf`, and saves the exact text rendered next to the output for checks. It needs pandoc; the PDF needs LibreOffice.
- **Make a redline:** `python3 tools/redline.py <old.docx> <new.docx> <out.docx>`. It uses LibreOffice's Compare Document, so formatting is kept. New tracked changes carry `track_changes_author` and the actual time; authors already in the new file are kept. It can also turn a clean, edited copy of an existing Word file into tracked changes against the baseline.
- Name each build by its version, following the convention in the brief (for example `<name>_v11.07.docx`).

## Sent versions

A person sends; the team records what was sent.

1. **Record it.** After a person sends a version, run:
   `python3 tools/team.py sent add --wp <WPn> --file <the exact file sent> --to "<recipients>" --purpose "<why>" --by "<who sent it>" --version <version>`
   The tool stores an exact copy in `<wp>/work/sent/`, with its SHA-256 checksum. Record the file that was sent, not a rebuild. If it is unclear which file left, ask the person who sent it. Never infer it.
   If the file must not be committed (for example, it holds identifiable interview data), add `--no-copy "<reason>"`. The tool then logs the checksum and recipients without storing a copy, and `sent compare` cannot be used for that version.
2. **Compare what comes back.** When a file returns, compare it with the copy that was sent:
   `python3 tools/team.py sent compare --id S-NNN --file <returned file> --out <wp>/reviews/returned-S-NNN.md`
   The report counts tracked changes and comments by author, and lists every passage changed without Track Changes. Rejecting all tracked changes does not reveal those edits; only the comparison does. In one round, eight co-author edits were found this way.
3. **Log everything.** Log every comment, tracked change and untracked edit in the comment log (`core/comment-log.md`).
4. Always compare a returned file with the copy that was sent to that person, never with a later build.

`register check` confirms that each sent copy still matches its checksum.
