import unittest
from htmlnode import HTMLNode

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
        
if __name__ == "__main__":
    unittest.main()
