import pyperclip
import tkinter as tk
from tkinter import messagebox, simpledialog
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

def show_message(title,message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo(title, message)
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

def ask_user_input_num(title="Input", message="Insert the number of copies"):
    root = tk.Tk()
    root.withdraw()  # Hide the main Tkinter window
    number_of_copies = simpledialog.askinteger(title, message,
                                               parent=root, minvalue=1)
    root.destroy()
    return number_of_copies

def ask_user_input_str(title="Input", message="Enter the new name"):
    root = tk.Tk()
    root.withdraw()  # Hide the main Tkinter window
    number_of_copies = simpledialog.askstring(title,message)
    root.destroy()
    return number_of_copies

def set_waapi_port(ip="127.0.0.1", port=8080):
    waapi_port = f"ws://{ip}:{port}/waapi"

    return waapi_port

def get_selected_items_type(type):
    try:
        waapi_port = set_waapi_port()
        with WaapiClient(waapi_port) as client:
            args = {"options": {"return":[type]}}
            result = client.call("ak.wwise.ui.getSelectedObjects", args)
            selected_items = []
            if "objects" in result:
                for obj in result["objects"]:
                    selection = obj[type]
                    selected_items.append((selection)) 
                    client.disconnect()
                return selected_items
                
            else:
                client.disconnect()
                return None
                
    except CannotConnectToWaapiException:
        show_error_message("Could not connect to Wwise Authoring API.")
        return None
    
def execute_func_times(func, times):
    for i in range(times):
        func()