import os

# Function to find all .txt files in a given directory and its subdirectories
def find_text_files(dir_path):
    text_files = []

    # Walk through the directory and its subdirectories to find .txt files
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith(".txt"):
                text_files.append(os.path.join(root, file))
    
    return text_files
