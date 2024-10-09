import pyperclip
import tkinter as tk
from tkinter import messagebox, simpledialog
from waapi import WaapiClient, CannotConnectToWaapiException
import xml.etree.ElementTree as ET
import os

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass


def set_client(ip="127.0.0.1"):
    port = "8080"
    wwise_settings = os.getenv('APPDATA')+r"\Audiokinetic\Wwise\Wwise.wsettings"
    tree = ET.ElementTree(file = wwise_settings)
    root = tree.getroot()
    for child in root[0][0][0]:
        if 'Waapi\\WampPort' in child.attrib["Name"]:
            port = (child.attrib["Value"])
    waapi_port = f"ws://{ip}:{port}/waapi"
    print(f"Client set to: {waapi_port}")
    client = WaapiClient(waapi_port)
    return client


def get_clipboard_content():
    content = pyperclip.paste()
    if content:
        return content.strip().split("\r\n")
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


def show_message(title, message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo(title, message)
    root.destroy()

### Returns a list with each selected object, its GUID, name and any additional arguments
def get_selected_items(client, *args):
    return_args = ["id","name"]
    if args:
        return_args.extend(args)
    args = {"options": {"return": return_args}}
    result = client.call("ak.wwise.ui.getSelectedObjects", args)
    selected_items = []
    if result:
        for obj in result["objects"]:
            selected_items.append(obj)
        return selected_items
    else:
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
    number_of_copies = simpledialog.askstring(title, message)
    root.destroy()
    return number_of_copies


def execute_func_times(func, times):
    for i in range(times):
        func()
