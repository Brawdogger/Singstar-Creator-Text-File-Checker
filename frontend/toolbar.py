# frontend/toolbar.py
import tkinter as tk
from tkinter import Menu, messagebox
import sv_ttk  # Import sv_ttk for Sun Valley theme

def create_toolbar(root, text_area):
    # Create a menu bar
    menu_bar = Menu(root)

    # Create a themes menu
    theme_menu = Menu(menu_bar, tearoff=0)
    theme_menu.add_command(label="Light", command=lambda: toggle_theme("light", text_area))
    theme_menu.add_command(label="Dark", command=lambda: toggle_theme("dark", text_area))

    help_menu = Menu(menu_bar, tearoff=0)
    help_menu.add_command(label="Info", command=lambda: info_popup())

    # Add the themes menu to the menu bar
    menu_bar.add_cascade(label="Themes", menu=theme_menu)
    menu_bar.add_cascade(label="Help", menu=help_menu)

    # Configure the menu bar in the main window
    root.config(menu=menu_bar)

def toggle_theme(theme, text_area):
    if theme == "dark":
        sv_ttk.set_theme("dark")  # Set dark theme
        text_area.config(background='black', foreground='white')  # Dark text area
    else:
        sv_ttk.set_theme("light")  # Set light theme
        text_area.config(background='white', foreground='black')  # Light text area

def info_popup():
    messagebox.showinfo("Singstar Creator Text File Checker - By Brawdogger", f"Singstar Creator Text File Checker V.1 - By Brawdogger\n\nThis tool is to be used alongside Singstar Creator to find any issues found within the txt files of songs that SC either doesn't find or doesn't explain clearly what the issue is\n\nCurrently, this tools detects the following errors in text files: \n Txt files not using UTF-8 encoding \n BPM that are using a comma instead of a fullstop \n BPM's that are too high (above 350) \n Invalid Rap notes (R and G) in file \n (OPTIONAL - Unsure if these do cause issues) Negative timestamps on notes")