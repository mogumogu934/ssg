import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from markdown import markdown_to_blocks, block_to_block_type, process_inline_text, markdown_to_html_node, text_to_children

class TestMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = "# This is the heading\n\nThis is a paragraph of text that has **bold** and *italic* words in it.\n\n* First item\n* Second item\n* Third item\n\n"
        result = markdown_to_blocks(markdown)
        expected = ["# This is the heading", "This is a paragraph of text that has **bold** and *italic* words in it.", "* First item\n* Second item\n* Third item"]
        self.assertEqual(result, expected)
        
    def test_block_to_block_type_heading(self):
        markdown_block = "#### title"
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

    def test_process_inline_text_plain_text(self):
        text = "This is plain text."
        output = process_inline_text(text)
        self.assertEqual(output[0].tag, None)
        self.assertEqual(output[0].value, "This is plain text.")

    def test_process_inline_text_bold_text(self):
        text = "**Bold text**"
        output = process_inline_text(text)
        self.assertEqual(output[0].tag, "b")
        self.assertEqual(output[0].value, "Bold text")

    def test_process_inline_text_italic_text(self):
        text = "*Italic text*"
        output = process_inline_text(text)
        self.assertEqual(output[0].tag, "i")
        self.assertEqual(output[0].value, "Italic text")

    def test_process_inline_text_mixed_text(self):
        text = "**Bold** and *Italic*"
        output = process_inline_text(text)
        self.assertEqual(output[0].tag, "b")
        self.assertEqual(output[0].value, "Bold")
        self.assertEqual(output[2].tag, "i")
        self.assertEqual(output[2].value, "Italic")
        
    def test_process_inline_text_link_text(self):
        text = "[Visit Boot.dev](https://boot.dev)"
        output = process_inline_text(text)
        self.assertEqual(output[0].tag, "a")
        self.assertEqual(output[0].value, "Visit Boot.dev")
        self.assertEqual(output[0].props['href'], "https://boot.dev")

    def test_process_inline_text_code_text(self):
        text = "`Code snippet`"
        output = process_inline_text(text)
        self.assertEqual(output[0].tag, "code")
        self.assertEqual(output[0].value, "Code snippet")

    def test_process_inline_text_image_text(self):
        text = "![Alt text](https://example.com/image.png)"
        output = process_inline_text(text)
        self.assertEqual(output[0].tag, "img")
        self.assertEqual(output[0].value, "")  # Images generally have no value
        self.assertEqual(output[0].props['src'], "https://example.com/image.png")
        self.assertEqual(output[0].props['alt'], "Alt text")
        
    def test_markdown_to_html_node(self):
        markdown_document = "# Heading 1\n\n```\nCode block\n```\n\n>Quote\n\n* Item 1\n* Item 2\n\n1. Item 1\n2. Item 2"
        result = markdown_to_html_node(markdown_document)
        expected = HTMLNode("div", None, [
            HTMLNode("h1", "Heading 1"),
            HTMLNode("pre", None, [HTMLNode("code", "Code block")]),
            HTMLNode("blockquote", "Quote"),
            HTMLNode("ul", None, [
                HTMLNode("li", "Item 1"),
                HTMLNode("li", "Item 2"),
            ]),
            HTMLNode("ol", None, [
                HTMLNode("li", "Item 1"),
                HTMLNode("li", "Item 2"),
            ])
        ])
        self.assertEqual(result, expected)
        
    def test_text_to_children(self):
        text = "This is a paragraph of text with **bold** and *italic* elements, with `code`, ![an image of an iguana](https://www.i.imgur.com/iguana.jpeg), and a link to a [quail](https://www.quail.net)."
        result = text_to_children(text)
        expected = [
            LeafNode(None, "This is a paragraph of text with "),
            LeafNode("b", "bold"),
            LeafNode(None, " and "),
            LeafNode("i", "italic"),
            LeafNode(None, " elements, with "),
            LeafNode("code", "code"),
            LeafNode(None, ", "),
            HTMLNode("image", "", {"alt": "an image of an iguana", "url": "https://www.i.imgur.com/iguana.jpeg"}),
            LeafNode(None, ", and a link to a "),
            HTMLNode("link", "quail", {"url": "https://www.quail.net"}),
            LeafNode(None, "."),
        ]
        self.assertEqual(result, expected)
        
    def test_text_to_children_bold(self):
        markdown = "**I like Tolkien**"
        nodes = text_to_children(markdown)
        html_fragment = "".join(node.to_html() for node in nodes)
        print(html_fragment)
        
if __name__ == "__main__":
    unittest.main()
