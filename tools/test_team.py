#!/usr/bin/env python3
"""Tests for tools/team.py: work packages, logs, checkpoints, rollback, outcome log and health check.

Standard library only. Each test builds a throwaway git repository with a copy of the team files:

    python3 tools/test_team.py
"""

import csv
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TEAM = Path(__file__).resolve().parent.parent
COPIED = ("tools", "core", "playbooks", "project-template")


class TeamCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        for name in COPIED:
            shutil.copytree(TEAM / name, self.root / name, ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copy(TEAM / "team.config.example.yaml", self.root / "team.config.yaml")
        self.git("init", "-q", "-b", "main", ".")
        self.git("config", "user.email", "test@example.com")
        self.git("config", "user.name", "Test")
        self.git("config", "commit.gpgsign", "false")
        self.git("config", "tag.gpgsign", "false")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "Base")

    def tearDown(self):
        self.tmp.cleanup()

    # ----- helpers

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.root, capture_output=True, text=True, check=True).stdout.strip()

    def team(self, *args, ok=True):
        """Run the tool. Returns its output; fails the test if the exit code is not the one expected."""
        res = subprocess.run([sys.executable, "tools/team.py", *args], cwd=self.root, capture_output=True, text=True)
        out = res.stdout + res.stderr
        if ok:
            self.assertEqual(res.returncode, 0, out)
        else:
            self.assertNotEqual(res.returncode, 0, out)
        return out

    def init(self, wp_title="Concept note"):
        self.team("init", "--name", "Test project", "--type", "concept-note", "--wp-title", wp_title)

    def decide(self, wp="project", by="Lead Name", **extra):
        args = ["register", "add", "--stage", extra.get("stage", "frame"), "--decision", extra.get("decision", "Approve?"),
                "--options", "yes; no", "--choice", "yes", "--reason", "Because.", "--by", by,
                "--reversible", extra.get("reversible", "yes"), "--wp", wp]
        return self.team(*args).strip()

    def second_wp(self):
        ref = self.decide()
        self.team("wp", "add", "--title", "Revised profile", "--type", "revision", "--ref", ref,
                  "--waits-for", "WP1 sign-off")
        return ref

    def rows(self, name):
        with (self.root / "project" / "register" / name).open(newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def wp(self, number):
        return next((self.root / "project" / "wp").glob(f"WP{number}-*"))

    def edit(self, path: Path, old: str, new: str):
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text)
        path.write_text(text.replace(old, new), encoding="utf-8")


class Playbooks(unittest.TestCase):
    def test_every_playbook_has_numbered_stages_with_checkpoints(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("team", TEAM / "tools" / "team.py")
        team = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(team)
        playbooks = sorted(p for p in (TEAM / "playbooks").glob("*.md") if not p.stem.startswith("_"))
        self.assertGreaterEqual(len(playbooks), 4)
        for playbook in playbooks:
            stages = team.playbook_stages(playbook)
            self.assertTrue(stages, playbook.name)
            self.assertEqual([n for n, _, _ in stages], list(range(1, len(stages) + 1)), playbook.name)
            slugs = [slug for _, _, slug in stages if slug]
            self.assertEqual(len(slugs), len(set(slugs)), f"{playbook.name}: checkpoint names repeat")
            self.assertGreaterEqual(len(slugs), len(stages) - 1, f"{playbook.name}: a stage lacks a checkpoint")

    def test_init_accepts_the_new_playbooks(self):
        for name in ("journal-article", "evidence-summary"):
            with self.subTest(name=name):
                case = TeamCase("setUp")
                case.setUp()
                try:
                    case.team("init", "--name", "Test project", "--type", name)
                    state = next((case.root / "project" / "wp").glob("WP1-*")) / "state.md"
                    self.assertIn(f"Type: {name}", state.read_text(encoding="utf-8"))
                finally:
                    case.tearDown()


class InitAndWorkPackages(TeamCase):
    def test_init_creates_the_project_and_wp1(self):
        self.init()
        project = self.root / "project"
        for name in ("state.md", "brief.md", "results.md", "lessons.md", "register/outcomes.csv"):
            self.assertTrue((project / name).exists(), name)
        self.assertFalse((project / "wp-template").exists())
        self.assertFalse((project / "work").exists())
        wp1 = project / "wp" / "WP1-concept-note"
        for name in ("brief.md", "state.md", "work/frozen/.gitkeep", "work/sent/.gitkeep", "reviews/.gitkeep"):
            self.assertTrue((wp1 / name).exists(), name)
        state = (wp1 / "state.md").read_text(encoding="utf-8")
        self.assertIn("Work package: WP1", state)
        self.assertIn("Type: concept-note", state)
        self.assertIn("Status: active", state)
        self.assertNotIn("{{", state + (wp1 / "brief.md").read_text(encoding="utf-8"))
        self.assertIn("Test project", (project / "state.md").read_text(encoding="utf-8"))

    def test_init_refuses_a_second_project_and_an_unknown_playbook(self):
        self.assertIn("No playbook", self.team("init", "--name", "X", "--type", "nothing", ok=False))
        self.init()
        self.assertIn("already exists", self.team("init", "--name", "X", "--type", "concept-note", ok=False))

    def test_wp_add_needs_the_leads_answer(self):
        self.init()
        self.assertIn("not found", self.team("wp", "add", "--title", "Second", "--type", "revision", "--ref", "D-009", ok=False))
        proposed = self.team("register", "add", "--stage", "frame", "--decision", "Add WP2?", "--options", "a; b",
                             "--choice", "a", "--reason", "r", "--by", "coordinator", "--reversible", "yes",
                             "--status", "proposed", "--wp", "project").strip()
        self.assertIn("not approved", self.team("wp", "add", "--title", "Second", "--type", "revision", "--ref", proposed, ok=False))
        self.assertFalse(list((self.root / "project" / "wp").glob("WP2-*")))
        self.team("register", "set", "--id", proposed, "--status", "approved")
        self.team("wp", "add", "--title", "Second output", "--type", "revision", "--ref", proposed)
        state = (self.wp(2) / "state.md").read_text(encoding="utf-8")
        self.assertIn("Status: planned", state)
        self.assertIn("Type: revision", state)

    def test_wp_list_follows_the_order_line(self):
        self.init()
        self.second_wp()
        listed = self.team("wp", "list").splitlines()
        self.assertTrue(listed[0].startswith("WP1") and listed[1].startswith("WP2"))
        self.assertIn("waits for: WP1 sign-off", listed[1])
        self.edit(self.root / "project" / "state.md", "Order: by number", "Order: WP2, WP1")
        listed = self.team("wp", "list").splitlines()
        self.assertTrue(listed[0].startswith("WP2") and listed[1].startswith("WP1"))
        self.assertIn("| WP2 |", self.team("wp", "list", "--md"))


class Logs(TeamCase):
    def test_one_work_package_needs_no_wp_argument(self):
        self.init()
        rid = self.team("register", "add", "--stage", "outline", "--decision", "Q?", "--options", "a; b", "--choice", "a",
                        "--reason", "r", "--by", "writer", "--reversible", "yes").strip()
        self.assertEqual(rid, "D-001")
        self.assertEqual(self.rows("decisions.csv")[0]["work_package"], "WP1")
        self.team("comment", "add", "--text", "Shorten section 2.", "--round", "R1")
        self.assertEqual(self.rows("comments.csv")[0]["work_package"], "WP1")

    def test_several_work_packages_need_the_wp_argument(self):
        self.init()
        self.second_wp()
        out = self.team("register", "add", "--stage", "outline", "--decision", "Q?", "--options", "a; b", "--choice", "a",
                        "--reason", "r", "--by", "writer", "--reversible", "yes", ok=False)
        self.assertIn("--wp", out)
        self.assertEqual(self.decide(wp="wp2-revised-profile", by="writer"), "D-002")
        rows = self.rows("decisions.csv")
        self.assertEqual([r["work_package"] for r in rows], ["project", "WP2"])
        self.assertIn("No work package", self.decide_fails("WP7"))
        shown = self.team("register", "show", "--wp", "WP2")
        self.assertIn("D-002", shown)
        self.assertNotIn("D-001", shown)
        self.assertIn("| D-002 | WP2 |", self.team("register", "show", "--md"))

    def decide_fails(self, wp):
        return self.team("register", "add", "--stage", "s", "--decision", "Q?", "--options", "a; b", "--choice", "a",
                         "--reason", "r", "--by", "writer", "--reversible", "yes", "--wp", wp, ok=False)

    def test_comment_import_takes_the_work_package_from_the_file_or_the_argument(self):
        self.init()
        self.second_wp()
        source = self.root / "comments-in.csv"
        source.write_text("text,work_package\nFirst comment,WP1\nSecond comment,\n", encoding="utf-8")
        self.assertIn("no work package", self.team("comment", "import", "--file", str(source), "--round", "R1", ok=False))
        self.team("comment", "import", "--file", str(source), "--round", "R1", "--wp", "WP2")
        self.assertEqual([r["work_package"] for r in self.rows("comments.csv")], ["WP1", "WP2"])
        self.assertIn("RC-002", self.team("comment", "show", "--wp", "WP2"))
        self.assertNotIn("RC-001", self.team("comment", "show", "--wp", "WP2"))

    def test_sent_copy_is_stored_in_the_work_package(self):
        self.init()
        self.second_wp()
        final = self.wp(2) / "work" / "final.md"
        final.write_text("Final text.\n", encoding="utf-8")
        self.assertIn("--wp", self.team("sent", "add", "--file", str(final), "--to", "Funder", "--purpose", "submission",
                                        "--by", "Lead Name", ok=False))
        self.team("sent", "add", "--file", str(final), "--to", "Funder", "--purpose", "submission",
                  "--by", "Lead Name", "--wp", "WP2", "--date", "2026-11-10")
        row = self.rows("sent.csv")[0]
        self.assertEqual(row["work_package"], "WP2")
        self.assertTrue((self.wp(2) / "work" / "sent" / "2026-11-10_final.md").exists())
        self.assertIn("Register OK", self.team("register", "check"))

    def test_register_check_reports_an_unknown_work_package(self):
        self.init()
        self.decide(wp="WP1")
        path = self.root / "project" / "register" / "decisions.csv"
        path.write_text(path.read_text(encoding="utf-8").replace(",WP1,", ",WP9,"), encoding="utf-8")
        self.assertIn("WP9", self.team("register", "check", ok=False))

    def test_memo_names_its_work_package(self):
        self.init()
        self.second_wp()
        self.team("memo", "new", "--issue", "Gate: approve the outline", "--wp", "WP2")
        self.team("memo", "new", "--issue", "Change the results chain?")
        memos = self.root / "project" / "escalations"
        self.assertIn("Work package: WP2", (memos / "EM-001.md").read_text(encoding="utf-8"))
        self.assertIn("Work package: project", (memos / "EM-002.md").read_text(encoding="utf-8"))
        listed = self.team("memo", "list")
        self.assertRegex(listed, r"EM-001\s+open\s+WP2")


class CheckpointsAndRollback(TeamCase):
    def test_tags_carry_the_work_package(self):
        self.init()
        self.second_wp()
        self.assertIn("cp-project-frame-01", self.team("checkpoint", "--stage", "frame", "--wp", "project"))
        self.assertIn("--wp", self.team("checkpoint", "--stage", "brief", ok=False))
        self.assertIn("cp-wp1-brief-01", self.team("checkpoint", "--stage", "brief", "--wp", "WP1"))
        self.assertIn("cp-wp2-brief-01", self.team("checkpoint", "--stage", "brief", "--wp", "WP2"))
        self.assertIn("cp-wp1-brief-02", self.team("checkpoint", "--stage", "brief", "--wp", "WP1"))
        self.assertEqual(self.rows("decisions.csv")[0]["checkpoint"], "cp-project-frame-01")

    def test_rollback_restores_one_work_package_only(self):
        self.init()
        self.second_wp()
        draft1, draft2 = self.wp(1) / "work" / "draft.md", self.wp(2) / "work" / "draft.md"
        draft1.write_text("WP1 outline version\n", encoding="utf-8")
        draft2.write_text("WP2 first version\n", encoding="utf-8")
        self.team("checkpoint", "--stage", "outline", "--wp", "WP1")
        draft1.write_text("WP1 later version\n", encoding="utf-8")
        draft2.write_text("WP2 later version\n", encoding="utf-8")
        sent = self.wp(1) / "work" / "sent" / "record.md"
        sent.write_text("A sent copy.\n", encoding="utf-8")
        d_wp1 = self.decide(wp="WP1", by="writer", stage="draft")
        d_wp2 = self.decide(wp="WP2", by="writer", stage="draft")
        self.team("checkpoint", "--stage", "draft", "--wp", "WP1")
        self.team("checkpoint", "--stage", "draft", "--wp", "WP2")
        out = self.team("rollback", "--to", "cp-wp1-outline-01", "--reason", "Wrong direction", "--by", "Lead Name")
        self.assertIn("WP1 work restored", out)
        self.assertEqual(draft1.read_text(encoding="utf-8"), "WP1 outline version\n")
        self.assertEqual(draft2.read_text(encoding="utf-8"), "WP2 later version\n")
        self.assertTrue(sent.exists(), "sent copies are records and stay")
        status = {r["id"]: r for r in self.rows("decisions.csv")}
        self.assertEqual(status[d_wp1]["status"], "rolled back")
        self.assertEqual(status[d_wp2]["status"], "approved")
        last = self.rows("decisions.csv")[-1]
        self.assertEqual((last["stage"], last["work_package"]), ("rollback", "WP1"))
        self.assertIn("Register OK", self.team("register", "check"))

    def test_rollback_to_a_project_checkpoint_needs_a_work_package(self):
        self.init()
        self.team("checkpoint", "--stage", "frame", "--wp", "project")
        out = self.team("rollback", "--to", "cp-project-frame-01", "--reason", "r", "--by", "Lead Name", ok=False)
        self.assertIn("--wp", out)

    def test_external_master_needs_an_export_for_its_own_work_package(self):
        self.init()
        self.second_wp()
        self.edit(self.wp(2) / "state.md", "Master copy: project/wp/WP2-revised-profile/work/",
                  "Master copy: Google Doc https://docs.example.org/d/abc")
        self.team("checkpoint", "--stage", "brief", "--wp", "WP1")
        self.assertIn("outside the repository", self.team("checkpoint", "--stage", "brief", "--wp", "WP2", ok=False))
        (self.wp(2) / "work" / "frozen" / "brief-2026-11-10.docx").write_bytes(b"export")
        self.assertIn("cp-wp2-brief-01", self.team("checkpoint", "--stage", "brief", "--wp", "WP2"))
        self.assertIn("cp-wp2-triage-01",
                      self.team("checkpoint", "--stage", "triage", "--wp", "WP2", "--no-export", "No change to the master"))


class OutcomesAndHealth(TeamCase):
    def state_outcomes(self):
        self.edit(self.root / "project" / "results.md", "## Outputs",
                  "- O1. The funder invites a full proposal. By: 2027-03-31\n"
                  "- O2. The bureau uses the cost estimates. By: 2027-06-30\n\n## Outputs")

    def test_an_outcome_is_logged_only_against_a_stated_outcome_and_with_a_source(self):
        self.init()
        args = ["outcome", "add", "--outcome", "O1", "--observed", "Written invitation received.",
                "--source", "project/sources/invitation.pdf", "--by", "Lead Name",
                "--other-factors", "The funder widened the call in February."]
        self.assertIn("No outcome O1", self.team(*args, ok=False))
        self.state_outcomes()
        self.assertIn("--source is empty", self.team(*[a if a != "project/sources/invitation.pdf" else " " for a in args], ok=False))
        self.assertEqual(self.team(*args, "--date", "2027-03-04").strip(), "OB-001")
        row = self.rows("outcomes.csv")[0]
        self.assertEqual((row["outcome"], row["date"], row["reported_by"]), ("O1", "2027-03-04", "Lead Name"))
        shown = self.team("outcome", "show")
        self.assertIn("OB-001", shown)
        self.assertIn("Nothing observed yet", shown)
        self.assertIn("| OB-001 |", self.team("outcome", "show", "--md"))
        self.assertIn("1 observed outcomes", self.team("register", "check"))

    def test_health_reports_each_work_package_and_the_new_measures(self):
        self.init()
        self.second_wp()
        self.state_outcomes()
        self.edit(self.wp(1) / "brief.md", "- Deadline:", "- Deadline: 2027-01-15")
        self.edit(self.wp(2) / "brief.md", "- Deadline:", "- Deadline: 2027-06-01")
        self.edit(self.wp(2) / "state.md", "Status: planned", "Status: waiting (since 2027-01-05)")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "Frame")

        facts = self.team("health", "--today", "2026-12-01")
        self.assertIn("| WP2 | Revised profile | revision |", facts)
        self.assertIn("| Work packages past their deadline | None | Green |", facts)
        self.assertIn("| Outcomes past their date with nothing observed | None | Green |", facts)
        self.assertIn("WP1: days to deadline per stage left", facts)

        facts = self.team("health", "--today", "2027-01-20")
        self.assertIn("| Work packages past their deadline | WP1, 5 day(s) past | Amber |", facts)
        self.assertIn("| Work packages waiting on another work package | WP2, 15 day(s) | Red |", facts)
        self.assertIn("WP2: waiting 15 day(s) for WP1 sign-off", facts)
        self.assertIn("**Overall: red.**", facts)

        facts = self.team("health", "--today", "2027-04-02")
        self.assertIn("| Outcomes past their date with nothing observed | O1 | Amber |", facts)
        self.team("outcome", "add", "--outcome", "O1", "--observed", "Invitation received.", "--source", "email of 2027-03-04",
                  "--by", "Lead Name", "--other-factors", "none identified")
        facts = self.team("health", "--today", "2027-04-02")
        self.assertIn("| Outcomes past their date with nothing observed | None | Green |", facts)

    def test_signed_off_work_packages_leave_the_pacing_measures(self):
        self.init()
        self.edit(self.wp(1) / "brief.md", "- Deadline:", "- Deadline: 2027-01-15")
        self.edit(self.wp(1) / "state.md", "Status: active", "Status: signed off (2027-01-10)")
        facts = self.team("health", "--today", "2027-02-01")
        self.assertNotIn("WP1: days", facts)
        self.assertIn("| Work packages past their deadline | None | Green |", facts)

    def test_status_lists_work_packages_and_outcomes(self):
        self.init()
        self.state_outcomes()
        out = self.team("status")
        self.assertIn("WP1  Concept note  [concept-note]", out)
        self.assertIn("Outcomes: O1 (0 observed), O2 (0 observed)", out)


if __name__ == "__main__":
    unittest.main()
