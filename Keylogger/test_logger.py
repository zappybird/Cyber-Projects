import unittest
import os
import tempfile
from datetime import datetime
from logger import key_pressed, rotate_file_if_needed
from pynput.keyboard import Key

class TestLogger(unittest.TestCase):

    def test_key_pressed_character(self):
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            path = tmp.name

        # Patch KEYLOG_FILE
        from logger import KEYLOG_FILE
        original = KEYLOG_FILE
        try:
            import logger
            logger.KEYLOG_FILE = path

            key_pressed(type("K", (), {"char": "a"}))
            with open(path, "r") as f:
                data = f.read()
            self.assertIn("a", data)
        finally:
            logger.KEYLOG_FILE = original
            os.remove(path)

    def test_key_pressed_special(self):
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            path = tmp.name

        from logger import KEYLOG_FILE
        original = KEYLOG_FILE
        try:
            import logger
            logger.KEYLOG_FILE = path

            key_pressed(Key.space)
            with open(path, "r") as f:
                data = f.read()
            self.assertIn("<Key.space>", data)
        finally:
            logger.KEYLOG_FILE = original
            os.remove(path)

if __name__ == "__main__":
    unittest.main()
