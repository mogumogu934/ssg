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
            return HTMLNode(None, text_node.text)
        case TextType.BOLD:
            return HTMLNode("b", text_node.text)
        case TextType.ITALIC:
            return HTMLNode("i", text_node.text)
        case TextType.CODE:
            return HTMLNode("code", text_node.text)
        case TextType.LINK:
            return HTMLNode("a", text_node.text, props = {"href": text_node.url})
        case TextType.IMAGE:
            return HTMLNode("img", "", props = {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Invalid text type: {text_node.text_type}")

def text_to_textnodes(text):
    from image_and_link_splitter import split_nodes_image, split_nodes_link
    from delimiter import split_nodes_delimiter
    
    nodes = []
    current_nodes = [TextNode(text, TextType.TEXT)]
    current_nodes = split_nodes_image(current_nodes) # split_nodes_image must be before split_nodes_link
    current_nodes = split_nodes_link(current_nodes)
    current_nodes = split_nodes_delimiter(current_nodes, "**", TextType.BOLD)
    for delimiter in ["*", "__"]:
        current_nodes = split_nodes_delimiter(current_nodes, delimiter, TextType.ITALIC)
    current_nodes = split_nodes_delimiter(current_nodes, "`", TextType.CODE)
    
    for node in current_nodes:
        if isinstance(node, str):
            nodes.append(TextNode(node, TextType.TEXT))
        else:
            nodes.append(node)
            
    return nodes
