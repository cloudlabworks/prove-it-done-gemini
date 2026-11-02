import os
import subprocess
import sys
import tempfile
import unittest

SCRIPT = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts", "check_skill_sync.py")
)


class TestCheckSkillSync(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

        self.base_dir = self.temp_dir.name
        self.upstream = os.path.join(self.base_dir, "upstream")
        self.copy = os.path.join(self.base_dir, "skills", "prove-it-done")

        os.makedirs(self.upstream)
        os.makedirs(self.copy)

        self.original_dir = os.getcwd()
        os.chdir(self.base_dir)
        self.addCleanup(os.chdir, self.original_dir)

        self.script = SCRIPT

    def write_file(self, directory, path, content):
        full_path = os.path.join(directory, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, "w", encoding="utf-8") as file:
            file.write(content)

    def run_check(self, *args):
        return subprocess.run(
            [sys.executable, self.script, *args],
            capture_output=True,
            text=True,
            cwd=self.base_dir,
        )

    def test_clean_copy(self):
        self.write_file(self.upstream, "SKILL.md", "same content")
        self.write_file(self.copy, "SKILL.md", "same content")

        result = self.run_check(self.upstream)

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")

    def test_differs(self):
        self.write_file(self.upstream, "SKILL.md", "upstream content")
        self.write_file(self.copy, "SKILL.md", "different content")

        result = self.run_check(self.upstream)

        self.assertEqual(result.returncode, 1)
        self.assertIn("DIFFERS SKILL.md", result.stdout)

    def test_missing_upstream(self):
        self.write_file(self.copy, "extra.txt", "extra")

        result = self.run_check(self.upstream)

        self.assertEqual(result.returncode, 1)
        self.assertIn("MISSING-UPSTREAM extra.txt", result.stdout)

    def test_missing_here(self):
        self.write_file(self.upstream, "SKILL.md", "content")

        result = self.run_check(self.upstream)

        self.assertEqual(result.returncode, 1)
        self.assertIn("MISSING-HERE SKILL.md", result.stdout)

    def test_usage_error(self):
        result = self.run_check()

        self.assertEqual(result.returncode, 2)
        self.assertIn("Usage:", result.stdout)

    def test_invalid_directory(self):
        result = self.run_check(
            os.path.join(self.base_dir, "does-not-exist")
        )

        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
