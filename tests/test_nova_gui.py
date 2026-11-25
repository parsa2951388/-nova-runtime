import unittest

from nova_gui import build_engine_args, build_validation_args


class BuildProfileTests(unittest.TestCase):
    def test_runtime_profile(self):
        self.assertEqual(
            build_engine_args("runtime", "C:/Games/Package", "D:/NOVA", "E:/work"),
            [
                "build",
                "--game", "C:/Games/Package",
                "--out", "D:/NOVA",
                "--work", "E:/work",
                "--stages", "check,shaders,runtime",
            ],
        )

    def test_asset_profile(self):
        self.assertEqual(
            build_engine_args("assets", "/games/package", "/nova/out"),
            [
                "build",
                "--game", "/games/package",
                "--out", "/nova/out",
                "--stages", "check,assets",
            ],
        )

    def test_full_profile_preserves_upstream_default(self):
        self.assertEqual(
            build_engine_args("full", "/games/package", "/nova/out"),
            ["build", "--game", "/games/package", "--out", "/nova/out"],
        )

    def test_invalid_profile_rejected(self):
        with self.assertRaises(ValueError):
            build_engine_args("unknown", "/games/package", "/nova/out")

    def test_missing_paths_rejected(self):
        with self.assertRaises(ValueError):
            build_engine_args("runtime", "", "/nova/out")
        with self.assertRaises(ValueError):
            build_engine_args("runtime", "/games/package", "")

    def test_validation_does_not_build(self):
        self.assertEqual(
            build_validation_args("/games/package"),
            ["build", "--game", "/games/package", "--check"],
        )


if __name__ == "__main__":
    unittest.main()
