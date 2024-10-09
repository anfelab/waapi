from waapi import CannotConnectToWaapiException
from wwise_helpers import show_error_message, show_success_message, set_client, get_selected_items
import tkinter as tk
from tkinter import ttk

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass


def fetch_switch_groups():
    return ["SwitchGroup1", "SwitchGroup2", "SwitchGroup3"]


def create_ui(client):
    # Create the main window
    window = tk.Tk()
    window.geometry("300x250")
    window.title("Assign Switch Group to Switch Containers")

    # Create a frame for the dropdown and button
    frame = ttk.Frame(window)
    frame.pack(padx=25, pady=25)

    # Dropdown for switch groups
    switch_group_label = ttk.Label(frame, text="Select Switch Group:")
    switch_group_label.pack(fill='x', expand=True)

    switch_groups = fetch_switch_groups(client)
    switch_group_var = tk.StringVar()
    switch_group_dropdown = ttk.Combobox(frame, textvariable=switch_group_var, values=switch_groups)
    switch_group_dropdown.pack(fill='x', expand=True)
    switch_group_dropdown.set("Select a Switch Group")

    # Dropdown for default switch - Placeholder, to be populated based on selected switch group
    default_switch_label = ttk.Label(frame, text="Select Default Switch:")
    default_switch_label.pack(fill='x', expand=True)

    default_switch_var = tk.StringVar()
    default_switch_dropdown = ttk.Combobox(frame, textvariable=default_switch_var)
    default_switch_dropdown.pack(fill='x', expand=True)
    default_switch_dropdown.set("Select a Default Switch")

    # Placeholder for function to update switches based on selected switch group
    def update_switches(event):
        selected_group = switch_group_var.get()  # Get the selected switch group name
        switches = fetch_switches_for_selected_group(client, selected_group)
        default_switch_dropdown['values'] = switches  # Update the dropdown values
        if switches:
            default_switch_dropdown.set(switches[0])  # Optionally, set to first switch as default
        else:
            default_switch_dropdown.set("No Switches Found")

    # Bind the update_switches function to the switch group selection event
    switch_group_dropdown.bind('<<ComboboxSelected>>', update_switches)

    # Button to assign switch group to selected switches
    assign_button = ttk.Button(frame, text="Assign Switch Group",
                               command=lambda: assign_switch_group(client, switch_group_var.get(),
                                                                   default_switch_var.get()))
    assign_button.pack(fill='x', expand=True, pady=(10, 0))
    window.mainloop()


# Function to fetch all switch groups
def fetch_switch_groups(client):
    """

    :rtype: object
    :type client: object
    """
    if not client:
        show_error_message("Client could not connect to Wwise!")
        return
    args = {
        "from": {"ofType": ["SwitchGroup"]},
        "options": {"return": ["id", "name"]}
    }
    result = client.call("ak.wwise.core.object.get", args)
    switch_groups = [item['name'] for item in result['return']]
    return switch_groups


def fetch_switches_for_selected_group(client, switch_group_name):
    waql = f'$ from type Switch where parent.name = "{switch_group_name}"'
    args = {
        "waql": waql
    }
    result = client.call("ak.wwise.core.object.get", args)
    if result:
        switches = [item['name'] for item in result['return']]
        return switches


def assign_switch_group(client, switch_group_name, default_switch_name):
    selected_items = get_selected_items(client)
    for item in selected_items:
        item_id = item["id"]
        item_name = item["name"]
        switch_group_id = get_switch_group_id(client, switch_group_name)
        switch_id = get_switch_id(client, default_switch_name, switch_group_name)
        switch_group_args = {
            "object": item_id,
            "reference": "SwitchGroupOrStateGroup",
            "value": switch_group_id
        }
        switch_group_result = client.call("ak.wwise.core.object.setReference", switch_group_args)
        if switch_group_result:
            print(f"{item_name} assigned to {switch_group_name} Switch Group!")
        switch_args = {
            "object": item_id,
            "reference": "DefaultSwitchOrState",
            "value": switch_id
        }
        switch_result = client.call("ak.wwise.core.object.setReference", switch_args)
        if switch_result:
            print(f"Default Switch set to {default_switch_name}")

    show_success_message("Switch Groups Successfully assigned!")


def get_switch_group_id(client, switch_group_name):
    waql = f'from type switchGroup where name = "{switch_group_name}"'
    args = {
        "waql": waql
    }
    result = client.call("ak.wwise.core.object.get", args)
    switch_group_id = result["return"][0]["id"]
    return switch_group_id


def get_switch_id(client, default_switch_name, switch_group_name):
    waql = f'from type switch where name = "{default_switch_name}" and parent.name = "{switch_group_name}"'
    args = {
        "waql": waql
    }
    result = client.call("ak.wwise.core.object.get", args)
    switch_id = result["return"][0]["id"]
    return switch_id


if __name__ == "__main__":
    client = set_client()
    with client:
        try:
            if client:
                create_ui(client)
            else:
                print("Failed to connect to Wwise via WAAPI.")

            client.disconnect()

        except CannotConnectToWaapiException as e:
            print("Error connecting to Wwise: {}".format(e))
