import unittest
from htmlnode import HTMLNode
from markdown import markdown_to_blocks, block_to_block_type, markdown_to_html_node

class TestMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = "# This is the heading\n\nThis is a paragraph of text that has **bold** and *italic* words in it.\n\n* First item\n* Second item\n* Third item\n\n"
        result = markdown_to_blocks(markdown)
        expected = ["# This is the heading", "This is a paragraph of text that has **bold** and *italic* words in it.", "* First item\n* Second item\n* Third item"]
        self.assertEqual(result, expected)
        
    def test_block_to_block_type_heading(self):
        markdown_block = "#### heading"
        result = block_to_block_type(markdown_block)
        expected = "HEADING"
        self.assertEqual(result, expected)
        
    def test_block_to_block_type_code(self):
        markdown_block = "```code```"
        result = block_to_block_type(markdown_block)
        expected = "CODE"
        self.assertEqual(result, expected)
        
    def test_block_to_block_type_quote(self):
        markdown_block = ">quote 1\n>quote 2\n>quote 3"
        result = block_to_block_type(markdown_block)
        expected = "QUOTE"
        self.assertEqual(result, expected)
        
    def test_block_to_block_type_unordered_list(self):
        markdown_block = "* First item\n* Second item\n* Third item"
        result = block_to_block_type(markdown_block)
        expected = "UNORDERED LIST"
        self.assertEqual(result, expected)
        
    def test_block_to_block_type_ordered_list(self):
        markdown_block = "1. First item\n2. Second item\n3. Third item"
        result = block_to_block_type(markdown_block)
        expected = "ORDERED LIST"
        self.assertEqual(result, expected)
        
    def test_block_to_block_type_paragraph(self):
        markdown_block = "This is a paragraph of text."
        result = block_to_block_type(markdown_block)
        expected = "PARAGRAPH"
        self.assertEqual(result, expected)
        
    def test_markdown_to_html_node(self):
        markdown_document = "# Heading 1\n\n```\nCode block\n```\n\n>Quote\n\n* Item 1\n* Item 2\n\n1. Item 1\n2. Item 2"
        result = markdown_to_html_node(markdown_document)
        expected = HTMLNode("div", "", [
            HTMLNode("h1", "Heading 1"),
            HTMLNode("pre", "", [HTMLNode("code", "Code block")]),
            HTMLNode("blockquote", "Quote"),
            HTMLNode("ul", "", [
                HTMLNode("li", "Item 1"),
                HTMLNode("li", "Item 2")
            ]),
            HTMLNode("ol", "", [
                HTMLNode("li", "Item 1"),
                HTMLNode("li", "Item 2"),
    ])
])
        self.assertEqual(result, expected)
        
if __name__ == "__main__":
    unittest.main()
