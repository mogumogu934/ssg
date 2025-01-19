import re
from enum import Enum
from htmlnode import HTMLNode, LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    
class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
        
    def __eq__(self, other):
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, props = {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", props = {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("invalid TextType")

def extract_markdown_images(text):
    alt_text_and_image_urls = re.findall(r"!\[(.*?)\]\(\w+\:\/\/(.*?)\)", text)
    
    alt_text = []
    image_urls =[]
    
    for string_and_url in alt_text_and_image_urls:
        end_of_alt_string_index = string_and_url.index("]")
        start_of_url_index = string_and_url.index("(") + 1
        alt_text.append(string_and_url[2:end_of_alt_string_index])
        image_urls.append(string_and_url[start_of_url_index:-1])
        
    return list(zip(alt_text, image_urls))

def extract_markdown_links(text):
    anchor_text_and_image_urls = re.findall(r"\[(.*?)\]\(\w+\:\/\/(.*?)\)", text)
    
    anchor_text = []
    image_urls =[]
    
    for string_and_url in anchor_text_and_image_urls:
        end_of_anchor_string_index = string_and_url.index("]")
        start_of_url_index = string_and_url.index("(") + 1
        anchor_text.append(string_and_url[1:end_of_anchor_string_index])
        image_urls.append(string_and_url[start_of_url_index:-1])
        
    return list(zip(anchor_text, image_urls))
