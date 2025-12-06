import subprocess as sub
import os
import re
import tkinter as tk
from tkinter import ttk, messagebox


TARGET_FOLDER = r"C:\Windows\SoftwareDistribution\Download"
STATUS_PREFIX = "Windows Update Status: "


# ------------------------------ PERMISSION HELPERS ------------------------------

def is_folder_accessible(path):
    try:
        os.listdir(path)
        return True
    except PermissionError:
        return False
    except Exception:
        return False


def is_list_group_available(path):
    try:
        sub.run(["icacls", path], check=True, capture_output=True, text=True)
        return True
    except Exception:
        return False


def take_ownership(path):
    try:
        sub.run(["takeown", "/f", path, "/r", "/d", "y"], check=True, capture_output=True, text=True)
        return True
    except Exception as e:
        return False


def has_everyone_entry(path):
    try:
        result = sub.run(["icacls", path], capture_output=True, check=True, text=True)
        return "Everyone" in result.stdout
    except Exception:
        return False

def add_everyone(path):
    try:
        sub.run(["icacls", path, "/grant", "Everyone:F"], check=True, capture_output=True, text=True)
        return True
    except Exception:
        return False


def get_folder_permission_status(path):
    """Returns 'F' (full), 'N' (none), or None."""
    pattern = r"Everyone:(\([\w]+\))"
    try:
        result = sub.run(["icacls", path], capture_output=True, check=True, text=True)
        m = re.search(r"Everyone:(\([N, F]\))", result.stdout)
        if m:
            return m.group(1).strip("()")
        else:
            sub.run(["icacls", path, "/remove", "Everyone"])
    except Exception:
        pass
    return "F"


def apply_permission(path, enabled):
    """enabled=True → grant   enabled=False → deny"""
    try:
        if enabled:
            sub.run(["icacls", path, "/grant:r", "Everyone:F"], check=True, text=True, capture_output=True)
        else:
            sub.run(["icacls", path, "/deny", "Everyone:F"], check=True, text=True, capture_output=True)
        return True
    except Exception as e:
        return False


# ------------------------------ UI LOGIC ------------------------------

def update_ui(status_label, button, enabled):
    status_label.config(
        text=f"{STATUS_PREFIX}{'Enabled' if enabled else 'Disabled'}",
        foreground="green" if enabled else "red"
    )
    button.config(text="Disable Windows Update" if enabled else "Enable Windows Update")


def toggle_update(status_label, button):
    # Determine desired state
    current = get_folder_permission_status(TARGET_FOLDER)
    new_state = current != 'F'  # If not full, user wants enable

    ok = apply_permission(TARGET_FOLDER, new_state)
    if not ok:
        
        messagebox.showwarning("Warning", "Failed to perform action, it may be your first time? taking ownership of the folder and trying again....")

        if not is_folder_accessible(TARGET_FOLDER):
            if not is_list_group_available(TARGET_FOLDER):
                take_ownership(TARGET_FOLDER)
        
            if not has_everyone_entry(TARGET_FOLDER):
                add_everyone(TARGET_FOLDER)
        else:
            messagebox.showerror("Error", "Failed to perform action")
    update_ui(status_label, button, new_state)
    
    return 

# ------------------------------ MAIN UI ------------------------------

def main():
    root = tk.Tk()
    root.title("Windows Update Toggle")
    root.geometry("420x200")
    root.resizable(False, False)


    #base = os.path.dirname(__file__)
    #path = os.path.join(base, "icon.png")

    #root.iconphoto(False, tk.PhotoImage(file="icon.png"))

    # Center on screen
    root.update_idletasks()
    w = 420
    h = 200
    x = (root.winfo_screenwidth() // 2) - (w // 2)
    y = (root.winfo_screenheight() // 2) - (h // 2)
    root.geometry(f"{w}x{h}+{x}+{y}")

    frame = ttk.Frame(root, padding=20)
    frame.pack(expand=True, fill="both")

    status_label = ttk.Label(frame, text="Checking status...", font=("Segoe UI", 12))
    status_label.pack(pady=10)

    button = ttk.Button(frame, text="Loading...")
    button.pack(pady=20)

    # ----- Initial setup -----
    try:
        if not is_folder_accessible(TARGET_FOLDER):
            if not is_list_group_available(TARGET_FOLDER):
                take_ownership(TARGET_FOLDER)
        
        if not has_everyone_entry(TARGET_FOLDER):
            add_everyone(TARGET_FOLDER)

        current = get_folder_permission_status(TARGET_FOLDER)
        enabled = current == "F"

        update_ui(status_label, button, enabled)

        button.config(command=lambda: toggle_update(status_label, button))

    except Exception as e:
        messagebox.showerror("Initialization Error", str(e))

    root.mainloop()


if __name__ == "__main__":
    main()
