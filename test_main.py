import unittest
import main
from available_langs import LANGUAGES


class TestMain(unittest.TestCase):
    def test_get_lang_key(self):
        self.assertEqual(main.get_lang_key(LANGUAGES, 'russian'), 'ru')
        self.assertEqual(main.get_lang_key(LANGUAGES, 'unknown'), "No such a key")
