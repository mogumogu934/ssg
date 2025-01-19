import unittest
from delimiter import InvalidMarkdownSyntaxError, split_nodes_delimiter
from textnode import TextNode, TextType

class TestDelimiter(unittest.TestCase):
    def test_delimiter_italic(self):
        old_nodes = [TextNode("This is text with an *italic delimiter*", TextType.TEXT)]
        expected_nodes = split_nodes_delimiter(old_nodes, "*", TextType.ITALIC)
        new_nodes = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic delimiter", TextType.ITALIC),
        ]
        self.assertEqual(expected_nodes, new_nodes)
        
    def test_delimiter_italic_multiple(self):
        old_nodes = [TextNode("*This* is *text* with an *italic delimiter*", TextType.TEXT)]
        expected_nodes = split_nodes_delimiter(old_nodes, "*", TextType.ITALIC)
        new_nodes = [
            TextNode("This", TextType.ITALIC),
            TextNode(" is ", TextType.TEXT),
            TextNode("text", TextType.ITALIC),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic delimiter", TextType.ITALIC),
        ]
        self.assertEqual(expected_nodes, new_nodes)

    def test_delimiter_bold(self):
        old_nodes = [TextNode("This is text with a **bold delimiter**", TextType.TEXT)]
        expected_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        new_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold delimiter", TextType.BOLD),
        ]
        self.assertEqual(expected_nodes, new_nodes)

    def test_delimiter_unmatched(self):
        old_nodes = [TextNode("This is text with a **bold delimiter", TextType.TEXT)]
        new_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold delimiter", TextType.BOLD),
        ]
        with self.assertRaises(InvalidMarkdownSyntaxError):
            split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

    def test_delimiter_two_types_and_empty_text(self):
        old_nodes = [
            TextNode("This is *text* with a **bold delimiter** and an *italic delimiter*", TextType.TEXT),
            TextNode("", TextType.TEXT)
            ]
        expected_nodes_1 = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        expected_nodes_2 = split_nodes_delimiter(expected_nodes_1, "*", TextType.ITALIC)
        new_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.ITALIC),
            TextNode(" with a ", TextType.TEXT),
            TextNode("bold delimiter", TextType.BOLD),
            TextNode(" and an ", TextType.TEXT),
            TextNode("italic delimiter", TextType.ITALIC),
        ]
        self.assertEqual(expected_nodes_2, new_nodes)
        
if __name__ == "__main__":
    unittest.main()
