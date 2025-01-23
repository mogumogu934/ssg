from copy_static import copy_static_to_public
from page_generator import generate_page

source_dir = "./static"
destination_dir = "./public"

def main():
    copy_static_to_public(source_dir, destination_dir)
    generate_page("./content/index.md", "template.html", "./public/index.html")
    
    
if __name__ == "__main__":
    main()
