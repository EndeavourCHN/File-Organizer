import os

def scan_files(directory):
    files = []
    for entry in os.listdir(directory):
        path = os.path.join(directory, entry)
        if os.path.isfile(path):
            files.append(path)
    return files
