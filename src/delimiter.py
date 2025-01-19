from textnode import TextNode, TextType

class InvalidMarkdownSyntaxError(Exception):
    pass

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if not delimiter.strip():
        raise ValueError("Delimiter cannot be empty or whitespace")
    
    new_nodes = []
    
    for node in old_nodes:
        match node.text_type:
            case TextType.TEXT:
                split_pieces = node.text.split(delimiter)
                
                # when the number of split_pieces is even, it implies an unmatched delimiter
                if len(split_pieces) % 2 == 0:
                    raise InvalidMarkdownSyntaxError(f"Invalid Markdown syntax. Unmatched delimiter: '{delimiter}' in text: '{node.text}'")
                
                for index, string in enumerate(split_pieces):
                    if string:  # avoid creating nodes for empty strings
                        
                        if index % 2 == 0:  # even index means it's plain text
                            new_nodes.append(TextNode(string, TextType.TEXT))
                        
                        else:   # odd index means the text is inside the delimiters
                            new_nodes.append(TextNode(string, text_type))
                        
            # add non-TextType.TEXT nodes as-is
            case _:
                new_nodes.append(node)

    return new_nodes
