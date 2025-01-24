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
        
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # get list of all files whose filenames end with ".md" with their full paths
    markdown_files = []
    for (dirpath, dirnames, filenames) in os.walk(dir_path_content):
        for file in filenames:
            if file.endswith(".md"):
                markdown_files.append(os.path.join(dirpath, file))
    
    with open(template_path, "r") as file:
        template_contents = file.read()
        
    for entry in markdown_files:
        with open(entry, "r") as file:
            markdown_contents = file.read()
            
        title = extract_title(markdown_contents)
        html_contents = markdown_to_html_node(markdown_contents).to_html()
        final_html = template_contents.replace("{{ Title }}", title).replace("{{ Content }}", html_contents)
            
        entry_relative_path = os.path.relpath(entry, dir_path_content)
        dest_file_path = os.path.join(dest_dir_path, entry_relative_path.replace(".md", ".html"))
        
        print(f"Processing: {entry}")
        print(f"Relative Path: {entry_relative_path}")
        print(f"Destination Path: {dest_file_path}")
        # ensure destination folder structure exists
        if os.path.dirname(dest_file_path):
            os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
        
        with open(dest_file_path, "wt") as file:
            file.write(final_html)
