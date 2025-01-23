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
    markdown_contents = open(from_path).read()
    template_contents = open(template_path).read()
    
    