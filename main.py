import subprocess as sub 
import os
import re
import tkinter as tk
from tkinter import ttk

# Is folder accesible? if not, can i list the groups inside it? 
# If so i will search for everyone 
# If not takeOwn From the Dir

def is_folder_accessible(target_folder):
    try:
        os.listdir(target_folder)
    except PermissionError as e:
        return False

def take_own_dir(target_folder):
    sub.run(["takeown", "/f", "/r", "/d", "y", target_folder], check=True, capture_output=True)

def is_list_group_available(target_folder):
    sub.run(["icacls", target_folder])

def is_everyone_present(target_folder):
    sub.run(["icacls", target_folder])

def main():
    root = tk.Tk()
    root.title("updie")

    target_folder = "C:\\Windows\\SoftwareDistribution\\Download"

    try: 
        if (is_folder_accessible(target_folder) == False):
            if (is_list_group_available(target_folder) == False):
                
    except Exception as e:
        label = ttk.Label(master=root, text="path= " + target_folder + "\n" + str(e))
        label.pack(padx=20)

    root.mainloop()

main()
