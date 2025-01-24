import re
from textnode import TextType, text_to_textnodes
from htmlnode import HTMLNode, LeafNode, ParentNode

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_ulist = "unordered_list"
block_type_olist = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = list(map(str.strip, markdown.split("\n\n"))) # strip whitespace from lines
    filtered_blocks = list(filter(None, blocks)) # remove empty blocks
    
    return filtered_blocks

def block_to_block_type(block):
    lines = block.split("\n")
    
    if block.startswith(("# ", "## ", "### ", "#### ", "#####", "###### ")):
        return block_type_heading
    
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].endswith("```"):
        return block_type_code
    
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return block_type_paragraph
        return block_type_quote
        
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return block_type_paragraph
        return block_type_ulist
    
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return block_type_paragraph
        return block_type_ulist
    
    if block.startswith("+ "):
        for line in lines:
            if not line.startswith("+ "):
                return block_type_paragraph
        return block_type_ulist
    
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return block_type_paragraph
            i += 1
        return block_type_olist
    
    return block_type_paragraph
    
def process_inline_text(text):
    inline_nodes = []
    text_nodes = text_to_textnodes(text)
    
    for text_node in text_nodes:
        if text_node.text_type == TextType.TEXT:
            inline_nodes.append(LeafNode(None, text_node.text))
        elif text_node.text_type == TextType.BOLD:
            inline_nodes.append(LeafNode("b", text_node.text))
        elif text_node.text_type == TextType.ITALIC:
            inline_nodes.append(LeafNode("i", text_node.text))
        elif text_node.text_type == TextType.CODE:
            inline_nodes.append(LeafNode("code", text_node.text))
        elif text_node.text_type == TextType.LINK:
            inline_nodes.append(LeafNode("a", text_node.text, props={"href": text_node.url}))
        elif text_node.text_type == TextType.IMAGE:
            inline_nodes.append(LeafNode("img", "", props={"src": text_node.url, "alt": text_node.text}))
    
    return inline_nodes

def markdown_to_html_node(markdown):
    children_nodes = []
    
    for block in markdown_to_blocks(markdown):
        if block_to_block_type(block) == block_type_heading:
            match = re.match(r"^(#{1,6})\s+(.*)", block)
            if match:
                hashes = match.group(1)
                heading_text = match.group(2)
                heading_level = len(hashes)
                heading_tag = f"h{heading_level}"
                children_nodes.append(LeafNode(heading_tag, heading_text))
            
        elif block_to_block_type(block) == block_type_code:
            match = re.match(r"^```\n([\s\S]*?)\n```$", block)
            if match:
                code_content = match.group(1).strip()
                children_nodes.append(ParentNode("pre", [LeafNode("code", code_content)]))

        elif block_to_block_type(block) == block_type_quote:
            stripped_lines = []
            lines = block.split("\n")
            for line in lines:
                stripped_lines.append(line.lstrip(">").strip())
            quote_content = "\n".join(stripped_lines)
            children_nodes.append(LeafNode("blockquote", quote_content))

        elif block_to_block_type(block) == block_type_ulist:
            list_items = []
            for line in block.split("\n"):
                if line.startswith(("- ", "* ", "+ ")):
                    inline_nodes = process_inline_text(line[2:])
                    inline_html = "".join(node.to_html() for node in inline_nodes)
                    list_items.append(LeafNode("li", inline_html))
            children_nodes.append(ParentNode("ul", list_items))
            
        elif block_to_block_type(block) == block_type_olist:
            list_items = []
            for line in block.split("\n"):
                if re.match(r"\d+\.", line):
                    text = line[line.find(" ") + 1:]
                    inline_nodes = process_inline_text(text)
                    inline_html = "".join(node.to_html() for node in inline_nodes)
                    list_items.append(LeafNode("li", inline_html))
            children_nodes.append(ParentNode("ol", list_items))
            
        elif block_to_block_type(block) == block_type_paragraph:
            inline_nodes = process_inline_text(block)     
            children_nodes.append(ParentNode("p", inline_nodes))

    return ParentNode("div", children_nodes)

def text_to_children(text):
    nodes = []
    regex = r"(\*\*.+?\*\*|\*.+?\*|`[^`]+`|!\[[^\]]+\]\([^)]*\)|\[[^\]]+\]\([^)]*\))" # composite regex
    
    # track remaining text after processing matches
    last_index = 0
    
    for match in re.finditer(regex, text):
        start, end = match.span() # start and end index of match
        
        # append any plain text before match
        if last_index < start:
            plain_text = text[last_index:start]
            nodes.append(LeafNode(None, plain_text))
            
        matched_text = match.group(0)
        
        if matched_text.startswith("**"):
            bold_content = matched_text.strip("**")
            nodes.append(LeafNode("b", bold_content))
            
        elif matched_text.startswith(("*", "_")):
            italic_content = matched_text[1:-1]
            nodes.append(LeafNode("i", italic_content))
            
        elif matched_text.startswith("`"):
            code_content = matched_text.strip("`")
            nodes.append(LeafNode("code", code_content))
            
        elif matched_text.startswith("!"):
            alt_text, image_url = re.match(r"!\[([^\]]+)\]\(([^)]+)\)", matched_text).groups()
            nodes.append(HTMLNode("image", "", {"alt": alt_text, "url": image_url}))
            
        elif matched_text.startswith("["):
            link_text, link_url = re.match(r"\[([^\]]+)\]\(([^)]+)\)", matched_text).groups()
            nodes.append(HTMLNode("link", link_text, {"url": link_url}))

        last_index = end
        
    # add any remaining plain text after last match
    if last_index < len(text):
        nodes.append(LeafNode(None, text[last_index:]))
        
    return nodes
