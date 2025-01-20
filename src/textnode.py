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

def text_to_textnodes(text):
    from image_and_link_splitter import split_nodes_image, split_nodes_link
    from delimiter import split_nodes_delimiter
    
    new_nodes = []
    new_text = [TextNode(text, TextType.TEXT)]
    current_nodes = split_nodes_image(new_text) # split_nodes_image must be before split_nodes_link
    current_nodes = split_nodes_link(current_nodes)
    current_nodes = split_nodes_delimiter(current_nodes, "**", TextType.BOLD)
    for delimiter in ["*", "__"]:
        current_nodes = split_nodes_delimiter(current_nodes, delimiter, TextType.ITALIC)
    current_nodes = split_nodes_delimiter(current_nodes, "`", TextType.CODE)
    
    for element in current_nodes:
        if isinstance(element, str):
            new_nodes.append(TextNode(element, TextType.TEXT))
        else:
            new_nodes.append(element)
            
    return new_nodes
