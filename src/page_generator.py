import os
from markdown_blocks import markdown_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode

def extract_title(markdown):
    import re
    regex_title = r"^#\s(.*)"
    match = re.match(regex_title, markdown)
    title = match.group()[2:]
    if title:
        return title
    else:
        raise Exception("missing title")
    
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r") as file:
        markdown_contents = file.read()
        
    with open(template_path, "r") as file:
        template_contents = file.read()
        
    title = extract_title(markdown_contents)
    html_contents = markdown_to_html_node(markdown_contents).to_html()
    final_html = template_contents.replace("{{ Title }}", title).replace("{{ Content }}", html_contents)
    
    # create directory if it doesn't exist (os.path.dirname will return "" if dest_path is just a filename)
    dest_file_path = os.path.dirname(dest_path)
    if dest_file_path:
        os.makedirs(dest_file_path, exist_ok=True)
        
    with open(dest_path, "wt") as file:
        file.write(final_html)
        