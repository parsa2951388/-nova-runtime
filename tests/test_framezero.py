import contextlib
import io
import unittest
from unittest.mock import patch

from framezero import (
    APP_NAME,
    APP_VERSION,
    main,
    parse_version,
    version_at_least,
)


class VersionParsingTests(unittest.TestCase):
    def test_plain_semver(self):
        self.assertEqual(parse_version("8.0.404"), (8, 0, 404))

    def test_version_in_tool_output(self):
        self.assertEqual(parse_version("LLVM version 21.1.3 (release build)"), (21, 1, 3))

    def test_two_component_version(self):
        self.assertEqual(parse_version("Python 3.12"), (3, 12, 0))

    def test_missing_version(self):
        self.assertIsNone(parse_version(None))
        self.assertIsNone(parse_version("version unavailable"))

    def test_minimum_version(self):
        self.assertTrue(version_at_least("8.0.1", (8, 0, 0)))
        self.assertFalse(version_at_least("7.4.9", (8, 0, 0)))
        self.assertFalse(version_at_least("not a version", (8, 0, 0)))


class CommandTests(unittest.TestCase):
    def test_version_command(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = main(["--version"])
        self.assertEqual(result, 0)
        self.assertIn(APP_NAME, output.getvalue())
        self.assertIn(APP_VERSION, output.getvalue())

    def test_help_command(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = main(["--help"])
        self.assertEqual(result, 0)
        self.assertIn("framezero.py", output.getvalue())
        self.assertIn("verify", output.getvalue())

    def test_unknown_command_returns_usage_error(self):
        output = io.StringIO()
        with contextlib.redirect_stderr(output):
            result = main(["not-a-command"])
        self.assertEqual(result, 2)
        self.assertIn("unknown command", output.getvalue())

    def test_doctor_json_is_machine_readable(self):
        output = io.StringIO()
        checks = [{"name": "Example", "status": "ready", "detail": "ok"}]
        with patch("framezero.collect_checks", return_value=checks):
            with contextlib.redirect_stdout(output):
                result = main(["doctor", "--json"])
        self.assertEqual(result, 0)
        self.assertIn('"name": "Example"', output.getvalue())

    def test_doctor_reports_missing_requirements(self):
        checks = [{"name": "Engine", "status": "missing", "detail": "not installed"}]
        with patch("framezero.collect_checks", return_value=checks):
            with contextlib.redirect_stdout(io.StringIO()):
                result = main(["doctor"])
        self.assertEqual(result, 1)




class RecursiveSubmoduleTests(unittest.TestCase):
    def test_all_initialized_submodules_are_accepted(self):
        from scripts.verify_upstream import verify_recursive_submodules

        sample = " abc123 engine/leonida\n def456 engine/leonida/third_party/rpf9-explorer"
        with patch("scripts.verify_upstream.run_git", return_value=sample):
            rows = verify_recursive_submodules()
        self.assertEqual(len(rows), 2)

    def test_missing_submodule_is_rejected(self):
        from scripts.verify_upstream import verify_recursive_submodules

        with patch("scripts.verify_upstream.run_git", return_value="-abc123 engine/leonida"):
            with self.assertRaisesRegex(RuntimeError, "not initialized"):
                verify_recursive_submodules()

    def test_mismatched_submodule_is_rejected(self):
        from scripts.verify_upstream import verify_recursive_submodules

        with patch("scripts.verify_upstream.run_git", return_value="+abc123 engine/leonida"):
            with self.assertRaisesRegex(RuntimeError, "different commit"):
                verify_recursive_submodules()

    def test_conflicted_submodule_is_rejected(self):
        from scripts.verify_upstream import verify_recursive_submodules

        with patch("scripts.verify_upstream.run_git", return_value="Uabc123 engine/leonida"):
            with self.assertRaisesRegex(RuntimeError, "conflict"):
                verify_recursive_submodules()

if __name__ == "__main__":
    unittest.main()
