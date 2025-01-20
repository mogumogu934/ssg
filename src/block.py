def markdown_to_blocks(markdown):
    blocks = list(map(str.strip, markdown.split("\n\n")))
    filtered_blocks = list(filter(None, blocks))
    
    return filtered_blocks

def block_to_block_type(markdown_block):
    import re
    
    def is_heading_block(block):
        regex_heading = r"(^#{1,6}\s{1})"
        if not re.findall(regex_heading, block):
            return False
        return True
        
    def is_code_block(block):
        return block.startswith("```") and block.endswith("```")
    
    def is_quote_block(block):
        lines = block.split("\n")
        for line in lines:
            if not line.startswith(">"):
                return False
        return True
        
    def is_unordered_list_block(block):
        lines = block.split("\n")
        for line in lines:
            if not line.startswith(("*", "-")):
                return False
        return True
    
    def is_ordered_list_block(block):
        lines = block.split("\n")
        i = 0
        for line in lines:
            i += 1
            if not line.startswith(f"{i}."):
                return False
        return True
                
    if is_heading_block(markdown_block):
        return "HEADING"
    elif is_code_block(markdown_block):
        return "CODE"
    elif is_quote_block(markdown_block):
        return "QUOTE"
    elif is_unordered_list_block(markdown_block):
        return "UNORDERED LIST"
    elif is_ordered_list_block(markdown_block):
        return "ORDERED LIST"
    else:
        return "PARAGRAPH"
    