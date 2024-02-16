import pyperclip
import tkinter as tk
from tkinter import messagebox
from waapi import WaapiClient, CannotConnectToWaapiException
from wwise_helpers import set_client, show_error_message, show_success_message, get_clipboard_content

# Function to get selected items from Wwise
def get_selected_items(client):
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
    
# Function to rename selected items in Wwise
def rename_selected_items(client,selected_items, new_names):
    if len(selected_items) != len(new_names):
        show_error_message("The number of selected items and clipboard names do not match.")
        return False
    
    for (obj_id, _), new_name in zip(selected_items, new_names):
        args = {
            "object": obj_id,  # Use the ID of the object
            "value": new_name
        }
        client.call("ak.wwise.core.object.setName", args)
    return True  # Indicate success

# Main function to orchestrate the renaming process
def main():
    client = set_client()
    print(client)
    try:
        with client:
            new_names = get_clipboard_content()
            if not new_names:
                show_error_message("Clipboard is empty or content is not valid.")
                return

            selected_items = get_selected_items(client)
            if not selected_items:
                show_error_message("No items selected in Wwise.")
                return

            if rename_selected_items(client,selected_items, new_names):
                show_success_message("Selected items renamed successfully.")

    except CannotConnectToWaapiException:
        show_error_message("Could not connect to Wwise Authoring API.")
        return None

if __name__ == "__main__":
    main()
