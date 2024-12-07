import chardet
import re
from tkinter import messagebox

def fix_comma_and_encoding_errors(file_list, invalid_files):
    fixed_files = []
    converted_files = []

    for file in file_list:
        if file in invalid_files:
            errors = invalid_files[file]

            # Fix BPM comma errors if present
            if "Contains comma in BPM" in errors:
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Replace commas in BPM values with periods
                    content_fixed = re.sub(r'BPM:\s*(\d+),(\d+)', r'BPM: \1.\2', content)

                    with open(file, 'w', encoding='utf-8') as f:
                        f.write(content_fixed)

                    fixed_files.append(file)

                except Exception as e:
                    print(f"Error fixing BPM comma in {file}: {e}")

            # Fix incorrect encoding by converting to UTF-8
            if "Incorrect encoding" in errors:
                try:
                    with open(file, 'rb') as f:
                        raw_data = f.read()
                    
                    # Decode with detected encoding and re-encode to UTF-8
                    result = chardet.detect(raw_data)
                    encoding = result['encoding']
                    if encoding and encoding.lower() != 'utf-8':
                        text_data = raw_data.decode(encoding)
                        with open(file, 'w', encoding='utf-8') as f:
                            f.write(text_data)
                        converted_files.append(file)

                except Exception as e:
                    print(f"Error converting {file} to UTF-8: {e}")

    # Notify the user of the changes
    if fixed_files or converted_files:
        msg = ""
        if fixed_files:
            msg += "The following files had BPM commas fixed:\n" + "\n".join(fixed_files) + "\n\n"
        if converted_files:
            msg += "The following files were converted to UTF-8 encoding:\n" + "\n".join(converted_files)
        
        # Display an info message to the user
        messagebox.showinfo("Files Fixed", msg)

        return fixed_files, converted_files
    else:
        messagebox.showinfo("No Files Fixed", "No files required fixing.")
        return [], []