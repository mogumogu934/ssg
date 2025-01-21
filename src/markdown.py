import re
from htmlnode import HTMLNode

def markdown_to_blocks(markdown):
    blocks = list(map(str.strip, markdown.split("\n\n")))
    filtered_blocks = list(filter(None, blocks))
    
    return filtered_blocks

def block_to_block_type(markdown_block): 
    def is_heading_block(block):
        regex_heading = r"^(#{1,6})\s"
        return bool(re.match(regex_heading, block))
    
    def is_code_block(block):
        return block.startswith("```") and block.endswith("```")
    
    def is_quote_block(block):
        return all(line.startswith(">") for line in markdown_block.split("\n"))
        
    def is_unordered_list_block(block):
        return all(line.strip().startswith(("-", "*", "+")) for line in markdown_block.split("\n"))
    
    def is_ordered_list_block(block):
        # A block is an ordered list if each line starts with '1.', '2.', ..., in order
        lines = markdown_block.split("\n")
        for i, line in enumerate(lines, start=1):
            if not line.strip().startswith(f"{i}."):
                return False
        return True
                
    if is_code_block(markdown_block): # code must be first to avoid potential misclassification
        return "CODE"
    elif is_heading_block(markdown_block):
        return "HEADING"
    elif is_quote_block(markdown_block):
        return "QUOTE"
    elif is_unordered_list_block(markdown_block):
        return "UNORDERED LIST"
    elif is_ordered_list_block(markdown_block):
        return "ORDERED LIST"
    else:
        return "PARAGRAPH"
    
def markdown_to_html_node(markdown):
    children_nodes = []
    
    for block in markdown_to_blocks(markdown):
        if block_to_block_type(block) == "HEADING":
            match = re.match(r"^(#{1,6})\s+(.*)", block)
            if match:
                hashes = match.group(1)
                heading_text = match.group(2)
                heading_level = len(hashes)
                heading_tag = f"h{heading_level}"
                children_nodes.append(HTMLNode(heading_tag, heading_text))
            
        elif block_to_block_type(block) == "CODE":
            match = re.match(r"^```\n([\s\S]*?)\n```$", block)
            if match:
                code_content = match.group(1).strip()
                children_nodes.append(HTMLNode("pre", "", [HTMLNode("code", code_content)]))

        elif block_to_block_type(block) == "QUOTE":
            lines = block.split("\n")
            normalized_lines = [line.lstrip(">").strip() for line in lines]
            quote_content = "\n".join(normalized_lines)  # Use "\n" to preserve formatting
            children_nodes.append(HTMLNode("blockquote", quote_content))

        elif block_to_block_type(block) == "UNORDERED LIST":
            list_items = []
            for line in block.split("\n"):
                if line.startswith(("-", "*", "+")):
                    list_items.append(HTMLNode("li", line[2:]))
            children_nodes.append(HTMLNode("ul", "", list_items))
            
        elif block_to_block_type(block) == "ORDERED LIST":
            list_items = []
            for line in block.split("\n"):
                if line[0].isdigit():
                    match = re.match(r"^\d+\.\s", line)
                    if match:
                        list_item_text = line[match.end():]  # get text after match
                        list_items.append(HTMLNode("li", list_item_text))
            children_nodes.append(HTMLNode("ol", "", list_items))
            
        elif block_to_block_type(block) == "PARAGRAPH":
            children_nodes.append(HTMLNode("p", block))
            
    return HTMLNode("div", "", children_nodes)

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
            nodes.append(HTMLNode("text", plain_text))
            
        matched_text = match.group(0)
        
        if matched_text.startswith("**"):
            bold_content = matched_text.strip("**")
            nodes.append(HTMLNode("b", bold_content))
            
        elif matched_text.startswith(("*", "_")):
            italic_content = matched_text[1:-1]
            nodes.append(HTMLNode("i", italic_content))
            
        elif matched_text.startswith("`"):
            code_content = matched_text.strip("`")
            nodes.append(HTMLNode("code", code_content))
            
        elif matched_text.startswith("!"):
            alt_text, image_url = re.match(r"!\[([^\]]+)\]\(([^)]+)\)", matched_text).groups()
            nodes.append(HTMLNode("image", "", {"alt": alt_text, "url": image_url}))
            
        elif matched_text.startswith("["):
            link_text, link_url = re.match(r"\[([^\]]+)\]\(([^)]+)\)", matched_text).groups()
            nodes.append(HTMLNode("link", link_text, {"url": link_url}))

        last_index = end
        
    # add any remaining plain text after last match
    if last_index < len(text):
        nodes.append(HTMLNode("text", text[last_index:]))
        
    return nodes
