import subprocess as sub 
import tkinter as tk
from tkinter import ttk

# Check the folder permissions
# cd: Permission Denied? If not Proceed
# if Permission Denied and Everyone is present settled to Deny All: take own rights from the folder 
# if Everyone is not present Proceed

def is_folder_accessible(target_folder):
    sub.run(["dir", target_folder], check=True)

    return True

def main():
    root = tk.Tk()
    root.title("updie")

    target_folder = "C:\\Windows\\SoftwareDistribution\\Download"

    try:
        #print(is_folder_accessible(sub, target_folder))
        
        label = ttk.Label(master=root, text="Result: " + str(is_folder_accessible(target_folder)))
        label.pack(padx=20)
    except Exception as e:
        label = ttk.Label(master=root, text="path= " + target_folder + "\n" + str(e))
        label.pack(padx=20)

    root.mainloop()

main()
