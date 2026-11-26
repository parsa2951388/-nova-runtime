import unittest

from framezero_gui import build_engine_args, build_validation_args


class BuildProfileTests(unittest.TestCase):
    def test_runtime_profile(self):
        self.assertEqual(
            build_engine_args("runtime", "C:/Games/Package", "D:/FRAMEZERO", "E:/work"),
            [
                "build",
                "--game", "C:/Games/Package",
                "--out", "D:/FRAMEZERO",
                "--work", "E:/work",
                "--stages", "check,shaders,runtime",
            ],
        )

    def test_asset_profile(self):
        self.assertEqual(
            build_engine_args("assets", "/games/package", "/framezero/out"),
            [
                "build",
                "--game", "/games/package",
                "--out", "/framezero/out",
                "--stages", "check,assets",
            ],
        )

    def test_full_profile_preserves_upstream_default(self):
        self.assertEqual(
            build_engine_args("full", "/games/package", "/framezero/out"),
            ["build", "--game", "/games/package", "--out", "/framezero/out"],
        )

    def test_invalid_profile_rejected(self):
        with self.assertRaises(ValueError):
            build_engine_args("unknown", "/games/package", "/framezero/out")

    def test_missing_paths_rejected(self):
        with self.assertRaises(ValueError):
            build_engine_args("runtime", "", "/framezero/out")
        with self.assertRaises(ValueError):
            build_engine_args("runtime", "/games/package", "")

    def test_whitespace_path_rejected(self):
        with self.assertRaises(ValueError):
            build_engine_args("runtime", "   ", "/framezero/out")

    def test_validation_does_not_build(self):
        self.assertEqual(
            build_validation_args("/games/package"),
            ["build", "--game", "/games/package", "--check"],
        )

    def test_validation_rejects_empty_path(self):
        with self.assertRaises(ValueError):
            build_validation_args("")


if __name__ == "__main__":
    unittest.main()
