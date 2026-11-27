"""Integration checks against real, disposable Git histories; no research inputs."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

GUARD = Path(__file__).resolve().parents[1] / "scripts/check_publication.py"


class PublicationGuardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.git("init", "--quiet", "--initial-branch=main")
        self.git("config", "user.name", "Publication guard test")
        self.git("config", "user.email", "publication-test@example.invalid")
        self.git("config", "commit.gpgsign", "false")
        self.git("config", "core.autocrlf", "false")
        self.write("README.md", "Reviewed main README\n")
        self.freeze("etude_final")
        self.main_base = self.record("reviewed main")
        self.main_blob = self.git("rev-parse", "HEAD:README.md")
        self.git("checkout", "--quiet", "-b", "audit-2026-11-03")
        self.write("README.md", "Reviewed audit README\n")
        self.freeze("etude_groupe")
        self.audit_base = self.record("reviewed audit")
        self.audit_blob = self.git("rev-parse", "HEAD:README.md")
        self.git("checkout", "--quiet", "main")
        self.git("update-ref", "refs/remotes/origin/main", self.main_base)
        self.git("update-ref", "refs/remotes/origin/audit-2026-11-03", self.audit_base)
        (self.repo / "scripts").mkdir(exist_ok=True)
        shutil.copyfile(GUARD, self.repo / "scripts/check_publication.py")
        self.policy = {"version": 1, "targets": {
            "main": {"baseline_commit": self.main_base, "readme_blob": self.main_blob,
                     "protocol_locks": ["etude_final/PROTOCOL.lock"]},
            "audit-2026-11-03": {"baseline_commit": self.audit_base,
                     "readme_blob": self.audit_blob,
                     "protocol_locks": ["etude_final/PROTOCOL.lock", "etude_groupe/PROTOCOL.lock"]}}}
        self.save_policy()

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.repo), *args], check=True,
                              capture_output=True, text=True).stdout.strip()

    def write(self, name, text):
        file = self.repo / name
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(text)

    def freeze(self, study):
        content = b"Immutable research input\n"
        self.write(f"{study}/frozen.txt", content.decode())
        self.write(f"{study}/PROTOCOL.lock", json.dumps({
            "fichiers": {"frozen.txt": hashlib.sha256(content).hexdigest()}}))

    def record(self, message):
        self.git("add", "--all")
        self.git("commit", "--quiet", "-m", message)
        return self.git("rev-parse", "HEAD")

    def save_policy(self):
        self.write("state/publication_baselines.json", json.dumps(self.policy))

    def check(self, target="main", extra=()):
        return subprocess.run([sys.executable, str(self.repo / "scripts/check_publication.py"),
                               "--target", target, *extra], capture_output=True, text=True)

    def rejected(self, target="main", text=None, extra=()):
        result = self.check(target, extra)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        if text:
            self.assertIn(text, result.stderr)

    def test_new_research_commit_is_allowed(self):
        self.write("research/new_case/README.md", "A new case, no previous evidence overwritten\n")
        self.write("research/new_case/result.json", '{"status": "unresolved"}\n')
        self.record("add separate research")
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_audit_uses_its_own_readme_and_both_locks(self):
        self.git("checkout", "--quiet", "audit-2026-11-03")
        result = self.check("audit-2026-11-03")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("2 frozen files", result.stdout)
        self.rejected("main", "Committed file changed")

    def test_committed_readme_replacement_is_rejected(self):
        self.write("README.md", "Old session overwrote the overview\n")
        self.record("replace overview")
        self.rejected(text="Committed file changed")

    def test_deleted_readme_is_rejected(self):
        (self.repo / "README.md").unlink()
        self.record("delete overview")
        self.rejected(text="Committed file changed")

    def test_working_readme_edit_is_rejected(self):
        self.write("README.md", "Uncommitted replacement\n")
        self.rejected(text="Working file changed")

    def test_index_change_cannot_hide_behind_a_restored_working_readme(self):
        self.write("README.md", "Staged replacement\n")
        self.git("add", "README.md")
        self.write("README.md", "Reviewed main README\n")
        self.rejected(text="Index file changed")

    def test_absent_correction_commit_fails(self):
        self.policy["targets"]["main"]["baseline_commit"] = "1" * 40
        self.save_policy()
        self.rejected(text="rev-parse")

    def test_present_but_unrelated_correction_commit_fails(self):
        orphan = self.git("commit-tree", self.git("rev-parse", "HEAD^{tree}"),
                          "-m", "unrelated correction")
        self.policy["targets"]["main"]["baseline_commit"] = orphan
        self.save_policy()
        self.rejected(text="Required correction")

    def test_missing_target_ref_fails(self):
        self.git("update-ref", "-d", "refs/remotes/origin/main")
        self.rejected(text="rev-parse")

    def test_unintegrated_target_tip_fails(self):
        self.write("remote_update.txt", "Another session's accepted change\n")
        newer = self.record("advance target")
        self.git("update-ref", "refs/remotes/origin/main", newer)
        self.git("checkout", "--quiet", "--detach", self.main_base)
        # The guard itself was committed in the newer tip, so restore only test tooling.
        (self.repo / "scripts").mkdir(exist_ok=True)
        shutil.copyfile(GUARD, self.repo / "scripts/check_publication.py")
        self.save_policy()
        self.rejected(text="Fetched target")

    def test_explicit_ci_event_base_is_checked(self):
        result = self.check(extra=("--target-ref", self.main_base))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.rejected(extra=("--target-ref", "2" * 40), text="rev-parse")

    def test_frozen_content_and_lock_cannot_be_rewritten_together(self):
        self.write("etude_final/frozen.txt", "Changed result\n")
        self.write("etude_final/PROTOCOL.lock", json.dumps({"fichiers": {
            "frozen.txt": hashlib.sha256(b"Changed result\n").hexdigest()}}))
        self.record("rewrite result and hash")
        self.rejected(text="Committed file changed")

    def test_frozen_file_cannot_redirect_to_another_frozen_file(self):
        self.git("checkout", "--quiet", "audit-2026-11-03")
        frozen = self.repo / "etude_final/frozen.txt"
        frozen.unlink()
        frozen.symlink_to("../etude_groupe/frozen.txt")
        self.record("substitute frozen file with a link to identical content")
        self.rejected("audit-2026-11-03", "Committed file changed")

    def test_target_argument_is_required(self):
        result = subprocess.run([sys.executable, str(self.repo / "scripts/check_publication.py")],
                                capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--target", result.stderr)


if __name__ == "__main__":
    unittest.main()
