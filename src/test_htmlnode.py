import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_no_props(self):
        node = HTMLNode("p", "the text", "child", None)
        self.assertEqual(node.props_to_html(), "")

    def test_one_prop(self):
        node = HTMLNode(None, "the text", "child", props = {"href": "https://www.htmlnode.net"})
        self.assertEqual(node.props_to_html(), ' href="https://www.htmlnode.net"')
        
    def test_three_props(self):
        node = HTMLNode("p", "the text", None, props = {"href": "https://www.htmlnode.net", "target": "_blank", "ping": "https://www.ping.net"})
        self.assertEqual(node.props_to_html(), ' href="https://www.htmlnode.net" target="_blank" ping="https://www.ping.net"')
 
        
class TestLeafNode(unittest.TestCase):
    def test_no_value(self):
        node = LeafNode("p", "", props = {"href": "https://www.leafnode.net"})
        with self.assertRaises(ValueError):
            node.to_html()
        
    def test_none_tag(self):
        node = LeafNode(None, "the text", props = {"href": "https://www.leafnode.net"})
        self.assertEqual(node.to_html(), "the text")
    
    def test_none_props(self):
        node = LeafNode("p", "the text", None)
        self.assertEqual(node.to_html(), "<p>the text</p>")
        
    def test_two_props(self):
        node = LeafNode("a", "the text", props = {"href": "https://www.leafnode.net", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="https://www.leafnode.net" target="_blank">the text</a>')
        
if __name__ == "__main__":
    unittest.main()


class TestParentNode(unittest.TestCase):
    def test_none_tag(self):
        node = ParentNode(None, children=[LeafNode("b", "Bold text")], props=None)
        with self.assertRaises(ValueError):
            node.to_html()
            
    def test_no_children(self):
        node = ParentNode("p", children=[], props=None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_none_children(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()
            
    def test_one_child(self):
        node = ParentNode("div", [LeafNode("p", "text")])
        self.assertEqual(node.to_html(), '<div><p>text</p></div>')
    
    def test_valid_case_1(self):
        test_children = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            ParentNode("div", [
                LeafNode("i", "Italic text"),
                LeafNode(None, "More text"),
            ])
        ]
        
        node = ParentNode("p", test_children, props=None)
        self.assertEqual(node.to_html(), '<p><b>Bold text</b>Normal text<div><i>Italic text</i>More text</div></p>')
        
    def test_valid_case_2(self):
        test_children = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            ParentNode("div", [
                LeafNode("i", "Italic text"),
                LeafNode(None, "More text"),
                ParentNode("div", [
                    LeafNode("b", "Bold text"),
                ])
            ])
        ]
        
        node = ParentNode("p", test_children, props=None)
        self.assertEqual(node.to_html(), '<p><b>Bold text</b>Normal text<div><i>Italic text</i>More text<div><b>Bold text</b></div></div></p>')
