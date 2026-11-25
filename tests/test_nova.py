import unittest

from nova import parse_version, version_at_least


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


if __name__ == "__main__":
    unittest.main()
