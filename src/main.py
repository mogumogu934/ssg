import os
import shutil
from enum import Enum

def copy_static_to_public():
    source_dir = os.path.expanduser("~/workspace/github.com/mogumogu934/ssg/static")
    destination_dir = os.path.expanduser("~/workspace/github.com/mogumogu934/ssg/public")
    
    if os.path.exists(destination_dir):
        print(f"Deleting {destination_dir}")
        shutil.rmtree(destination_dir)
        
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            source_file = os.path.join(root, file)
            destination_file = os.path.join(destination_dir, os.path.relpath(source_file, source_dir))
            destination_file_dir = os.path.dirname(destination_file)
            if not os.path.exists(destination_file_dir):
                os.makedirs(destination_file_dir)
            print(f"Copying from {source_file} to {destination_file}...")
            shutil.copy2(source_file, destination_file)

def main():
    copy_static_to_public()
    
if __name__ == "__main__":
    main()
