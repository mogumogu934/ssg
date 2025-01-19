import unittest
from textnode import TextNode, TextType, text_node_to_html_node
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
        
if __name__ == "__main__":
    unittest.main()
