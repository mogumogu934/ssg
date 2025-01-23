import unittest
from page_generator import extract_title

class TestMain(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# Hello"
        result = extract_title(markdown)
        expected = "Hello"
        self.assertEqual(result, expected)
    