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
    regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    # re.findall returns a list of matches,
    # where each match is a tuple of captured groups
    # a captured group is a set of () in regex
    return re.findall(regex, text)

def extract_markdown_links(text):
    regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(regex, text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        remaining_text = node.text
        while True:
            extracted_images = extract_markdown_images(remaining_text)
            if not extracted_images: # no more images
                break
            
            image_alt, image_link = extracted_images[0]
            if not image_link: # handle invalid links if needed
                break
            
            # split text at current image
            sections = remaining_text.split(f"![{image_alt}]({image_link})", 1)
            if sections[0]: # avoid empty strings
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            
            # add image alt text and link as a LINK node
            new_nodes.append(TextNode(image_alt, TextType.LINK, image_link))
            
            # update the remaining text with the section after the image
            remaining_text = sections[1] if len(sections) > 1 else ""
            
        # add remaining text if there's still some left over after processing all images
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
                  
    return new_nodes
    
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        remaining_text = node.text
        while True:
            extracted_links = extract_markdown_links(remaining_text)
            if not extracted_links: # no more images
                break
            
            link_text, image_link = extracted_links[0]
            if not image_link: # handle invalid links if needed
                break
            
            # split text at current image
            sections = remaining_text.split(f"[{link_text}]({image_link})", 1)
            if sections[0]: # avoid empty strings
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            
            # add image link text and link as a LINK node
            new_nodes.append(TextNode(link_text, TextType.LINK, image_link))
            
            # update the remaining text with the section after the image
            remaining_text = sections[1] if len(sections) > 1 else ""
            
        # add remaining text if there's still some left over after processing all images
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
                  
    return new_nodes
