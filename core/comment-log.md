# Comment log

Comments received on the work go in `project/register/comments.csv`, one row per comment. They come from the lead, partners, co-authors, a funder, a government office, a journal's reviewers or a validation workshop. The log keeps hundreds of comments traceable without filling the decision register.

## Comment log or decision register?

- **Comment log:** every comment, tracked edit, untracked edit or finding received on the work, and what was done with it.
- **Decision register:** choices that change the scope, the central claim, the method or the plan, and the lead's approval of a round of comment responses. One register row can cover many comments: the row names the memo, and each comment carries the memo id.

For example, co-authors return 34 comments. They become 34 comment rows. The lead approves the proposed responses in one memo, EM-007, and one register row records that approval. Two of the comments would change the title and the aims. Each gets its own option in the memo and its own register row, because it changes the central claim.

## Fields

| Field | Content |
| --- | --- |
| id | RC-001, RC-002 and so on, never reused (set by the tool) |
| work_package | The work package whose output the comment is on, or `project` for a comment on the project brief or the results chain |
| round | The review round, for example `R1`, `DOH-2026-10` or `coauthors-v10.31` |
| source_ref | The reviewer's own number, for example DOH matrix row D-083 or comment C12. It stays in this field, so it never clashes with register ids. |
| reviewer | Who made it: a name, initials, or `untracked (author not recorded)` |
| location | Section, page, line or table, in the version the reviewer saw |
| type | `comment`, `tracked edit`, `untracked edit` or `finding` |
| text | The comment or edit as received |
| tier | `A`, `B`, `C` or `closed` (below) |
| proposed_response | The response the team proposes, in one to three sentences |
| proposed_action | `accept`, `accept in part`, `decline`, `later`, `query` or `none` |
| approved_action | The lead's action. Only `comment approve` sets it. |
| decision_ref | The decided memo (EM-NNN) or approved register row (D-NNN) that holds the lead's answer |
| outcome | What was done and where, or why it was not applied |
| status | `open`, `approved`, `done` or `not applied` |

## Tiers

- **A.** Must be resolved before the next version leaves the team.
- **B.** Needs research before a response can be given.
- **C.** Noted for a later version or edition. The response says so; the text does not change.
- **closed.** No action needed: a duplicate, already done, or a question the text already answers.

## Actions

- **accept**
- **accept in part:** the response says what was not done and why, in one sentence.
- **decline:** the response gives the evidence.
- **later:** next version or edition.
- **query:** a partner must answer first. The response names who.
- **none**

## Steps

1. **Log every comment as it arrives.** For a returned Word file, log every comment and every tracked change. Then compare the file with the copy that was sent (`sent compare`, in `core/documents.md`) and log each passage it finds as an untracked edit. For many comments at once, write a CSV with the field names above and run `python3 tools/team.py comment import --file <csv> --round <round> --wp <WPn>`. A project with one work package needs no `--wp`.
2. **Triage.** Set the tier, proposed action and proposed response of each row: `comment set --id RC-NNN --tier A --proposed-action accept --proposed-response "..."`. Research for tier B follows the playbook's evidence rules. A response that rests on a source needs a verified claim.
3. **Ask the lead.** Send the proposed responses in one memo per round. `comment show --wp <WPn> --round <round> --md` prints the table for the memo. A comment that changes the scope, the central claim, the method, authorship or a named stakeholder gets its own option and recommendation in the memo, and its own register row.
4. **Record the answer.** Run `memo close`, then `comment approve --ref EM-NNN --all-proposed`. Where the lead approved only some rows, use `--ids`; where the lead chose a different action, add `--action`.
5. **Apply only approved comments.** Then mark each one done with its outcome (`comment set --id RC-NNN --status done --outcome "..."`), or not applied with the reason.
6. **Draft the reply.** Write the response matrix or letter to the reviewers from the outcomes. A person sends it.

## Rules

- Change the text only for approved comments. Research may go on before approval.
- Never mark a comment approved for the lead. Approval comes only from a decided memo or an approved register row, and the tool checks this.
- Never delete a row. A comment its author withdraws is set to `not applied`, with the reason.
- `register check` also checks the comment log. Run it before each checkpoint.
