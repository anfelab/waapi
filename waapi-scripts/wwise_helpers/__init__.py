import pyperclip
import tkinter as tk
from tkinter import messagebox
from waapi import WaapiClient, CannotConnectToWaapiException

def get_clipboard_content():
    content = pyperclip.paste()
    if content:
        return content.strip().split('\n')
    else:
        return None

def show_error_message(message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Error", message)
    root.destroy()

def show_success_message(message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Success", message)
    root.destroy()

def get_selected_items():
    try:
        with WaapiClient() as client:
            args = {"options": {"return":["id", "name"]}}
            result = client.call("ak.wwise.ui.getSelectedObjects", args)
            selected_items = []
            if "objects" in result:
                for obj in result["objects"]:
                    obj_name = obj["name"]
                    obj_id = obj["id"]
                    selected_items.append((obj_id, obj_name))
                return selected_items
            else:
                return None
    except CannotConnectToWaapiException:
        show_error_message("Could not connect to Wwise Authoring API.")
        return None

def set_waapi_port(ip="127.0.0.1", port=8080):
    waapi_port = f"ws://{ip}:{port}/waapi"
    return waapi_port
