#!/usr/bin/env python3
"""Agent Team helper: work packages, register, comment log, sent log, outcome log, checkpoints, rollback, memos, health check and status.

Standard library only. Run from anywhere inside a project repository:

    python3 tools/team.py <command> [options]

Commands
    init        Create project/ from project-template/, with its first work package (WP1)
    wp          add | list                                    (work packages: core/project-and-work-packages.md)
    register    add | set | reverse | check | show
    comment     add | import | set | approve | show | check   (comments received on the work)
    sent        add | list | compare                         (versions that left the team)
    outcome     add | show                                    (observed outcomes: core/results-chain.md)
    checkpoint  Save a checkpoint (commit + tag) at the end of a stage or before a gate
    rollback    Restore one work package's work/ folder to an earlier checkpoint
    memo        new | list | close
    health      Weekly health check facts for the process monitor (--due: is a check due today?)
    status      Print the project state, work packages, open memos, comments, last checkpoint and last health check

Commands that act on one work package take --wp WPn. A project with one work package needs no --wp.
Use --wp project for a decision, comment, memo or checkpoint that belongs to the project as a whole.
"""

import argparse
import csv
import datetime as dt
import difflib
import hashlib
import re
import shutil
import subprocess
import sys
import zipfile
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

FIELDS = [
    "id", "project", "work_package", "date", "stage", "decision", "options", "choice", "reason",
    "evidence", "decided_by", "reversible", "escalated", "status", "checkpoint",
]
STATUSES = {"proposed", "approved", "rolled back"}  # plus "reversed by D-NNN"
TAG_RE = re.compile(r"^cp-[a-z0-9-]+-\d{2}$")

COMMENT_FIELDS = [
    "id", "work_package", "round", "source_ref", "reviewer", "location", "type", "text", "tier",
    "proposed_response", "proposed_action", "approved_action", "decision_ref", "outcome", "status",
]
TIERS = {"A", "B", "C", "closed"}
ACTIONS = {"accept", "accept in part", "decline", "later", "query", "none"}
COMMENT_STATUSES = {"open", "approved", "done", "not applied"}

SENT_FIELDS = ["id", "work_package", "date", "file", "version", "recipients", "purpose", "sent_by", "sha256", "note"]

OUTCOME_FIELDS = ["id", "date", "outcome", "observed", "source", "reported_by", "other_factors"]

WP_STATUSES = ("planned", "active", "waiting", "signed off", "dropped")


# ---------- paths and git ----------

def repo_root() -> Path:
    try:
        out = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True,
                             text=True, check=True).stdout.strip()
        return Path(out)
    except subprocess.CalledProcessError:
        sys.exit("Not inside a git repository.")


ROOT = repo_root()
# The agent-team files (core/, playbooks/, project-template/) sit beside tools/. In the template
# repository this is the repository root; in another repository it can be a subfolder, such as agent-team/.
TEAM = Path(__file__).resolve().parent.parent
PROJECT = ROOT / "project"
REGISTER = PROJECT / "register" / "decisions.csv"
COMMENTS = PROJECT / "register" / "comments.csv"
SENT = PROJECT / "register" / "sent.csv"
ESCALATIONS = PROJECT / "escalations"
OUTCOMES = PROJECT / "register" / "outcomes.csv"
STATE = PROJECT / "state.md"
RESULTS = PROJECT / "results.md"
WP_ROOT = PROJECT / "wp"


def git(*args, check=True) -> str:
    res = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    if check and res.returncode != 0:
        sys.exit(f"git {' '.join(args)} failed:\n{res.stderr.strip()}")
    return res.stdout.strip()


def need_project():
    if not REGISTER.exists():
        sys.exit("No project here yet. Run: python3 tools/team.py init --name ... --type ...")


def today() -> str:
    return dt.date.today().isoformat()


def project_name() -> str:
    if STATE.exists():
        m = re.search(r"^Project:\s*(.+)$", STATE.read_text(encoding="utf-8"), re.M)
        if m:
            return m.group(1).strip()
    return ROOT.name


def file_field(path: Path, name: str) -> str:
    """The value of a 'Name: value' line in a state file. Empty if the file or the line is missing."""
    if path.exists():
        m = re.search(rf"^{re.escape(name)}:[ \t]*(.*)$", path.read_text(encoding="utf-8"), re.M)
        if m:
            return m.group(1).strip()
    return ""


def state_field(name: str) -> str:
    """A line of the project's state.md."""
    return file_field(STATE, name)


# ---------- work packages ----------
# A project holds one or more work packages, each in project/wp/WP<n>-<short-name>/ with its own
# brief.md, state.md, work/ and reviews/. Rules: core/project-and-work-packages.md.

def wp_folders() -> dict:
    """{'WP1': folder, ...} in the order of work: the 'Order:' line of project/state.md, then by number."""
    found = {}
    if WP_ROOT.exists():
        for folder in WP_ROOT.iterdir():
            m = re.match(r"^(WP\d+)(?:-|$)", folder.name)
            if folder.is_dir() and m:
                found[m.group(1)] = folder
    order = [w for w in re.findall(r"WP\d+", state_field("Order")) if w in found]
    order += [w for w in sorted(found, key=lambda w: int(w[2:])) if w not in order]
    return {w: found[w] for w in order}


def resolve_wp(value: str, allow_project: bool = False) -> str:
    """The work package a command applies to: 'WPn', or 'project' where that is allowed.

    A project with one work package needs no --wp. The folder name (WP2-concept-note) is accepted too.
    """
    wps = wp_folders()
    value = (value or "").strip()
    if value.lower() == "project":
        if allow_project:
            return "project"
        sys.exit("This command acts on one work package. Name it with --wp WPn.")
    if value:
        wp = value.upper().split("-")[0]
        if wp not in wps:
            sys.exit(f"No work package {value}. Available: {', '.join(wps) or 'none'}")
        return wp
    if not wps:
        sys.exit("This project has no work package yet. Run: python3 tools/team.py wp add ...")
    if len(wps) == 1:
        return next(iter(wps))
    sys.exit("This project has several work packages. Add --wp with one of: " + ", ".join(wps)
             + (", or project" if allow_project else ""))


def wp_dir(wp: str) -> Path:
    return wp_folders()[wp]


def wp_work(wp: str) -> Path:
    return wp_dir(wp) / "work"


def wp_frozen(wp: str) -> Path:
    return wp_work(wp) / "frozen"


def wp_sent_dir(wp: str) -> Path:
    return wp_work(wp) / "sent"


def wp_field(wp: str, name: str) -> str:
    """A line of the work package's state.md."""
    return file_field(wp_dir(wp) / "state.md", name)


def wp_status(wp: str) -> str:
    """planned, active, waiting, signed off or dropped, from the 'Status:' line. Active if not stated."""
    value = wp_field(wp, "Status").lower()
    return next((st for st in WP_STATUSES if value.startswith(st)), "active")


def wp_deadline(wp: str):
    """The date on the '- Deadline:' line of the work package's brief, or None."""
    brief = wp_dir(wp) / "brief.md"
    line = re.search(r"^- Deadline:\s*(.*)$", brief.read_text(encoding="utf-8"), re.M) if brief.exists() else None
    return parse_date(line.group(1)) if line else None


def tag_wp(tag: str) -> str:
    """The work package a checkpoint tag belongs to ('WP2' for cp-wp2-outline-01), or '' for a project checkpoint."""
    m = re.match(r"^cp-(wp\d+)-", tag)
    return m.group(1).upper() if m else ""


def check_wp_value(value: str, wps) -> str:
    """'' if the work_package value of a log row is valid, else the problem."""
    if value == "project" or value in wps:
        return ""
    return f"work_package '{value}' is not a work package of this project or 'project'"


def master_copy(wp: str) -> str:
    """The 'Master copy:' line of the work package's state.md, without backticks. Empty if the line is missing."""
    return wp_field(wp, "Master copy").replace("`", "").strip()


def master_path(wp: str) -> str:
    """The path part of the 'Master copy:' line: the first `quoted` part, or the line without a closing note in brackets."""
    line = wp_field(wp, "Master copy")
    quoted = re.search(r"`([^`]+)`", line)
    if quoted:
        return quoted.group(1).strip()
    return re.sub(r"\s+\([^()]*\)\s*$", "", line).strip()


def master_is_external(wp: str) -> bool:
    """True when the work package's master copy lives outside the repository (a Word file elsewhere or a Google Doc).

    A master anywhere inside the repository is internal: git keeps its versions, so no frozen export is needed.
    """
    value = master_path(wp)
    if not value or value.startswith("project/"):
        return False
    try:
        return not (ROOT / value).resolve().is_relative_to(ROOT.resolve()) or not (ROOT / value).exists()
    except (OSError, ValueError):
        return True


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_table(path: Path, fields):
    """Read a CSV log with a fixed header. A missing file is created with its header."""
    need_project()
    if not path.exists():
        write_table(path, fields, [])
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != fields:
            sys.exit(f"{path.relative_to(ROOT)}: header does not match.\nExpected: {fields}\nFound:    {reader.fieldnames}")
        return list(reader)


def write_table(path: Path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})


def next_prefixed_id(rows, prefix: str) -> str:
    nums = [int(r["id"][len(prefix):]) for r in rows if re.fullmatch(rf"{prefix}\d{{3,}}", r["id"])]
    return f"{prefix}{(max(nums) + 1) if nums else 1:03d}"


# ---------- register ----------

def read_rows():
    need_project()
    with REGISTER.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != FIELDS:
            sys.exit(f"Register header does not match the schema.\nExpected: {FIELDS}\nFound:    {reader.fieldnames}")
        return list(reader)


def write_rows(rows):
    with REGISTER.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in FIELDS})


def next_id(rows) -> str:
    nums = [int(r["id"][2:]) for r in rows if re.fullmatch(r"D-\d{3,}", r["id"])]
    return f"D-{(max(nums) + 1) if nums else 1:03d}"


def find_row(rows, rid):
    for r in rows:
        if r["id"] == rid:
            return r
    sys.exit(f"No decision with id {rid}.")


def cmd_register_add(a):
    rows = read_rows()
    if a.reversible not in ("yes", "no"):
        sys.exit("--reversible must be yes or no.")
    if a.status not in ("proposed", "approved"):
        sys.exit("--status must be proposed or approved for a new decision.")
    rid = next_id(rows)
    rows.append({
        "id": rid, "project": project_name(), "work_package": resolve_wp(a.wp, allow_project=True),
        "date": a.date or today(), "stage": a.stage,
        "decision": a.decision, "options": a.options, "choice": a.choice, "reason": a.reason,
        "evidence": a.evidence or "", "decided_by": a.by, "reversible": a.reversible,
        "escalated": a.escalated or "", "status": a.status, "checkpoint": "",
    })
    write_rows(rows)
    print(rid)


def cmd_register_set(a):
    rows = read_rows()
    r = find_row(rows, a.id)
    if a.status:
        if a.status not in STATUSES:
            sys.exit(f"--status must be one of {sorted(STATUSES)}; use 'register reverse' for reversals.")
        r["status"] = a.status
    if a.escalated:
        r["escalated"] = a.escalated
    if a.choice:
        r["choice"] = a.choice
    if a.reason:
        r["reason"] = a.reason
    write_rows(rows)
    print(f"{a.id} updated")


def cmd_register_reverse(a):
    rows = read_rows()
    old = find_row(rows, a.id)
    new = find_row(rows, a.by)
    if old is new:
        sys.exit("A decision cannot reverse itself.")
    old["status"] = f"reversed by {a.by}"
    write_rows(rows)
    print(f"{a.id} marked reversed by {a.by}")


def restore_checkpoint_tags():
    """Recreate local checkpoint tags from commit messages ("Checkpoint cp-<stage>-NN ...").

    Some git hosts and proxies reject tag pushes, and fresh clones may be shallow. The commit
    message is the durable record of a checkpoint; tags are a local convenience rebuilt from it.
    """
    if git("rev-parse", "--is-shallow-repository", check=False) == "true":
        branch = git("rev-parse", "--abbrev-ref", "HEAD", check=False) or "main"
        git("fetch", "-q", "--depth=1000", "origin", branch, check=False)
    log = git("log", "--format=%H %s", check=False)
    existing = set(git("tag", "--list", "cp-*", check=False).splitlines())
    for line in log.splitlines():
        sha, _, subject = line.partition(" ")
        m = re.match(r"^Checkpoint (cp-[a-z0-9-]+-\d{2})\b", subject)
        if m and m.group(1) not in existing:
            git("tag", m.group(1), sha, check=False)
            existing.add(m.group(1))


def tags_in_order():
    """Checkpoint tags in the order their commits appear in history (oldest first).

    Ordering by tag date is unreliable when two checkpoints are saved within the same second.
    """
    restore_checkpoint_tags()
    refs = git("for-each-ref", "refs/tags/cp-*", "--format=%(*objectname) %(objectname) %(refname:short)", check=False)
    if not refs:
        return []
    history = git("rev-list", "--reverse", "HEAD", check=False).splitlines()
    pos = {sha: i for i, sha in enumerate(history)}
    tagged = []
    for line in refs.splitlines():
        peeled, obj, name = line.split(" ", 2) if line.count(" ") >= 2 else ("", *line.split(" ", 1))
        sha = peeled or obj
        tagged.append((pos.get(sha, len(history)), name))
    return [name for _, name in sorted(tagged)]


def register_problems():
    """Problems in the register, comment log and sent log, with their row counts."""
    rows = read_rows()
    problems = []
    seen = set()
    tags = set(tags_in_order())
    wps = wp_folders()
    for i, r in enumerate(rows, start=2):
        rid = r["id"]
        if not re.fullmatch(r"D-\d{3,}", rid):
            problems.append(f"line {i}: bad id '{rid}'")
        if rid in seen:
            problems.append(f"line {i}: duplicate id {rid}")
        seen.add(rid)
        for k in ("date", "stage", "decision", "choice", "reason", "decided_by", "reversible", "status"):
            if not r[k].strip():
                problems.append(f"{rid}: '{k}' is empty")
        if check_wp_value(r["work_package"], wps):
            problems.append(f"{rid}: {check_wp_value(r['work_package'], wps)}")
        if r["reversible"] and r["reversible"] not in ("yes", "no"):
            problems.append(f"{rid}: reversible must be yes or no")
        st = r["status"]
        if st not in STATUSES and not re.fullmatch(r"reversed by D-\d{3,}", st):
            problems.append(f"{rid}: unknown status '{st}'")
        if r["checkpoint"] and r["checkpoint"] not in tags:
            problems.append(f"{rid}: checkpoint '{r['checkpoint']}' is not a tag in this repository")
        if r["escalated"] and not (ESCALATIONS / f"{r['escalated']}.md").exists():
            problems.append(f"{rid}: memo {r['escalated']} not found in escalations/")
    comments = read_table(COMMENTS, COMMENT_FIELDS) if COMMENTS.exists() else []
    sent = read_table(SENT, SENT_FIELDS) if SENT.exists() else []
    outcomes = read_table(OUTCOMES, OUTCOME_FIELDS) if OUTCOMES.exists() else []
    problems += comment_problems(comments, rows)
    problems += sent_problems(sent)
    problems += outcome_problems(outcomes)
    return problems, rows, comments, sent


def cmd_register_check(a):
    problems, rows, comments, sent = register_problems()
    if problems:
        print("Register problems:")
        for p in problems:
            print(" -", p)
        sys.exit(1)
    outcomes = read_table(OUTCOMES, OUTCOME_FIELDS) if OUTCOMES.exists() else []
    print(f"Register OK: {len(rows)} decisions, {len(comments)} comments, {len(sent)} sent versions, "
          f"{len(outcomes)} observed outcomes")


def register_markdown(rows) -> str:
    """The register as a readable Markdown page, newest first, for a file such as DECISIONS.md."""
    def cell(v):
        return (v or "").replace("|", "/").replace("\n", " ").strip()
    lines = [
        "# Decisions",
        "",
        f"Generated from `project/register/decisions.csv` on {today()} by `team.py register show --md`. "
        "Do not edit this file by hand: decisions are logged with `team.py register add`, and this file is regenerated.",
        "",
        "| Id | WP | Date | Decision | Choice | Decided by | Evidence | Status | Memo |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for r in reversed(rows):
        lines.append("| " + " | ".join(cell(r[k]) for k in
                     ("id", "work_package", "date", "decision", "choice", "decided_by", "evidence", "status",
                      "escalated")) + " |")
    return "\n".join(lines) + "\n"


def cmd_register_show(a):
    rows = read_rows()
    if a.md:
        print(register_markdown(rows), end="")
        return
    if a.wp:
        wp = resolve_wp(a.wp, allow_project=True)
        rows = [r for r in rows if r["work_package"] == wp]
    if a.stage:
        rows = [r for r in rows if r["stage"] == a.stage]
    if a.search:
        q = a.search.lower()
        rows = [r for r in rows if any(q in (r[k] or "").lower() for k in FIELDS)]
    if not rows:
        print("No matching decisions.")
        return
    for r in rows:
        print(f"{r['id']}  {r['work_package']}  [{r['stage']}]  {r['date']}  {r['status']}  "
              f"{r['checkpoint'] or 'not yet checkpointed'}")
        print(f"  Decision: {r['decision']}")
        print(f"  Options:  {r['options']}")
        print(f"  Choice:   {r['choice']}")
        print(f"  Reason:   {r['reason']}")
        if r["evidence"]:
            print(f"  Evidence: {r['evidence']}")
        print(f"  By: {r['decided_by']}  Reversible: {r['reversible']}" + (f"  Memo: {r['escalated']}" if r["escalated"] else ""))
        print()


# ---------- comment log ----------
# One row per comment received on the work: from the lead, partners, co-authors, reviewers,
# a funder or a validation workshop. Rules: core/comment-log.md.

def read_comments():
    return read_table(COMMENTS, COMMENT_FIELDS)


def write_comments(rows):
    write_table(COMMENTS, COMMENT_FIELDS, rows)


def check_choice(value, allowed, name):
    if value and value not in allowed:
        sys.exit(f"{name} must be one of: {', '.join(sorted(allowed))}")


def ref_is_lead_decision(ref: str, decisions) -> str:
    """Return '' if ref is a decided memo or an approved register row, else the problem."""
    if re.fullmatch(r"EM-\d{3,}", ref):
        path = ESCALATIONS / f"{ref}.md"
        if not path.exists():
            return f"memo {ref} not found"
        if memo_status(path) != "decided":
            return f"memo {ref} is not decided yet"
        return ""
    if re.fullmatch(r"D-\d{3,}", ref):
        row = next((r for r in decisions if r["id"] == ref), None)
        if row is None:
            return f"decision {ref} not found"
        if row["status"] != "approved":
            return f"decision {ref} is '{row['status']}', not approved"
        return ""
    return f"'{ref}' is not a memo (EM-NNN) or a decision (D-NNN)"


def comment_ids(a):
    ids = [x.strip() for x in (a.ids or "").split(",") if x.strip()]
    if getattr(a, "id", None):
        ids.append(a.id)
    return ids


def cmd_comment_add(a):
    rows = read_comments()
    check_choice(a.tier, TIERS, "--tier")
    check_choice(a.proposed_action, ACTIONS, "--proposed-action")
    cid = next_prefixed_id(rows, "RC-")
    rows.append({
        "id": cid, "work_package": resolve_wp(a.wp, allow_project=True),
        "round": a.round, "source_ref": a.source_ref, "reviewer": a.reviewer,
        "location": a.location, "type": a.type, "text": a.text, "tier": a.tier,
        "proposed_response": a.proposed_response, "proposed_action": a.proposed_action,
        "approved_action": "", "decision_ref": "", "outcome": "", "status": "open",
    })
    write_comments(rows)
    print(cid)


def cmd_comment_import(a):
    rows = read_comments()
    allowed = [f for f in COMMENT_FIELDS if f not in ("id", "approved_action", "decision_ref", "outcome", "status")]
    with open(a.file, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        unknown = [c for c in (reader.fieldnames or []) if c not in allowed]
        if unknown:
            sys.exit(f"Unknown columns {unknown}. Allowed: {allowed}")
        incoming = list(reader)
    added = []
    wps = wp_folders()
    default_wp = resolve_wp(a.wp, allow_project=True) if a.wp or len(wps) == 1 else ""
    for i, src in enumerate(incoming, start=2):
        if not (src.get("text") or "").strip():
            sys.exit(f"{a.file} line {i}: 'text' is empty")
        row_wp = (src.get("work_package") or "").strip() or default_wp
        if not row_wp:
            sys.exit(f"{a.file} line {i}: no work package. Add --wp, or a work_package column.")
        if check_wp_value(row_wp, wps):
            sys.exit(f"{a.file} line {i}: {check_wp_value(row_wp, wps)}")
        check_choice(src.get("tier", ""), TIERS, f"line {i}: tier")
        check_choice(src.get("proposed_action", ""), ACTIONS, f"line {i}: proposed_action")
        row = {k: (src.get(k) or "").strip() for k in allowed}
        row["work_package"] = row_wp
        row["round"] = row["round"] or a.round
        row["reviewer"] = row["reviewer"] or a.reviewer
        row.update({"id": next_prefixed_id(rows, "RC-"), "approved_action": "", "decision_ref": "",
                    "outcome": "", "status": "open"})
        rows.append(row)
        added.append(row["id"])
    write_comments(rows)
    print(f"Imported {len(added)} comments" + (f": {added[0]} to {added[-1]}" if added else ""))


def cmd_comment_set(a):
    rows = read_comments()
    ids = comment_ids(a)
    if not ids:
        sys.exit("Name the comment(s) with --id or --ids.")
    check_choice(a.tier, TIERS, "--tier")
    check_choice(a.proposed_action, ACTIONS, "--proposed-action")
    if a.status:
        check_choice(a.status, {"open", "done", "not applied"}, "--status (approval goes through 'comment approve')")
    for cid in ids:
        r = next((x for x in rows if x["id"] == cid), None)
        if r is None:
            sys.exit(f"No comment {cid}.")
        if a.proposed_action and r["status"] in ("approved", "done") and a.proposed_action != r["approved_action"]:
            sys.exit(f"{cid} is already {r['status']} as '{r['approved_action']}'. A different action needs a new lead decision.")
        for field in ("tier", "location", "source_ref", "proposed_response", "proposed_action", "outcome"):
            value = getattr(a, field)
            if value:
                r[field] = value
        if a.status == "done":
            if not r["approved_action"]:
                sys.exit(f"{cid}: not approved yet. Run 'comment approve' with the lead's memo or decision first.")
            if not r["outcome"]:
                sys.exit(f"{cid}: give --outcome (what was done, and where).")
        if a.status == "not applied" and not r["outcome"]:
            sys.exit(f"{cid}: give --outcome (why it was not applied).")
        if a.status:
            r["status"] = a.status
    write_comments(rows)
    print(f"{', '.join(ids)} updated")


def cmd_comment_approve(a):
    rows = read_comments()
    decisions = read_rows()
    problem = ref_is_lead_decision(a.ref, decisions)
    if problem:
        sys.exit(f"Cannot approve: {problem}. Comments are approved only from the lead's answer.")
    check_choice(a.action, ACTIONS, "--action")
    if a.all_proposed:
        targets = [r for r in rows if r["status"] == "open" and r["proposed_action"]]
    else:
        ids = comment_ids(a)
        if not ids:
            sys.exit("Name the comments with --ids, or use --all-proposed.")
        targets = []
        for cid in ids:
            r = next((x for x in rows if x["id"] == cid), None)
            if r is None:
                sys.exit(f"No comment {cid}.")
            if r["status"] != "open":
                sys.exit(f"{cid} is '{r['status']}', not open.")
            targets.append(r)
    for r in targets:
        action = a.action or r["proposed_action"]
        if not action:
            sys.exit(f"{r['id']} has no proposed action; give --action.")
        r["approved_action"] = action
        r["decision_ref"] = a.ref
        r["status"] = "approved"
    write_comments(rows)
    print(f"{len(targets)} comment(s) approved under {a.ref}")


def comment_problems(rows, decisions):
    problems, seen = [], set()
    wps = wp_folders()
    for r in rows:
        cid = r["id"]
        if check_wp_value(r["work_package"], wps):
            problems.append(f"{cid}: {check_wp_value(r['work_package'], wps)}")
        if not re.fullmatch(r"RC-\d{3,}", cid):
            problems.append(f"comment '{cid}': bad id")
        if cid in seen:
            problems.append(f"comment {cid}: duplicate id")
        seen.add(cid)
        if not r["text"].strip():
            problems.append(f"{cid}: 'text' is empty")
        if r["tier"] and r["tier"] not in TIERS:
            problems.append(f"{cid}: unknown tier '{r['tier']}'")
        for k in ("proposed_action", "approved_action"):
            if r[k] and r[k] not in ACTIONS:
                problems.append(f"{cid}: unknown {k} '{r[k]}'")
        if r["status"] not in COMMENT_STATUSES:
            problems.append(f"{cid}: unknown status '{r['status']}'")
        if r["status"] in ("approved", "done"):
            if not r["approved_action"] or not r["decision_ref"]:
                problems.append(f"{cid}: {r['status']} without the lead's approval recorded")
            elif ref_is_lead_decision(r["decision_ref"], decisions):
                problems.append(f"{cid}: {ref_is_lead_decision(r['decision_ref'], decisions)}")
        if r["status"] in ("done", "not applied") and not r["outcome"].strip():
            problems.append(f"{cid}: {r['status']} but 'outcome' is empty")
    return problems


def cmd_comment_check(a):
    problems = comment_problems(read_comments(), read_rows())
    if problems:
        print("Comment log problems:")
        for p in problems:
            print(" -", p)
        sys.exit(1)
    print("Comment log OK")


def cmd_comment_show(a):
    rows = read_comments()
    if a.id:
        rows = [r for r in rows if r["id"] == a.id]
    if a.wp:
        wp = resolve_wp(a.wp, allow_project=True)
        rows = [r for r in rows if r["work_package"] == wp]
    for field in ("status", "tier", "round", "reviewer"):
        value = getattr(a, field)
        if value:
            rows = [r for r in rows if r[field] == value]
    if a.search:
        q = a.search.lower()
        rows = [r for r in rows if any(q in (r[k] or "").lower() for k in COMMENT_FIELDS)]
    if not rows:
        print("No matching comments.")
        return
    if a.md:
        cell = lambda s: (s or "").replace("|", "/").replace("\n", " ")
        print("| ID | Source ref | Reviewer | Location | Comment | Proposed action | Proposed response | Approved | Outcome |")
        print("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
        for r in rows:
            approved = f"{r['approved_action']} ({r['decision_ref']})" if r["approved_action"] else ""
            print("| " + " | ".join(cell(x) for x in (r["id"], r["source_ref"], r["reviewer"], r["location"], r["text"],
                                                      r["proposed_action"], r["proposed_response"], approved, r["outcome"])) + " |")
        return
    for r in rows:
        print(f"{r['id']}  {r['work_package']}  [{r['status']}]  tier {r['tier'] or '-'}  round {r['round'] or '-'}  "
              f"{r['reviewer']}  {r['location']}"
              + (f"  (source ref {r['source_ref']})" if r["source_ref"] else ""))
        print(f"  Comment:  {r['text']}")
        if r["proposed_action"] or r["proposed_response"]:
            print(f"  Proposed: {r['proposed_action']}. {r['proposed_response']}")
        if r["approved_action"]:
            print(f"  Approved: {r['approved_action']} ({r['decision_ref']})")
        if r["outcome"]:
            print(f"  Outcome:  {r['outcome']}")
        print()


# ---------- sent log ----------
# One row per version that left the team, with an exact copy in the work package's work/sent/.
# A person sends; the team records. Rules: core/documents.md.

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
MC_FALLBACK = "{http://schemas.openxmlformats.org/markup-compatibility/2006}Fallback"


def read_sent():
    return read_table(SENT, SENT_FIELDS)


def cmd_sent_add(a):
    rows = read_sent()
    src = Path(a.file).resolve()
    if not src.is_file():
        sys.exit(f"No file {a.file}.")
    date = a.date or today()
    wp = resolve_wp(a.wp)
    sent_dir = wp_sent_dir(wp)
    if a.no_copy:
        # The file must not be committed (identifiable data, for example): log its checksum only.
        sid = next_prefixed_id(rows, "S-")
        shown = src.relative_to(ROOT.resolve()).as_posix() if src.is_relative_to(ROOT.resolve()) else src.name
        note = f"Not stored: {a.no_copy}" + (f". {a.note}" if a.note else "")
        rows.append({
            "id": sid, "work_package": wp, "date": date, "file": shown, "version": a.version, "recipients": a.to,
            "purpose": a.purpose, "sent_by": a.by, "sha256": sha256(src), "note": note,
        })
        write_table(SENT, SENT_FIELDS, rows)
        print(f"{sid}: {shown} (checksum only, no copy stored)")
        return
    sent_dir.mkdir(parents=True, exist_ok=True)
    if src.parent == sent_dir.resolve():
        stored = src
    else:
        stored = sent_dir / f"{date}_{src.name}"
        if stored.exists() and sha256(stored) != sha256(src):
            sys.exit(f"{stored.relative_to(ROOT)} already exists with different content. Rename the file first.")
        shutil.copy2(src, stored)
    sid = next_prefixed_id(rows, "S-")
    rows.append({
        "id": sid, "work_package": wp, "date": date, "file": stored.relative_to(ROOT).as_posix(), "version": a.version,
        "recipients": a.to, "purpose": a.purpose, "sent_by": a.by, "sha256": sha256(stored), "note": a.note,
    })
    write_table(SENT, SENT_FIELDS, rows)
    print(f"{sid}: {stored.relative_to(ROOT).as_posix()}")


def cmd_sent_list(a):
    rows = read_sent()
    if not rows:
        print("Nothing sent yet.")
        return
    for r in rows:
        print(f"{r['id']}  {r['work_package']}  {r['date']}  {r['version'] or '-'}  to {r['recipients']}  "
              f"by {r['sent_by']}  ({r['purpose']})")
        print(f"  {r['file']}  sha256 {r['sha256'][:12]}" + (f"  {r['note']}" if r["note"] else ""))


def sent_problems(rows):
    problems, seen = [], set()
    wps = wp_folders()
    for r in rows:
        sid = r["id"]
        if r["work_package"] not in wps:
            problems.append(f"sent {sid}: work_package '{r['work_package']}' is not a work package of this project")
        if not re.fullmatch(r"S-\d{3,}", sid):
            problems.append(f"sent '{sid}': bad id")
        if sid in seen:
            problems.append(f"sent {sid}: duplicate id")
        seen.add(sid)
        if r["note"].startswith("Not stored:"):
            continue  # logged with --no-copy: there is no stored copy to check
        path = ROOT / r["file"]
        if not path.is_file():
            problems.append(f"{sid}: stored copy {r['file']} is missing")
        elif sha256(path) != r["sha256"]:
            problems.append(f"{sid}: stored copy {r['file']} has changed since it was logged")
    return problems


def docx_paragraphs(path: Path):
    """Body paragraphs of a .docx as they read with every tracked change rejected.

    Inserted text, moved-to text and inserted table rows are left out; deleted and moved-from
    text is kept. A paragraph whose paragraph mark was inserted is joined to the next one.
    """
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read("word/document.xml"))
    body = root.find(W + "body")
    skip = {W + "ins", W + "moveTo", MC_FALLBACK}

    def text_of(el, out):
        for child in el:
            tag = child.tag
            if tag in skip or tag == W + "p":
                continue
            if tag in (W + "t", W + "delText"):
                out.append(child.text or "")
            elif tag == W + "tab":
                out.append(" ")
            elif tag in (W + "br", W + "cr"):
                out.append(" ")
            else:
                text_of(child, out)

    def paragraphs(el):
        for child in el:
            tag = child.tag
            if tag in skip:
                continue
            if tag == W + "tr" and child.find(f"{W}trPr/{W}ins") is not None:
                continue
            if tag == W + "p":
                yield child
            yield from paragraphs(child)

    out, carry = [], ""
    for p in paragraphs(body):
        parts = []
        text_of(p, parts)
        text = carry + "".join(parts)
        if p.find(f"{W}pPr/{W}rPr/{W}ins") is not None:
            carry = text
            continue
        carry = ""
        text = " ".join(text.split())
        if text:
            out.append(text)
    if carry.strip():
        out.append(" ".join(carry.split()))
    return out


def docx_revisions(path: Path):
    """Tracked changes and comments in a .docx, counted by author."""
    counts = {}
    kinds = {W + "ins": "insertions", W + "del": "deletions", W + "moveFrom": "moves", W + "rPrChange": "format",
             W + "pPrChange": "format"}
    with zipfile.ZipFile(path) as z:
        names = set(z.namelist())
        root = ET.fromstring(z.read("word/document.xml"))
        for el in root.iter():
            kind = kinds.get(el.tag)
            if kind:
                author = el.get(W + "author") or "(no author)"
                counts.setdefault(author, Counter())[kind] += 1
        if "word/comments.xml" in names:
            for c in ET.fromstring(z.read("word/comments.xml")).iter(W + "comment"):
                author = c.get(W + "author") or "(no author)"
                counts.setdefault(author, Counter())["comments"] += 1
    return counts


def word_diff(old: str, new: str) -> str:
    a, b = old.split(), new.split()
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op == "equal":
            out.append(" ".join(a[i1:i2]))
        if op in ("delete", "replace"):
            out.append("[-" + " ".join(a[i1:i2]) + "-]")
        if op in ("insert", "replace"):
            out.append("{+" + " ".join(b[j1:j2]) + "+}")
    return " ".join(out)


def cmd_sent_compare(a):
    rows = read_sent()
    row = next((r for r in rows if r["id"] == a.id), None)
    if row is None:
        sys.exit(f"No sent version {a.id}.")
    if row["note"].startswith("Not stored:"):
        sys.exit(f"{a.id} was logged with --no-copy, so there is no stored copy to compare with. "
                 f"Compare the returned file with the sender's own copy, checking it against checksum {row['sha256']}.")
    sent_path, returned = ROOT / row["file"], Path(a.file)
    if not returned.is_file():
        sys.exit(f"No file {a.file}.")
    lines = [f"# {returned.name} compared with {a.id} ({row['file']})", ""]
    if sha256(returned) == row["sha256"]:
        lines.append("The returned file is byte-identical to the copy that was sent.")
    elif sent_path.suffix.lower() == ".docx" and returned.suffix.lower() == ".docx":
        lines += ["## Tracked changes and comments in the returned file", ""]
        revs = docx_revisions(returned)
        before = docx_revisions(sent_path)
        if revs:
            lines += ["| Author | Insertions | Deletions | Moves | Format | Comments |", "| --- | --- | --- | --- | --- | --- |"]
            for author, c in sorted(revs.items()):
                lines.append(f"| {author} | {c['insertions']} | {c['deletions']} | {c['moves']} | {c['format']} | {c['comments']} |")
            lines.append("")
            lines.append("Counts are of tracked-change elements and can differ from the count Word shows.")
            if before:
                lines.append("The sent copy already held tracked changes or comments; these counts include them.")
        else:
            lines.append("None.")
        old, new = docx_paragraphs(sent_path), docx_paragraphs(returned)
        blocks = [op for op in difflib.SequenceMatcher(None, old, new, autojunk=False).get_opcodes() if op[0] != "equal"]
        lines += ["", "## Changes made without Track Changes", "",
                  f"{len(blocks)} passage(s) differ when every tracked change in both files is rejected. "
                  "Each is an edit whose author Word did not record, or a tracked change the recipient accepted or rejected. "
                  "Log each one in the comment log with type 'untracked edit'. Body text only: headers, footers, footnotes, "
                  "formatting and empty paragraphs are not compared.", ""]
        for n, (op, i1, i2, j1, j2) in enumerate(blocks, start=1):
            lines.append(f"### {n}. Sent paragraph {i1 + 1}" + (f" to {i2}" if i2 - i1 > 1 else "") + f" ({op})")
            lines.append("")
            if op == "replace" and i2 - i1 == 1 and j2 - j1 == 1:
                lines.append(word_diff(old[i1], new[j1]))
            else:
                for t in old[i1:i2]:
                    lines.append(f"- Sent: {t}")
                for t in new[j1:j2]:
                    lines.append(f"- Returned: {t}")
            lines.append("")
    elif returned.suffix.lower() in (".md", ".txt", ".csv"):
        old = sent_path.read_text(encoding="utf-8").splitlines()
        new = returned.read_text(encoding="utf-8").splitlines()
        lines += ["```diff"] + list(difflib.unified_diff(old, new, "sent", "returned", lineterm="")) + ["```"]
    else:
        lines.append("The files differ. Text comparison covers .docx, .md, .txt and .csv files only.")
    report = "\n".join(lines).rstrip() + "\n"
    if a.out:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(report, encoding="utf-8")
        print(f"Report written to {a.out}")
    else:
        print(report)


# ---------- outcome log ----------
# One row per observed sign that an outcome in project/results.md happened. Every row names its
# source and the other factors that may explain what was observed. Rules: core/results-chain.md.

def results_outcomes() -> dict:
    """Outcomes stated in project/results.md: {'O1': (statement, date after 'By:' or None)}."""
    if not RESULTS.exists():
        return {}
    section = re.search(r"^## Outcomes\s*\n(.*?)(?=^## |\Z)", RESULTS.read_text(encoding="utf-8"), re.M | re.S)
    out = {}
    for oid, rest in re.findall(r"^- (O\d+)\.\s*(.+)$", section.group(1) if section else "", re.M):
        by = re.search(r"\bBy:\s*(.+)$", rest)
        out[oid] = (rest.strip(), parse_date(by.group(1)) if by else None)
    return out


def read_outcomes():
    return read_table(OUTCOMES, OUTCOME_FIELDS)


def cmd_outcome_add(a):
    rows = read_outcomes()
    stated = results_outcomes()
    if a.outcome not in stated:
        sys.exit(f"No outcome {a.outcome} in project/results.md. Stated outcomes: {', '.join(stated) or 'none'}")
    for name, value in (("--observed", a.observed), ("--source", a.source), ("--by", a.by),
                        ("--other-factors", a.other_factors)):
        if not value.strip():
            sys.exit(f"{name} is empty. An outcome is logged only with what was observed, its source, who reported it, "
                     "and the other factors that may explain it ('none identified' if none).")
    oid = next_prefixed_id(rows, "OB-")
    rows.append({
        "id": oid, "date": a.date or today(), "outcome": a.outcome, "observed": a.observed, "source": a.source,
        "reported_by": a.by, "other_factors": a.other_factors,
    })
    write_table(OUTCOMES, OUTCOME_FIELDS, rows)
    print(oid)


def cmd_outcome_show(a):
    rows = read_outcomes()
    stated = results_outcomes()
    if a.outcome:
        rows = [r for r in rows if r["outcome"] == a.outcome]
    if a.md:
        cell = lambda s: (s or "").replace("|", "/").replace("\n", " ")
        print("| ID | Date | Outcome | Observed | Source | Reported by | Other factors |")
        print("| --- | --- | --- | --- | --- | --- | --- |")
        for r in rows:
            print("| " + " | ".join(cell(r[k]) for k in OUTCOME_FIELDS) + " |")
        return
    for oid, (statement, by) in stated.items():
        if a.outcome and oid != a.outcome:
            continue
        print(f"{oid}. {statement}")
        seen = [r for r in rows if r["outcome"] == oid]
        if not seen:
            print("  Nothing observed yet.")
        for r in seen:
            print(f"  {r['id']}  {r['date']}  {r['observed']}")
            print(f"    Source: {r['source']}  Reported by: {r['reported_by']}  Other factors: {r['other_factors']}")
    if not stated:
        print("No outcomes are stated in project/results.md yet.")


def outcome_problems(rows):
    problems, seen = [], set()
    stated = results_outcomes()
    for r in rows:
        oid = r["id"]
        if not re.fullmatch(r"OB-\d{3,}", oid):
            problems.append(f"outcome '{oid}': bad id")
        if oid in seen:
            problems.append(f"outcome {oid}: duplicate id")
        seen.add(oid)
        if r["outcome"] not in stated:
            problems.append(f"{oid}: outcome '{r['outcome']}' is not stated in project/results.md")
        for k in ("date", "observed", "source", "reported_by", "other_factors"):
            if not r[k].strip():
                problems.append(f"{oid}: '{k}' is empty")
    return problems


# ---------- checkpoints ----------

def frozen_changes_since(wp: str, tag: str):
    """Files in the work package's work/frozen/ added or changed since the given checkpoint (or ever, if none)."""
    rel = wp_frozen(wp).relative_to(ROOT).as_posix()
    changed = set(git("status", "--porcelain", "--", rel, check=False).splitlines())
    if tag:
        changed |= set(git("diff", "--name-only", tag, "HEAD", "--", rel, check=False).splitlines())
    else:
        changed |= set(git("ls-files", "--", rel, check=False).splitlines())
    return [c for c in changed if c.strip() and not c.strip().endswith(".gitkeep")]


def cmd_checkpoint(a):
    need_project()
    wp = resolve_wp(a.wp, allow_project=True)
    stage = re.sub(r"[^a-z0-9-]+", "-", a.stage.lower()).strip("-")
    all_tags = tags_in_order()
    prefix = f"cp-{wp.lower()}-"
    own = [t for t in all_tags if t.startswith(prefix)]
    tag = f"{prefix}{stage}-{len([t for t in own if t.startswith(f'{prefix}{stage}-')]) + 1:02d}"
    if wp != "project" and master_is_external(wp) and not a.no_export and not frozen_changes_since(wp, own[-1] if own else ""):
        frozen = wp_frozen(wp).relative_to(ROOT).as_posix()
        sys.exit(f"The master copy of {wp} is outside the repository (state.md: 'Master copy: {master_copy(wp)}').\n"
                 f"Save a DOCX and a PDF export of it in {frozen}/ first (core/checkpoint-rules.md),\n"
                 "or pass --no-export \"<reason>\" if nothing in it changed since the last checkpoint.")
    rows = read_rows()
    filled = 0
    for r in rows:
        if not r["checkpoint"]:
            r["checkpoint"] = tag
            filled += 1
    write_rows(rows)
    git("add", "-A")
    msg = f"Checkpoint {tag}" + (f": {a.message}" if a.message else "")
    if a.no_export:
        msg += f"\n\nNo export of the master copy: {a.no_export}"
    if git("status", "--porcelain"):
        git("commit", "-m", msg)
    else:
        git("commit", "--allow-empty", "-m", msg)
    git("tag", "-a", tag, "-m", msg)
    print(f"{tag} saved ({filled} decision(s) recorded in it)")


def cmd_rollback(a):
    need_project()
    order = tags_in_order()
    if a.to not in order:
        sys.exit(f"No checkpoint named {a.to}. Available: {', '.join(order) or 'none'}")
    wp = resolve_wp(a.wp) if a.wp else tag_wp(a.to)
    if wp not in wp_folders():
        sys.exit(f"{a.to} is not a checkpoint of one work package. Name the work package whose work returns to it: --wp WPn")
    if git("status", "--porcelain"):
        sys.exit("There are unsaved changes. Save a checkpoint first, so nothing is lost.")
    work = wp_work(wp).relative_to(ROOT).as_posix()
    if not git("ls-tree", "-r", "--name-only", a.to, "--", work, check=False):
        sys.exit(f"{wp} had no work folder at {a.to}, so there is nothing to return to.")
    later = set(order[order.index(a.to) + 1:])
    head = git("rev-parse", "HEAD")
    # Restore the work package's work files as they stood at the checkpoint, in a new commit.
    # Other work packages, and the project files, stay as they are.
    git("rm", "-r", "-q", "--ignore-unmatch", work)
    git("checkout", a.to, "--", work)
    # Frozen exports and sent copies are records, not work in progress: keep the current ones.
    for keep in (wp_frozen(wp), wp_sent_dir(wp)):
        rel = keep.relative_to(ROOT).as_posix()
        if git("ls-tree", "-r", "--name-only", head, "--", rel, check=False):
            git("checkout", head, "--", rel)
    rows = read_rows()
    marked = []
    for r in rows:
        if r["work_package"] != wp:
            continue
        if (r["checkpoint"] in later or not r["checkpoint"]) and not r["status"].startswith("reversed by"):
            if r["status"] != "rolled back":
                r["status"] = "rolled back"
                marked.append(r["id"])
    rid = next_id(rows)
    rows.append({
        "id": rid, "project": project_name(), "work_package": wp, "date": today(), "stage": "rollback",
        "decision": f"Return the work of {wp} to checkpoint {a.to}?", "options": "Keep current work; roll back",
        "choice": f"Roll back to {a.to}", "reason": a.reason, "evidence": "",
        "decided_by": a.by, "reversible": "yes", "escalated": "", "status": "approved", "checkpoint": "",
    })
    write_rows(rows)
    git("add", "-A")
    git("commit", "-m", f"Roll back {wp} work to {a.to}: {a.reason}")
    print(f"{wp} work restored to {a.to}. Logged as {rid}. Marked rolled back: {', '.join(marked) or 'none'}")


# ---------- memos ----------

def memo_paths():
    return sorted(ESCALATIONS.glob("EM-*.md"))


def memo_status(p: Path) -> str:
    m = re.search(r"^Status:\s*(\w+)", p.read_text(encoding="utf-8"), re.M)
    return m.group(1).lower() if m else "unknown"


def cmd_memo_new(a):
    need_project()
    template = TEAM / "core" / "decision-memo-template.md"
    nums = [int(p.stem[3:]) for p in memo_paths() if re.fullmatch(r"EM-\d{3,}", p.stem)]
    mid = f"EM-{(max(nums) + 1) if nums else 1:03d}"
    body = template.read_text(encoding="utf-8")
    body = body.replace("{{ID}}", mid).replace("{{ISSUE}}", a.issue).replace("{{DATE}}", today())
    body = body.replace("{{URGENCY}}", "urgent" if a.urgent else "batched at stage end")
    wps = wp_folders()
    body = body.replace("{{WP}}", resolve_wp(a.wp, allow_project=True) if a.wp or len(wps) == 1 else "project")
    path = ESCALATIONS / f"{mid}.md"
    path.write_text(body, encoding="utf-8")
    print(path.relative_to(ROOT))


def cmd_memo_list(a):
    need_project()
    paths = memo_paths()
    if a.open:
        paths = [p for p in paths if memo_status(p) == "open"]
    if not paths:
        print("No memos." if not a.open else "No open memos.")
        return
    for p in paths:
        text = p.read_text(encoding="utf-8")
        issue = re.search(r"^\*\*Issue:\*\*\s*(.+)$", text, re.M)
        print(f"{p.stem}  {memo_status(p):8}  {file_field(p, 'Work package') or 'project':8}  "
              f"{issue.group(1).strip() if issue else ''}")


def cmd_memo_close(a):
    need_project()
    path = ESCALATIONS / f"{a.id}.md"
    if not path.exists():
        sys.exit(f"No memo {a.id}.")
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"^Status:\s*\w+", "Status: decided", text, count=1, flags=re.M)
    text = text.rstrip() + f"\n\n## Lead's decision ({today()}, {a.by})\n\n{a.decision}\n"
    path.write_text(text, encoding="utf-8")
    print(f"{a.id} closed")


# ---------- weekly health check ----------
# Facts for the process monitor, computed with fixed rules from the project files.
# Rules: core/learning-and-oversight.md. Thresholds: health_check in team.config.yaml.

HEALTH_DIR = PROJECT / "health"
STATUS = PROJECT / "status.md"
CONFIG = ROOT / "team.config.yaml" if (ROOT / "team.config.yaml").exists() else TEAM / "team.config.yaml"
HEALTH_DEFAULTS = {
    "day": "Monday",
    "memo_overdue_amber_days": 1, "memo_overdue_red_days": 5,
    "gate_wait_amber_days": 5, "gate_wait_red_days": 10,
    "checkpoint_gap_amber_days": 7, "checkpoint_gap_red_days": 14,
    "idle_runs_amber": 2, "idle_runs_red": 4,
    "time_limit_runs_amber": 2, "time_limit_runs_red": 3,
    "days_per_stage_amber": 3, "days_per_stage_red": 1.5,
    "wp_overdue_amber_days": 1, "wp_overdue_red_days": 7,
    "wp_blocked_amber_days": 7, "wp_blocked_red_days": 14,
}
AGENT_ROLES = ("coordinator", "writer", "evidence checker", "blind reviewer", "compliance check",
               "after action reviewer", "process monitor")
WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
MONTHS = {m: i for i, m in enumerate(["january", "february", "march", "april", "may", "june", "july",
                                      "august", "september", "october", "november", "december"], start=1)}
FLAG_ORDER = {"n/a": 0, "green": 1, "amber": 2, "red": 3}


def config_block(name: str) -> dict:
    """Flat 'key: value' pairs under a top-level block of team.config.yaml. Standard library only."""
    if not CONFIG.exists():
        return {}
    out, inside = {}, False
    for line in CONFIG.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line[0].isspace():
            inside = line.split("#", 1)[0].strip() == f"{name}:"
            continue
        if inside and ":" in line:
            key, _, value = line.split("#", 1)[0].partition(":")
            out[key.strip()] = value.strip().strip('"').strip("'")
    return out


def health_settings() -> dict:
    s = dict(HEALTH_DEFAULTS)
    for key, value in config_block("health_check").items():
        if key in s and isinstance(s[key], (int, float)):
            try:
                s[key] = float(value) if "." in value else int(value)
            except ValueError:
                sys.exit(f"team.config.yaml: health_check.{key} must be a number, found '{value}'")
        else:
            s[key] = value
    return s


def parse_date(text: str):
    """The first date in the text: 2026-11-16, 16 November 2026 or November 16, 2026."""
    text = text or ""
    m = re.search(r"\b(\d{4})-(\d{2})-(\d{2})\b", text)
    if m:
        return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = re.search(r"\b(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})\b", text)
    if m and m.group(2).lower() in MONTHS:
        return dt.date(int(m.group(3)), MONTHS[m.group(2).lower()], int(m.group(1)))
    m = re.search(r"\b([A-Za-z]+)\s+(\d{1,2}),?\s+(\d{4})\b", text)
    if m and m.group(1).lower() in MONTHS:
        return dt.date(int(m.group(3)), MONTHS[m.group(1).lower()], int(m.group(2)))
    return None


def open_tasks(state_file: Path):
    """The items under '## Open tasks' in a state file."""
    if not state_file.exists():
        return []
    m = re.search(r"^## Open tasks\s*\n(.*?)(?=^## |\Z)", state_file.read_text(encoding="utf-8"), re.M | re.S)
    items = re.findall(r"^- (.+)$", m.group(1), re.M) if m else []
    return [i for i in items if not re.match(r"(none|nothing)\b", i.strip(), re.I)]


def memo_facts():
    """Open memos: (id, issue, raised, needed_by, is_gate)."""
    out = []
    for p in memo_paths():
        if memo_status(p) != "open":
            continue
        text = p.read_text(encoding="utf-8")
        issue = re.search(r"^\*\*Issue:\*\*\s*(.+)$", text, re.M)
        raised = re.search(r"^Raised:\s*(.+)$", text, re.M)
        needed = re.search(r"^Needed by:\s*(.+)$", text, re.M)
        issue = issue.group(1).strip() if issue else ""
        out.append((p.stem, issue, parse_date(raised.group(1)) if raised else None,
                    parse_date(needed.group(1)) if needed else None, issue.lower().startswith("gate:")))
    return out


def status_history(limit: int = 30):
    """Committed versions of status.md, newest first, as dicts of their lines."""
    rel = STATUS.relative_to(ROOT).as_posix()
    out = []
    for sha in git("log", f"-{limit}", "--format=%H", "--", rel, check=False).splitlines():
        text = git("show", f"{sha}:{rel}", check=False)
        fields = dict(re.findall(r"^(Run|Moved|Stopped|Waiting on the lead|Next):\s*(.*)$", text, re.M))
        out.append(fields)
    return out


def playbook_stages(playbook: Path):
    """[(number, name, checkpoint slug)] for each stage heading of a playbook."""
    text = playbook.read_text(encoding="utf-8")
    stages = []
    for m in re.finditer(r"^### (\d+)\. (.+?)\s*\n(.*?)(?=^### |^## |\Z)", text, re.M | re.S):
        slug = re.search(r"`cp-([a-z0-9-]+)-(?:NN|\d{2})`", m.group(3))
        stages.append((int(m.group(1)), m.group(2).strip(), slug.group(1) if slug else ""))
    return stages


def grade(value, amber, red, lower_is_worse=False) -> str:
    if value is None:
        return "n/a"
    if lower_is_worse:
        return "red" if value < red else "amber" if value < amber else "green"
    return "red" if value >= red else "amber" if value >= amber else "green"


def next_health_day(day_name: str, after: dt.date) -> dt.date:
    target = WEEKDAYS.index(day_name.lower()) if day_name.lower() in WEEKDAYS else 0
    ahead = (target - after.weekday()) % 7 or 7
    return after + dt.timedelta(days=ahead)


def health_digests():
    """Saved digests (not facts files), oldest first."""
    if not HEALTH_DIR.exists():
        return []
    return sorted(p for p in HEALTH_DIR.glob("*.md") if re.fullmatch(r"\d{4}-\d{2}-\d{2}", p.stem))


def health_due(s: dict, now: dt.date):
    digests = health_digests()
    last = parse_date(digests[-1].stem) if digests else None
    if last == now:
        return False, f"a digest was already saved today ({digests[-1].relative_to(ROOT)})"
    is_day = now.weekday() == WEEKDAYS.index(s["day"].lower()) if s["day"].lower() in WEEKDAYS else False
    if is_day:
        return True, f"today is the health-check day ({s['day']})"
    if last and (now - last).days > 7:
        return True, f"the last digest is {(now - last).days} days old"
    return False, f"next health check on {next_health_day(s['day'], now).isoformat()}"


def health_facts(now: dt.date):
    """[(measure, value, flag, details)] and the settings used."""
    s = health_settings()
    facts = []

    # Memos past their "Needed by" date, and gates waiting on the lead.
    memos = memo_facts()
    overdue, undated, gates = [], [], []
    for mid, issue, raised, needed, is_gate in memos:
        if is_gate:
            gates.append(((now - raised).days if raised else None, mid, issue))
        elif needed is None:
            undated.append(f"{mid}: {issue}")
        elif now > needed:
            overdue.append(((now - needed).days, mid, issue))
    worst = max((d for d, _, _ in overdue), default=0)
    facts.append(("Memos past \"Needed by\"",
                  ", ".join(f"{m}, {d} day(s) past" for d, m, _ in sorted(overdue, reverse=True)) or "None",
                  grade(worst, s["memo_overdue_amber_days"], s["memo_overdue_red_days"]) if overdue else "green",
                  [f"{m}: {i} ({d} day(s) past)" for d, m, i in overdue]))
    facts.append(("Open memos with no \"Needed by\" date", ", ".join(u.split(":")[0] for u in undated) or "None",
                  "amber" if undated else "green", undated))
    gate_days = max((d for d, _, _ in gates if d is not None), default=0)
    facts.append(("Gates waiting on the lead",
                  ", ".join(f"{m}, {d} day(s)" if d is not None else f"{m}, raised date missing" for d, m, _ in gates) or "None",
                  grade(gate_days, s["gate_wait_amber_days"], s["gate_wait_red_days"]) if gates else "green",
                  [f"{m}: {i}" for _, m, i in gates]))

    # Each work package in progress: days since its last checkpoint while it has open tasks.
    tags = tags_in_order()
    wps = wp_folders()
    in_progress = [w for w in wps if wp_status(w) in ("active", "waiting")]
    for wp in in_progress:
        own = [t for t in tags if tag_wp(t) == wp]
        tasks = open_tasks(wp_dir(wp) / "state.md")
        if own:
            since = parse_date(git("log", "-1", "--format=%cs", own[-1], check=False))
            label = own[-1]
        else:
            since, label = parse_date(wp_field(wp, "Started")), "work package start"
        gap = (now - since).days if since else None
        name = f"{wp}: days since last checkpoint, with tasks open"
        if not tasks:
            facts.append((name, f"{gap} ({label}); no open tasks" if gap is not None else "No open tasks", "green", []))
        else:
            facts.append((name, f"{gap} ({label})" if gap is not None else "Date of last checkpoint not found",
                          grade(gap, s["checkpoint_gap_amber_days"], s["checkpoint_gap_red_days"]), tasks))

    # Runs in a row that moved nothing (not counting runs that stopped because everything waits on the lead),
    # and runs in a row that hit the time limit on the same task.
    history = status_history()
    idle = 0
    for h in history:
        moved = h.get("Moved", "").strip().lower()
        stopped = h.get("Stopped", "").strip().lower()
        if re.match(r"(nothing|none|no change)", moved) and not stopped.startswith("waiting on the lead"):
            idle += 1
        else:
            break
    facts.append(("Runs in a row that moved nothing", str(idle),
                  grade(idle, s["idle_runs_amber"], s["idle_runs_red"]),
                  [h.get("Run", "(no Run line)") for h in history[:idle]]))
    limit_task, limit_runs = "", 0
    for h in history:
        m = re.match(r"time limit\s*\((.+)\)", h.get("Stopped", "").strip(), re.I)
        task = m.group(1).strip().lower() if m else ""
        if not task or (limit_task and task != limit_task):
            break
        limit_task, limit_runs = task, limit_runs + 1
    facts.append(("Runs in a row that hit the time limit on one task",
                  f"{limit_runs} ({limit_task})" if limit_runs else "0",
                  grade(limit_runs, s["time_limit_runs_amber"], s["time_limit_runs_red"]), []))

    # Register: agent decisions not reversible and logged without a memo; proposed rows with no memo; check errors.
    problems, rows, comments, _ = register_problems()
    live = [r for r in rows if r["status"] in ("proposed", "approved")]

    def by_agent(r):
        who = r["decided_by"].lower().replace("-", " ")
        return any(role in who for role in AGENT_ROLES)

    unescalated = [r for r in live if r["reversible"] == "no" and not r["escalated"] and by_agent(r)]
    facts.append(("Agent decisions not reversible, logged without a memo",
                  ", ".join(r["id"] for r in unescalated) or "None", "red" if unescalated else "green",
                  [f"{r['id']} ({r['decided_by']}, {r['stage']}): {r['choice']}" for r in unescalated]))
    orphans = [r for r in rows if r["status"] == "proposed" and not r["escalated"]]
    facts.append(("Register rows left \"proposed\" with no memo", ", ".join(r["id"] for r in orphans) or "None",
                  "amber" if orphans else "green", [f"{r['id']}: {r['decision']}" for r in orphans]))
    facts.append(("`register check` errors", str(len(problems)), "red" if problems else "green", problems))

    # Comments still open in a round whose triage the lead has already decided.
    decided_rounds = {(c["work_package"], c["round"]) for c in comments if c["approved_action"] or c["decision_ref"]}
    stray = [c for c in comments if c["status"] == "open" and (c["work_package"], c["round"]) in decided_rounds]
    facts.append(("Comments open after their round was decided", ", ".join(c["id"] for c in stray) or "None",
                  "amber" if stray else "green", [f"{c['id']} ({c['work_package']}, round {c['round']})" for c in stray]))

    # Each work package in progress: days to the current stage's due date (its state.md "Due:"),
    # or else days to the deadline in its brief, per stage left.
    for wp in in_progress:
        due = parse_date(wp_field(wp, "Due"))
        if due is not None:
            days = (due - now).days
            facts.append((f"{wp}: days to the current stage's due date", f"{days} days to {due.isoformat()}",
                          grade(days, s["days_per_stage_amber"], s["days_per_stage_red"], lower_is_worse=True), []))
            continue
        name = f"{wp}: days to deadline per stage left"
        deadline = wp_deadline(wp)
        playbook = TEAM / "playbooks" / f"{wp_field(wp, 'Type')}.md"
        stage = wp_field(wp, "Stage").lower()
        left = None
        if playbook.exists() and stage:
            stages = [st for st in playbook_stages(playbook) if st[2]]
            for i, (_, stage_name, slug) in enumerate(stages):
                if stage == slug or stage_name.lower().startswith(stage) or stage in stage_name.lower():
                    left = len(stages) - i
                    break
        if deadline is None:
            facts.append((name, "No deadline in the work package brief", "n/a", []))
        elif left is None:
            facts.append((name, f"{(deadline - now).days} days to {deadline.isoformat()}; stage '{stage}' not found in the playbook",
                          "n/a", []))
        else:
            days = (deadline - now).days
            per = days / left
            facts.append((name, f"{days} days to {deadline.isoformat()}, {left} stage(s) left: {per:.1f} per stage",
                          "red" if days < 0 else grade(per, s["days_per_stage_amber"], s["days_per_stage_red"], lower_is_worse=True),
                          []))

    # Work packages past the deadline in their brief and not signed off, whether started or not.
    late = []
    for wp in wps:
        deadline = wp_deadline(wp)
        if wp_status(wp) not in ("signed off", "dropped") and deadline and now > deadline:
            late.append(((now - deadline).days, wp, deadline))
    facts.append(("Work packages past their deadline",
                  ", ".join(f"{w}, {d} day(s) past" for d, w, _ in sorted(late, reverse=True)) or "None",
                  grade(max(d for d, _, _ in late), s["wp_overdue_amber_days"], s["wp_overdue_red_days"]) if late else "green",
                  [f"{w}: deadline {dl.isoformat()}, status {wp_status(w)}, stage {wp_field(w, 'Stage') or 'not set'}"
                   for _, w, dl in late]))

    # Work packages stopped because they wait for another work package: "Status: waiting (since <date>)".
    blocked, undated_wait = [], []
    for wp in wps:
        if wp_status(wp) != "waiting":
            continue
        since = parse_date(wp_field(wp, "Status"))
        waits = wp_field(wp, "Waits for") or "not stated"
        if since is None:
            undated_wait.append(f"{wp}: waiting for {waits}; no date on the Status line")
        else:
            blocked.append(((now - since).days, wp, waits))
    if blocked:
        blocked_flag = grade(max(d for d, _, _ in blocked), s["wp_blocked_amber_days"], s["wp_blocked_red_days"])
    else:
        blocked_flag = "green"
    if undated_wait and blocked_flag == "green":
        blocked_flag = "amber"
    facts.append(("Work packages waiting on another work package",
                  ", ".join([f"{w}, {d} day(s)" for d, w, _ in sorted(blocked, reverse=True)]
                            + [u.split(":")[0] + ", date missing" for u in undated_wait]) or "None",
                  blocked_flag, [f"{w}: waiting {d} day(s) for {x}" for d, w, x in blocked] + undated_wait))

    # Outcomes in results.md whose date has passed with nothing in the outcome log.
    stated = results_outcomes()
    logged = {r["outcome"] for r in (read_outcomes() if OUTCOMES.exists() else [])}
    silent = [(oid, by) for oid, (_, by) in stated.items() if by and now > by and oid not in logged]
    if not stated:
        facts.append(("Outcomes past their date with nothing observed", "No outcomes stated in results.md", "n/a", []))
    else:
        facts.append(("Outcomes past their date with nothing observed", ", ".join(o for o, _ in silent) or "None",
                      "amber" if silent else "green",
                      [f"{o}: expected by {by.isoformat()}: {stated[o][0]}" for o, by in silent]))
    return facts, s


def wp_table(md: bool = False) -> str:
    """The work packages in the order of work, as plain lines or a Markdown table."""
    tags = tags_in_order()
    rows = []
    for wp in wp_folders():
        own = [t for t in tags if tag_wp(t) == wp]
        deadline = wp_deadline(wp)
        rows.append((wp, wp_field(wp, "Title"), wp_field(wp, "Type"), wp_field(wp, "Stage") or "not set",
                     wp_field(wp, "Status") or "active", wp_field(wp, "Waits for") or "none",
                     deadline.isoformat() if deadline else "not set", own[-1] if own else "none yet"))
    head = ("WP", "Title", "Playbook", "Stage", "Status", "Waits for", "Deadline", "Last checkpoint")
    if md:
        lines = ["| " + " | ".join(head) + " |", "| " + " | ".join("---" for _ in head) + " |"]
        lines += ["| " + " | ".join(str(c).replace("|", "/") for c in r) + " |" for r in rows]
        return "\n".join(lines)
    return "\n".join(f"{r[0]}  {r[1]}  [{r[2]}]  stage: {r[3]}  status: {r[4]}  waits for: {r[5]}  "
                     f"deadline: {r[6]}  last checkpoint: {r[7]}" for r in rows)


def cmd_health(a):
    need_project()
    now = parse_date(a.today) if a.today else dt.date.today()
    s = health_settings()
    if a.due:
        due, why = health_due(s, now)
        print(("due: " if due else "not due: ") + why)
        return
    facts, s = health_facts(now)
    overall = max((f[2] for f in facts), key=lambda f: FLAG_ORDER[f], default="green")
    if overall == "n/a":
        overall = "green"
    lines = [
        f"# Health check facts, {now.isoformat()}",
        "",
        f"Project: {project_name()}. Stage: {state_field('Stage') or 'not set'}.",
        "Computed by `python3 tools/team.py health` from the project files, with the thresholds in "
        "`team.config.yaml` (`health_check`).",
        "",
        f"**Overall: {overall}.**",
        "",
        "## Work packages",
        "",
        wp_table(md=True),
        "",
        "## Measures",
        "",
        "| Measure | Value | Flag |",
        "| --- | --- | --- |",
    ]
    for measure, value, flag, _ in facts:
        lines.append(f"| {measure} | {str(value).replace('|', '/')} | {flag.capitalize() if flag != 'n/a' else 'n/a'} |")
    flagged = [f for f in facts if f[2] in ("amber", "red") and f[3]]
    if flagged:
        lines += ["", "## Details of flagged measures", ""]
        for measure, _, flag, details in flagged:
            lines.append(f"**{measure}** ({flag})")
            lines.append("")
            lines += [f"- {d}" for d in details]
            lines.append("")
    lines += ["", f"Next health check: {next_health_day(s['day'], now).isoformat()} ({s['day']})."]
    text = "\n".join(lines).rstrip() + "\n"
    if a.out:
        out = (ROOT / a.out) if not Path(a.out).is_absolute() else Path(a.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        print(f"{out.relative_to(ROOT) if out.is_relative_to(ROOT) else out}  (overall: {overall})")
    else:
        print(text, end="")


# ---------- init and status ----------

def need_playbook(name: str):
    if not (TEAM / "playbooks" / f"{name}.md").exists() or name.startswith("_"):
        names = sorted(p.stem for p in (TEAM / "playbooks").glob("*.md") if not p.stem.startswith("_"))
        sys.exit(f"No playbook '{name}'. Available: {', '.join(names)}")


def create_wp(title: str, playbook: str, status: str, waits_for: str = "") -> Path:
    """Create the next work package folder from project-template/wp-template/. Numbers are never reused."""
    template = TEAM / "project-template" / "wp-template"
    if not template.exists():
        sys.exit("project-template/wp-template/ is missing.")
    number = max((int(w[2:]) for w in wp_folders()), default=0) + 1
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:40].strip("-") or "work"
    folder = WP_ROOT / f"WP{number}-{slug}"
    shutil.copytree(template, folder)  # .gitkeep files keep empty folders tracked
    values = {"{{WP}}": f"WP{number}", "{{TITLE}}": title, "{{TYPE}}": playbook, "{{DATE}}": today(),
              "{{STATUS}}": status, "{{WAITS_FOR}}": waits_for or "none",
              "{{FOLDER}}": folder.relative_to(ROOT).as_posix()}
    for name in ("state.md", "brief.md"):
        text = (folder / name).read_text(encoding="utf-8")
        for key, value in values.items():
            text = text.replace(key, value)
        (folder / name).write_text(text, encoding="utf-8")
    return folder


def cmd_init(a):
    if PROJECT.exists():
        sys.exit("project/ already exists. One project per repository.")
    template = TEAM / "project-template"
    if not template.exists():
        sys.exit("project-template/ is missing.")
    need_playbook(a.type)
    shutil.copytree(template, PROJECT, ignore=shutil.ignore_patterns("wp-template"))
    state = STATE.read_text(encoding="utf-8")
    state = state.replace("{{PROJECT}}", a.name).replace("{{DATE}}", today())
    STATE.write_text(state, encoding="utf-8")
    folder = create_wp(a.wp_title or a.name, a.type, "active")
    print(f"project/ created for '{a.name}'. First work package: {folder.relative_to(ROOT).as_posix()} "
          f"({a.type} playbook)")


def cmd_wp_add(a):
    need_project()
    need_playbook(a.type)
    problem = ref_is_lead_decision(a.ref, read_rows())
    if problem:
        sys.exit(f"Cannot add a work package: {problem}. Adding one changes scope, so it needs the lead's answer first.")
    if a.waits_for and not re.search(r"\bWP\d+\b", a.waits_for):
        sys.exit("--waits-for names the work package waited for and what is needed from it, e.g. \"WP1 evidence file\".")
    folder = create_wp(a.title, a.type, "planned", a.waits_for)
    print(f"{folder.relative_to(ROOT).as_posix()} created ({a.type} playbook), approved under {a.ref}")


def cmd_wp_list(a):
    need_project()
    print(wp_table(md=a.md) or "No work packages yet.")


def cmd_status(a):
    need_project()
    print(STATE.read_text(encoding="utf-8").strip())
    print()
    print("Work packages, in the order of work:")
    print(wp_table() or "none yet")
    print()
    open_memos = [p.stem for p in memo_paths() if memo_status(p) == "open"]
    print(f"Open memos: {', '.join(open_memos) if open_memos else 'none'}")
    tags = tags_in_order()
    print(f"Last checkpoint: {tags[-1] if tags else 'none yet'}")
    rows = read_rows()
    print(f"Decisions logged: {len(rows)}")
    if COMMENTS.exists():
        counts = Counter(r["status"] for r in read_comments())
        if counts:
            print("Comments: " + ", ".join(f"{counts[s]} {s}" for s in ("open", "approved", "done", "not applied") if counts[s]))
    if SENT.exists():
        sent = read_sent()
        if sent:
            last = sent[-1]
            print(f"Last sent: {last['id']} {last['date']} {last['version'] or last['file']} to {last['recipients']}")
    stated = results_outcomes()
    if stated:
        logged = Counter(r["outcome"] for r in (read_outcomes() if OUTCOMES.exists() else []))
        print("Outcomes: " + ", ".join(f"{o} ({logged[o]} observed)" for o in stated))
    digests = health_digests()
    if digests:
        m = re.search(r"Overall:\s*(\w+)", digests[-1].read_text(encoding="utf-8"))
        print(f"Last health check: {digests[-1].stem}, {m.group(1).lower() if m else 'overall not stated'}")


# ---------- CLI ----------

def main():
    p = argparse.ArgumentParser(description="Agent Team helper")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init", help="create project/ from the template, with its first work package")
    s.add_argument("--name", required=True, help="the project's name")
    s.add_argument("--type", required=True, help="playbook of the first work package, e.g. concept-note")
    s.add_argument("--wp-title", default="", help="title of the first work package; the project's name if not given")
    s.set_defaults(func=cmd_init)

    wpc = sub.add_parser("wp", help="work packages").add_subparsers(dest="wcmd", required=True)
    s = wpc.add_parser("add", help="create the next work package, after the lead has approved it")
    s.add_argument("--title", required=True)
    s.add_argument("--type", required=True, help="playbook name, e.g. concept-note")
    s.add_argument("--ref", required=True, help="the decided memo (EM-NNN) or approved decision (D-NNN) that holds the lead's approval")
    s.add_argument("--waits-for", default="", help='what it waits for from another work package, e.g. "WP1 evidence file"')
    s.set_defaults(func=cmd_wp_add)
    s = wpc.add_parser("list", help="the work packages in the order of work")
    s.add_argument("--md", action="store_true", help="print a Markdown table")
    s.set_defaults(func=cmd_wp_list)

    reg = sub.add_parser("register", help="decision register").add_subparsers(dest="rcmd", required=True)
    s = reg.add_parser("add")
    s.add_argument("--stage", required=True)
    s.add_argument("--decision", required=True, help="the question, in one line")
    s.add_argument("--options", required=True, help="options considered, separated by semicolons")
    s.add_argument("--choice", required=True)
    s.add_argument("--reason", required=True)
    s.add_argument("--evidence", default="")
    s.add_argument("--by", required=True, help="agent role or person's name")
    s.add_argument("--reversible", required=True, choices=["yes", "no"])
    s.add_argument("--escalated", default="", help="memo id, e.g. EM-002")
    s.add_argument("--status", default="approved", choices=["proposed", "approved"])
    s.add_argument("--date", default="")
    s.add_argument("--wp", default="", help="work package, e.g. WP2, or project; not needed when the project has one work package")
    s.set_defaults(func=cmd_register_add)
    s = reg.add_parser("set")
    s.add_argument("--id", required=True)
    s.add_argument("--status")
    s.add_argument("--escalated")
    s.add_argument("--choice")
    s.add_argument("--reason")
    s.set_defaults(func=cmd_register_set)
    s = reg.add_parser("reverse")
    s.add_argument("--id", required=True, help="the decision being reversed")
    s.add_argument("--by", required=True, help="the new decision that replaces it")
    s.set_defaults(func=cmd_register_reverse)
    s = reg.add_parser("check")
    s.set_defaults(func=cmd_register_check)
    s = reg.add_parser("show")
    s.add_argument("--wp", default="", help="only this work package, or project")
    s.add_argument("--stage")
    s.add_argument("--search")
    s.add_argument("--md", action="store_true", help="print the whole register as a Markdown page, newest first")
    s.set_defaults(func=cmd_register_show)

    com = sub.add_parser("comment", help="comment log").add_subparsers(dest="ccmd", required=True)
    s = com.add_parser("add", help="log one comment received on the work")
    s.add_argument("--text", required=True, help="the comment or edit, as received")
    s.add_argument("--reviewer", default="", help="who made it (initials or name)")
    s.add_argument("--round", default="", help="review round, e.g. R1 or DOH-2026-10")
    s.add_argument("--source-ref", default="", help="the reviewer's own number, e.g. DOH D-083 or C12")
    s.add_argument("--location", default="")
    s.add_argument("--type", default="", help="comment, tracked edit, untracked edit, finding")
    s.add_argument("--tier", default="", help="A, B, C or closed")
    s.add_argument("--proposed-response", default="")
    s.add_argument("--proposed-action", default="", help=", ".join(sorted(ACTIONS)))
    s.add_argument("--wp", default="", help="work package, e.g. WP2, or project; not needed when the project has one work package")
    s.set_defaults(func=cmd_comment_add)
    s = com.add_parser("import", help="log many comments from a CSV with comment-log column names")
    s.add_argument("--file", required=True)
    s.add_argument("--round", default="")
    s.add_argument("--reviewer", default="")
    s.add_argument("--wp", default="", help="work package, e.g. WP2, or project; not needed when the project has one work package")
    s.set_defaults(func=cmd_comment_import)
    s = com.add_parser("set", help="update proposed response, tier, outcome or status")
    s.add_argument("--id")
    s.add_argument("--ids", help="several ids, comma-separated")
    s.add_argument("--tier", default="")
    s.add_argument("--location", default="")
    s.add_argument("--source-ref", default="")
    s.add_argument("--proposed-response", default="")
    s.add_argument("--proposed-action", default="")
    s.add_argument("--outcome", default="", help="what was done and where, or why not applied")
    s.add_argument("--status", default="", help="open, done or not applied")
    s.set_defaults(func=cmd_comment_set)
    s = com.add_parser("approve", help="record the lead's approval of proposed actions")
    s.add_argument("--ref", required=True, help="the decided memo (EM-NNN) or approved decision (D-NNN)")
    s.add_argument("--ids", help="comma-separated ids")
    s.add_argument("--all-proposed", action="store_true", help="every open comment with a proposed action")
    s.add_argument("--action", default="", help="the lead's action, when it differs from the proposed one")
    s.set_defaults(func=cmd_comment_approve)
    s = com.add_parser("show")
    s.add_argument("--id")
    s.add_argument("--wp", default="", help="only this work package, or project")
    s.add_argument("--status")
    s.add_argument("--tier")
    s.add_argument("--round")
    s.add_argument("--reviewer")
    s.add_argument("--search")
    s.add_argument("--md", action="store_true", help="print a Markdown table, e.g. for a memo or a response matrix")
    s.set_defaults(func=cmd_comment_show)
    s = com.add_parser("check")
    s.set_defaults(func=cmd_comment_check)

    snt = sub.add_parser("sent", help="sent log").add_subparsers(dest="scmd", required=True)
    s = snt.add_parser("add", help="record a version a person sent, and store an exact copy")
    s.add_argument("--file", required=True, help="the exact file that was sent")
    s.add_argument("--to", required=True, help="recipients")
    s.add_argument("--purpose", required=True, help="e.g. co-author review, submission, clearance")
    s.add_argument("--by", required=True, help="the person who sent it")
    s.add_argument("--version", default="")
    s.add_argument("--date", default="")
    s.add_argument("--note", default="")
    s.add_argument("--no-copy", default="", metavar="REASON",
                   help="log the checksum only, without storing a copy, for a file that must not be committed")
    s.add_argument("--wp", default="", help="work package, e.g. WP2; not needed when the project has one")
    s.set_defaults(func=cmd_sent_add)
    s = snt.add_parser("list")
    s.set_defaults(func=cmd_sent_list)
    s = snt.add_parser("compare", help="compare a returned file with the copy that was sent")
    s.add_argument("--id", required=True, help="sent version, e.g. S-002")
    s.add_argument("--file", required=True, help="the returned file")
    s.add_argument("--out", default="", help="write the report here, e.g. <work package folder>/reviews/returned-S-002.md")
    s.set_defaults(func=cmd_sent_compare)

    out = sub.add_parser("outcome", help="outcome log (core/results-chain.md)").add_subparsers(dest="ocmd", required=True)
    s = out.add_parser("add", help="log one observed sign that an outcome in project/results.md happened")
    s.add_argument("--outcome", required=True, help="the outcome in project/results.md, e.g. O1")
    s.add_argument("--observed", required=True, help="what was observed, in one sentence")
    s.add_argument("--source", required=True, help="the file, link or message that shows it")
    s.add_argument("--by", required=True, help="who reported it")
    s.add_argument("--other-factors", required=True,
                   help="other factors that may explain what was observed, or 'none identified'")
    s.add_argument("--date", default="", help="the date it was observed; today if not given")
    s.set_defaults(func=cmd_outcome_add)
    s = out.add_parser("show", help="each stated outcome with what has been observed")
    s.add_argument("--outcome", default="")
    s.add_argument("--md", action="store_true", help="print the log as a Markdown table")
    s.set_defaults(func=cmd_outcome_show)

    s = sub.add_parser("checkpoint", help="commit and tag the current state")
    s.add_argument("--stage", required=True)
    s.add_argument("--message", default="")
    s.add_argument("--no-export", default="", metavar="REASON",
                   help="skip the export check for an external master copy, with the reason")
    s.add_argument("--wp", default="", help="work package, e.g. WP2, or project; not needed when the project has one work package")
    s.set_defaults(func=cmd_checkpoint)

    s = sub.add_parser("rollback", help="restore one work package's work/ folder to a checkpoint")
    s.add_argument("--to", required=True)
    s.add_argument("--reason", required=True)
    s.add_argument("--by", required=True)
    s.add_argument("--wp", default="", help="the work package to restore; taken from the checkpoint name if not given")
    s.set_defaults(func=cmd_rollback)

    memo = sub.add_parser("memo", help="decision memos").add_subparsers(dest="mcmd", required=True)
    s = memo.add_parser("new")
    s.add_argument("--issue", required=True)
    s.add_argument("--urgent", action="store_true")
    s.add_argument("--wp", default="", help="work package, e.g. WP2, or project; not needed when the project has one work package")
    s.set_defaults(func=cmd_memo_new)
    s = memo.add_parser("list")
    s.add_argument("--open", action="store_true")
    s.set_defaults(func=cmd_memo_list)
    s = memo.add_parser("close")
    s.add_argument("--id", required=True)
    s.add_argument("--decision", required=True, help="the lead's answer, in their words")
    s.add_argument("--by", required=True)
    s.set_defaults(func=cmd_memo_close)

    s = sub.add_parser("health", help="weekly health check facts (core/learning-and-oversight.md)")
    s.add_argument("--due", action="store_true", help="only say whether a health check is due today")
    s.add_argument("--out", default="", help="write the facts here, e.g. project/health/2026-11-16-facts.md")
    s.add_argument("--today", default="", help=argparse.SUPPRESS)
    s.set_defaults(func=cmd_health)

    s = sub.add_parser("status", help="print project status")
    s.set_defaults(func=cmd_status)

    a = p.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
