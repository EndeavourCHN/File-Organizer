import os
import shutil

def move_file(filepath, target_dir):
    os.makedirs(target_dir, exist_ok=True)
    filename = os.path.basename(filepath)
    shutil.move(filepath, os.path.join(target_dir, filename))
