import pyperclip
import tkinter as tk
from tkinter import messagebox
from waapi import WaapiClient, CannotConnectToWaapiException
import wwise_helpers

#Set the WAAPI port
waapi_port = wwise_helpers.set_waapi_port()
# Function to get clipboard content
def get_clipboard_content():
    content = pyperclip.paste()  # Get content from clipboard
    if content:
        return content.strip().split('\n')  # Split content into a list by new lines
    else:
        return None

# Function to display an error message
def show_error_message(message):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showerror("Error", message)
    root.destroy()

# Function to display a success message
def show_success_message(message):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showinfo("Success", message)
    root.destroy()

# Function to get selected items from Wwise
def get_selected_items():
    try:
        with WaapiClient(waapi_port) as client:
            args = {
                "options": {"return":["id", "name"]}  # Correct syntax for return fields
            }
            result = client.call("ak.wwise.ui.getSelectedObjects", args)
            selected_items = []
            if "objects" in result:  # Ensuring that "objects" key is present in the result
                for obj in result["objects"]:
                    obj_name = obj["name"]
                    obj_id = obj["id"]
                    selected_items.append((obj_id, obj_name))  # Append tuple of ID and name to list
                return selected_items  # Return list of tuples
            else:
                return None  # Return None if no objects are selected
    except CannotConnectToWaapiException:
        show_error_message("Could not connect to Wwise Authoring API.")
        return None

# Function to rename selected items in Wwise
def rename_selected_items(selected_items, new_names):
    try:
        with WaapiClient(waapi_port) as client:
            if len(selected_items) != len(new_names):
                show_error_message("The number of selected items and clipboard names do not match.")
                return False
            
            for (obj_id, _), new_name in zip(selected_items, new_names):
                args = {
                    "object": obj_id,  # Use the ID of the object
                    "value": new_name
                }
                client.call("ak.wwise.core.object.setName", args)
                client.disconnect()
            
            return True  # Indicate success
    except CannotConnectToWaapiException:
        show_error_message("Could not connect to Wwise Authoring API.")
        return False

# Main function to orchestrate the renaming process
def main():
    new_names = get_clipboard_content()
    if not new_names:
        show_error_message("Clipboard is empty or content is not valid.")
        return

    selected_items = get_selected_items()
    if not selected_items:
        show_error_message("No items selected in Wwise.")
        return

    if rename_selected_items(selected_items, new_names):
        show_success_message("Selected items renamed successfully.")

if __name__ == "__main__":
    main()
