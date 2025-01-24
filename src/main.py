from copy_static import copy_static_to_public
from page_generator import generate_page, generate_pages_recursive

source_dir = "./static"
destination_dir = "./public"
content_dir = "./content"
template_dir = "./template.html"

def main():
    copy_static_to_public(source_dir, destination_dir)
#   generate_page("./content/index.md", template_dir, "./public/index.html")
    generate_pages_recursive(content_dir, template_dir, destination_dir)
    
if __name__ == "__main__":
    main()
