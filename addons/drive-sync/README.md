# Add-on: Google Drive folders and register

Gives the lead and partners a place in Google Drive to read, comment and drop files, and copies the decision register to a Google Sheet. GitHub stays the record: Drive holds reading copies.

**Needs:** Google Drive, Google Docs and Google Sheets connectors in the session.

## Layout

```
Agent Team/                          (addons.drive_sync.folder_id; shared with share_with)
  Agent Team Register                (sheet: one tab per project, plus "All projects")
  <project repository name>/         (one folder per project)
    Read me                          (what is here, how to comment, where the record is)
    Project brief, Results chain     (Google Docs; reading copies)
    WP1 <title>/                     (one subfolder per work package)
      Brief, Draft, Final            (Google Docs; reading copies)
    Memos/                           (one Doc per open memo; a summary Doc for decided ones)
    Sources/                         (inbox: files the lead or partners want the team to use)
    Previous versions/               (replaced copies, kept with their comments)
```

The ids of the project's folders and documents are kept in `project/drive.json`.

## First use (template level)

1. If `addons.drive_sync.folder_id` is empty, create the **Agent Team** folder, share it with `share_with`, and save its id in `team.config.yaml`.
2. If `sheet_id` is empty, create the **Agent Team Register** sheet inside it, with a **Read me** tab and an **All projects** tab, and save its id.

## At project start

1. Create the project folder with **Memos**, **Sources** and **Previous versions** inside it, and a **Read me** Doc.
2. Create one subfolder for each work package, named `<WPn> <title>`. Create the subfolder of a later work package when `wp add` creates it (`core/project-and-work-packages.md`).
3. Add a tab named after the repository to the register sheet, and add it to the **All projects** formula, for example `=QUERY({'proj-a'!A2:O; 'proj-b'!A2:O}, "select * where Col1 is not null", 0)`. The register has 15 columns, with the work package in the third.
4. Write every id to `project/drive.json`, with the work package each folder and document belongs to.

## Which documents to mirror

Mirror what people read and comment on at a gate, not working files:

- the project brief and the results chain, at the project frame gate (project folder)
- each work package's brief, at its brief gate (its subfolder)
- the outline, at the outline gate, when the playbook has one
- the draft, after the check stage
- the final version, at sign-off
- each open memo, when it is sent; once decided, fold it into the summary Doc

The evidence file, the register CSV, reviews and the trace stay in the repository. The register reaches Drive through the sheet.

Create each Doc from the Markdown file (`contentMimeType: text/markdown`), so headings and lists keep their format. Put one line at the top: "Reading copy. The record is <path> in the GitHub repo <owner>/<repo>. Edits here are overwritten; comments are picked up at the next run."

## When the master copy is a Google Doc

A playbook may move the master copy into a Google Doc, for example when the lead and partners review in Google Docs (`core/documents.md`). From then on, that Doc is not a reading copy:

- Never overwrite or replace it, and do not put the "Reading copy" line at its top.
- Before every batch of edits, read its current text, comments and suggestions. Log in the trace any change made by others since the last read.
- Make edits as suggestions, each with a comment naming the comment-log id and the source.
- Google Docs names the connected Google account as the author of suggestions and comments. Confirm that the Docs connector uses the lead's account (`track_changes_author`) before editing; if it does not, tell the lead first.
- At each checkpoint, export it as DOCX and PDF into the work package's `work/frozen/` folder (`core/checkpoint-rules.md`).
- Record its link in `project/drive.json` and on the `Master copy:` line of the work package's `state.md`.

## Replacing a document with a newer version

1. Read its comments first (see below).
2. Move the old Doc into **Previous versions**, and add the date to its title.
3. Create the new Doc in its place and update `project/drive.json`.

This keeps formatting, keeps every comment with the version it was made on, and keeps the folder tidy.

## At the start of every run

1. **Comments.** Read each mirrored Doc with comments included. For each new comment, treat it as the lead's or partner's input on the work package the Doc belongs to: answer in the thread, log any decision in the register, and turn anything beyond the threshold into a memo. Resolve the thread only when the commenter asked for a change that is now made.
2. **Sources inbox.** Copy any new file in **Sources** into `project/sources/`, note it in the trace, and leave the original in Drive.

## After each checkpoint

1. Clear the project's tab in the register sheet and write the full `decisions.csv`, header included.
2. Mirror any document this stage produced for a gate.
3. Note the sync in the trace.

## If it fails

Leave the files as they are, note the failure and its message in the trace and in `status.md`, and try again after the next checkpoint. Never retry in a loop.
