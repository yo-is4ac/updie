import subprocess as sub 
import os
import re
import tkinter as tk
from tkinter import ttk

def is_folder_accessible(target_folder):
    try:
        os.listdir(target_folder)
    except PermissionError as e:
        return False

def is_list_group_available(target_folder):
    try:
        sub.run(["icacls", target_folder], check=True, capture_output=True, text=True)
    except sub.SubprocessError as e:
        return False

def take_own_dir(target_folder):
    sub.run(["takeown", "/f", target_folder, "/r", "/d", "y"], check=True, capture_output=True)

def is_everyone_present(target_folder):
    pattern = r"Everyone"
    text = sub.run(["icacls", target_folder], capture_output=True, check=True, text=True)

    match_object = re.search(pattern, str(text))

    if match_object:
        return True
    
    return False

def add_everyone_to_group(target_folder):
    # Adding to everyone full access
    sub.run(["icacls", target_folder, "/grant", "Everyone:F"], capture_output=True, check=True, text=True)

def get_current_status(target_folder):
    pattern = r"(Everyone:)\((\w)\)"
    text = sub.run(["icacls", target_folder], capture_output=True, check=True, text=True)
    
    match_object = re.search(pattern, str(text))
    
    if match_object:
        return match_object.group(2)

def format_current_status(permission):
    if permission == 'N':
        return "Disabled"
    elif permission == 'F':
        return 'Enabled'

def disableWindowsUpdate(target_folder, label):
    sub.run(["icacls", target_folder, "/deny", "Everyone:F"], capture_output=True, check=True, text=True)
    label.config(text="Windows Update Status: Disabled")

def enableWindowsUpdate(target_folder, label):
    sub.run(["icacls", target_folder, "/grant", "Everyone:F"], capture_output=True, check=True, text=True)
    label.config(text="Windows Update Status: Enabled")

def main():
    root = tk.Tk()
    root.title("updie")

    target_folder = "C:\\Windows\\SoftwareDistribution\\Download"

    try: 
        if (is_folder_accessible(target_folder) == False):
            if (is_list_group_available(target_folder) == False):
                take_own_dir(target_folder) 
        
        if (is_everyone_present(target_folder) == False):
            add_everyone_to_group(target_folder)
        
        status = get_current_status(target_folder)
        status_formatted = format_current_status(status)

        label = ttk.Label(master=root, text=f"Windows Update Status: {status_formatted}")
        label.pack(padx=20)

        button_disable = ttk.Button(master=root, text="Disable Windows Update", command=lambda: disableWindowsUpdate(target_folder, label))
        button_enable = ttk.Button(master=root, text="Enable Windows Update", command=lambda: enableWindowsUpdate(target_folder, label))
        
        button_disable.pack(pady=30)
        button_enable.pack(pady=30)
    except Exception as e:
        label = ttk.Label(master=root, text="path= " + target_folder + "\n" + str(e))
        label.pack(padx=20)

    root.mainloop()

main()
