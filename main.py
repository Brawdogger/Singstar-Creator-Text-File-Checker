# ADD CHECK FOR ' AND " AND / IN SONG TITLE AND FILE NAME
# ADD CHECK FOR DUETSINGERP1/2 IN META (NEEDS TO BE P1/P2) AND TO REMOVE ANY SPACES BETWEEN P 2
# ADD CHECK FOR FOR IF LAST LINE IN DUET IS A PAGE BREAK (CAUSES SINGSTAR TO CRASH)
# ADD CHECK FOR LINES WITH NUMBERS THAT ARE SMALLER THAN PREVIOUS LINE (ESPECIALLY FOR LINE BREAKS)

import tkinter as tk
from tkinter import filedialog, messagebox
import sv_ttk
from frontend.toolbar import create_toolbar
from backend.find_txt_files import find_text_files
from backend.scan_files import scan_errors_in_files
from backend.fix_comma_error import fix_comma_and_encoding_errors
from idlelib.tooltip import Hovertip

# Main application class
class SCTxtAnalysis:
    def __init__(self, root):
        self.root = root
        self.root.geometry("500x900")
        self.root.title('Singstar Creator Text File Checker')
        sv_ttk.set_theme("light")  # Set the light theme

        # Text area to display the results
        self.text_area = tk.Text(root, wrap=tk.WORD, state=tk.DISABLED, bg='white', fg='black')
        self.text_area.pack(expand=True, fill=tk.BOTH)

        # Add tag for invalid files to be highlighted in red
        self.text_area.tag_configure('invalid', foreground='red')

        # Store the list of text files
        self.text_files = []

        # Create the toolbar
        create_toolbar(root, self.select_directory)

        # Button to select individual text files
        self.select_files_button = tk.Button(root, text="Select Individual Text Files", command=self.select_individual_files)
        self.select_files_button.pack(pady=5)

        # Button to select a directory of text files
        self.select_directory_button = tk.Button(root, text="Select Directory", command=self.select_directory)
        self.select_directory_button.pack(pady=5)
       
        # Variable to track the checkbox state (for negative timestamps search)
        self.check_negative_timestamp = tk.BooleanVar(value=False)

        # Add checkbox to enable or disable negative timestamp search
        self.checkbox = tk.Checkbutton(self.root, text="(OPTIONAL) Check for negative timestamps", variable=self.check_negative_timestamp)
        self.checkbox.pack()
        self.checkboxTooltip = Hovertip(self.checkbox,'It is currently unknown whether negative timestamps are causing any issues, however \n if you try importing any songs and experience issues when trying to play them, \n try enabling this setting to see if this could be a possible reason')

        # Scan button
        self.scan_button = tk.Button(root, text="Scan files for errors", state=tk.DISABLED, command=self.scan_files)
        self.scan_button.pack(pady=5)

        # Add a button to fix comma errors
        self.fix_errors_button = tk.Button(self.root, text="Fix Comma & Encoding Errors", state=tk.DISABLED, command=self.fix_errors)
        self.fix_errors_button.pack(pady=5)

        self.clear_list_button = tk.Button(self.root, text="Clear list", state=tk.DISABLED, command=self.clear_file_list)
        self.clear_list_button.pack(pady=5)

    def update_file_list(self):
        """Update the text area with the current list of files."""
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        if self.text_files:
            self.text_area.insert(tk.END, "Selected Files:\n")
            for file in self.text_files:
                self.text_area.insert(tk.END, f"{file}\n\n")  # Add a break line between each file
        else:
            self.text_area.insert(tk.END, "No files selected.")
        self.text_area.config(state=tk.DISABLED)

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            # Get all the text files from the selected directory
            selected_files = find_text_files(directory)
            if selected_files:
                # Add selected files to the main list
                self.text_files.extend(selected_files)
                self.scan_button.config(state=tk.NORMAL)  # Enable scan button if files found
                self.clear_list_button.config(state=tk.NORMAL)
                self.update_file_list()  # Update the text area with the new file list

    def select_individual_files(self):
        # Allow users to select individual text files
        files = filedialog.askopenfilenames(title="Select Text Files", filetypes=[("Text Files", "*.txt")])
        if files:
            # Add selected files to the main list
            self.text_files.extend(files)
            self.scan_button.config(state=tk.NORMAL)  # Enable scan button if files found
            self.clear_list_button.config(state=tk.NORMAL)
            self.update_file_list()  # Update the text area with the new file list

    def scan_files(self):
        if self.text_files:
            # Use the function to scan each file for "BPM:" and numbers before it
            bpm_data, self.invalid_files = scan_errors_in_files(self.text_files, self.check_negative_timestamp.get())

            # Display the BPM findings in the text area
            self.text_area.config(state=tk.NORMAL)
            self.text_area.delete(1.0, tk.END)

            if bpm_data:
                if any("Contains comma in BPM" or "Incorrect encoding (expected UTF-8)" in error for error in self.invalid_files.values()):
                    self.fix_errors_button.config(state=tk.NORMAL)

                for file, bpm in bpm_data.items():
                    if file in self.invalid_files and self.invalid_files[file]:
                        # Highlight invalid files in red and show the error
                        self.text_area.insert(tk.END, f"{file} - BPM: {bpm} ({self.invalid_files[file]})\n\n", 'invalid')
                    else:
                        self.text_area.insert(tk.END, f"{file} - BPM: {bpm}\n\n")
            else:
                self.text_area.insert(tk.END, "No BPM information found in any of the selected files.")

            self.text_area.config(state=tk.DISABLED)
        else:
            messagebox.showwarning("No Files to Scan", "There are no files to scan for BPM.")
   
    def fix_errors(self):
        fixed_files, converted_files = fix_comma_and_encoding_errors(self.text_files, self.invalid_files)
        if fixed_files or converted_files:
            self.update_file_list()  # Refresh file list after fixing errors

    def clear_file_list(self):
        """Clear the file list and update the display."""
        self.text_files = []
        self.scan_button.config(state=tk.DISABLED)  # Enable scan button if files found
        self.fix_errors_button.config(state=tk.DISABLED)
        self.update_file_list()  # Update the text area with the new file list

# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = SCTxtAnalysis(root)
    root.mainloop()
