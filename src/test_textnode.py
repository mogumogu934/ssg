import unittest
from textnode import TextNode, TextType

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
        
if __name__ == "__main__":
    unittest.main()
