import os
import shutil

def copy_static_to_public(source_dir, destination_dir):
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
            print(f"Copying static files to public directory...")
            shutil.copy2(source_file, destination_file)
            