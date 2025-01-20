import unittest
from textnode import TextNode, TextType, text_node_to_html_node, text_to_textnodes
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestTextNode(unittest.TestCase):
    def test_equal(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)
        
    def test_unequal_text_type(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node1, node2)
        
    def test_unequal_text(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is not a text node", TextType.BOLD)
        self.assertNotEqual(node1, node2)
        
    def test_unequal_url(self):
        node1 = TextNode("This is a text node", TextType.BOLD, "https://www.textnode.net")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node1, node2)
        
    def test_unequal_text_type_and_url(self):
        node1 = TextNode("This is a text node", TextType.BOLD, "https://www.textnode.net")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://www.notatextnode.net")
        self.assertNotEqual(node1, node2)
        
    def test_text_node_to_html_node_text(self):
        text_node = TextNode("the text", TextType.TEXT)
        self.assertEqual(text_node_to_html_node(text_node), LeafNode(None, "the text"))
    
    def test_text_node_to_html_node_bold(self):
        text_node = TextNode("the text", TextType.BOLD)
        self.assertEqual(text_node_to_html_node(text_node), LeafNode("b", "the text"))
        
    def test_text_node_to_html_node_italic(self):
        text_node = TextNode("the text", TextType.ITALIC)
        self.assertEqual(text_node_to_html_node(text_node), LeafNode("i", "the text"))
        
    def test_text_node_to_html_node_code(self):
        text_node = TextNode("the text", TextType.CODE)
        self.assertEqual(text_node_to_html_node(text_node), LeafNode("code", "the text"))
        
    def test_text_node_to_html_node_link(self):
        text_node = TextNode("click here", TextType.LINK, "https://www.leafnode.net")
        self.assertEqual(text_node_to_html_node(text_node), LeafNode("a", "click here", {"href": "https://www.leafnode.net"}))
        
    def test_text_node_to_html_node_image(self):
        text_node = TextNode("cute puppy", TextType.IMAGE, "https://www.cutepuppy.net")
        self.assertEqual(text_node_to_html_node(text_node), LeafNode("img", "", {"src": "https://www.cutepuppy.net", "alt": "cute puppy"}))
        
    def test_text_node_to_html_node_invalid(self):
        text_node = TextNode("the text", "not an enum", "https://www.leafnode.net")
        with self.assertRaises(Exception):
            text_node_to_html_node(text_node)
        
    def test_text_to_textnodes(self):
        text = "This is text with a **bold** word, an *italic* word, a `code block`, an ![image of a cat](https://i.imgur.com/cat.jpeg), and a [link](https://www.okayu.net)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word, an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word, a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(", an ", TextType.TEXT),
            TextNode("image of a cat", TextType.IMAGE, "https://i.imgur.com/cat.jpeg"),
            TextNode(", and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.okayu.net"),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_empty_input(self):
        text = ""
        result = text_to_textnodes(text)
        expected = []
        self.assertEqual(result, expected)
        
    def test_text_to_textnodes_no_markdown(self):
        text = "plain text"
        result = text_to_textnodes(text)
        expected = [TextNode("plain text", TextType.TEXT)]
        self.assertEqual(result, expected)
        
    def test_text_to_textnodes_adjacent_markdown(self):
        text = "**bold**__italic__"
        result = text_to_textnodes(text)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC), 
        ]
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
