import unittest
from pathlib import Path

from nova_gui import build_engine_args, build_validation_args


class LegacyEntryPointTests(unittest.TestCase):
    def test_legacy_gui_shim_uses_framezero_argument_builder(self):
        game = str(Path("C:/Games/Package").expanduser())
        output = str(Path("D:/FRAMEZERO").expanduser())
        self.assertEqual(
            build_engine_args("full", "C:/Games/Package", "D:/FRAMEZERO"),
            ["build", "--game", game, "--out", output],
        )

    def test_legacy_validation_shim(self):
        game = str(Path("C:/Games/Package").expanduser())
        self.assertEqual(
            build_validation_args("C:/Games/Package"),
            ["build", "--game", game, "--check"],
        )


if __name__ == "__main__":
    unittest.main()
