from waapi import CannotConnectToWaapiException
from wwise_helpers import show_error_message, set_client, show_success_message
import tkinter as tk
from tkinter import ttk

# GLOBALS:
client = set_client()
origin = None
dest = None
switches = None


# FUNCTIONS:

def set_dpi_awareness():
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass


def get_selected_from_ui():
    args = {"options": {"return": ["id", "name", "path", "parent"]}}
    result = client.call("ak.wwise.ui.getSelectedObjects", args)
    if result:
        return result["objects"]
    else:
        show_error_message("No items selected!")
        return None


def get_all_switch_groups():
    args = {
        "from": {"ofType": ["SwitchGroup"]},
        "options": {"return": ["id", "name"]}
    }
    result = client.call("ak.wwise.core.object.get", args)
    switch_groups = [item['name'] for item in result['return']]
    return switch_groups


def get_switch_containers(path):
    waql = f'from object "{path}" select descendants where type = "SwitchContainer"'
    args = {
        "waql": waql,
    }
    result = client.call("ak.wwise.core.object.get", args)
    return result["return"]


def get_switch_group(id):
    args = {
        "from": {"id": [id]},
        "options": {"return": ["SwitchGroupOrStateGroup"]}
    }
    result = client.call("ak.wwise.core.object.get", args)
    if result:
        return result["return"][0]["SwitchGroupOrStateGroup"]
    
def get_switch_to_assign(switch_group_name):
    waql = f'from type Switch where parent.name = "{switch_group_name}"'
    args = {
        "waql": waql
    }
    result = client.call("ak.wwise.core.object.get", args)
    switches = [item['name'] for item in result['return']]
    return switches

def assign_container_to_switch(child_id, target_id):
    target = find_specific_switch()
    print(target)
    args = {
        "child": child_id,
        "stateOrSwitch": target_id
    }
    client.call("ak.wwise.core.switchContainer.addAssignment", args)

def copy_item(origin, dest_id):
    if origin != dest_id:
        args = {
            "object": origin,
            "parent": dest_id,
            "onNameConflict": "replace"
        }
        result = client.call("ak.wwise.core.object.copy", args)
        return result

def find_specific_switch():
    parent_name = sw_group_var.get()
    child_name = switch.get()
    waql = f'from type switch where name = "{child_name}" and parent.name = "{parent_name}"'
    # print(waql)
    args = {"waql":waql}
    result = client.call("ak.wwise.core.object.get", args)
    return result["return"]

def update_origin_path():
    global origin
    origin = get_selected_from_ui()
    origin_path.set(origin[0]["path"])
    return origin


def update_dest_path():
    global dest
    dest = get_selected_from_ui()
    dest_path.set(dest[0]["path"])
    return dest

def update_switches(event):
    global switches
    name = sw_group_var.get()
    switches = get_switch_to_assign(name)
    sw_child_dropdown['values'] = switches 
    return switches 


def main():
    if not dest_path or not origin_path:
        show_error_message("Invalid path!")
        raise ValueError("Invalid path!")

    if is_switch.get():
        copied = 0
        client.call("ak.wwise.core.undo.beginGroup")
        dest_switch_containers = get_switch_containers(dest[0]["path"])
        for cont in dest_switch_containers:
            cont_ref = get_switch_group(cont["id"])
            if sw_group_var.get() == cont_ref["name"] and origin[0]["parent"]["id"] != cont["id"]:
                target = find_specific_switch()
                result = copy_item(origin[0]["id"], cont["id"])
                assign_container_to_switch(result["id"], target[0]["id"])
                copied += 1
        if copied > 0:
            show_success_message(f"Copied in {copied} places!")
        else:
            show_error_message("No items were copied!")

        client.call("ak.wwise.core.undo.endGroup", {'displayName': 'Copy Item to Multiple Containers'})
    client.disconnect()

# UI Elements:

root = tk.Tk()
root.title("Copy item to different paths based on conditions")
# Origin Label
origin_path = tk.StringVar()
origin_label = ttk.Label(root, text="Enter the path of the container to copy:", padding=(50, 15))
origin_path_entry = ttk.Entry(root, width=50, textvariable=origin_path)
blocate_origin = ttk.Button(root, text="Get Selected", command=lambda: update_origin_path())

dest_path = tk.StringVar()
origin_label.grid(column=0, row=0, padx=15, sticky="EW")
origin_path_entry.grid(column=1, row=0, padx=15)
blocate_origin.grid(column=2, row=0, columnspan=2, padx=15)
origin_path_entry.focus()

# Destiny Label
dest_label = ttk.Label(root, text="Enter the path to scan for file copy:", padding=(50, 15))
dest_path_entry = ttk.Entry(root, width=50, textvariable=dest_path)
blocate_dest = ttk.Button(root, text="Get Selected", command=lambda: update_dest_path())

dest_label.grid(column=0, row=1, padx=15, sticky="EW")
dest_path_entry.grid(column=1, row=1, padx=15)
blocate_dest.grid(column=2, row=1, columnspan=2, padx=15)

# Conditionals
cond_sw_label = ttk.Label(root, text = "Conditions for copy arguments:", padding = (50,15))
is_switch = tk.BooleanVar()
sw_checkbox = ttk.Checkbutton(root, text="IsSwitch", padding= (50,15), variable= is_switch)
sw_group_var = tk.StringVar()
switch_groups = get_all_switch_groups()
sw_dropdown = ttk.Combobox(root, textvariable=sw_group_var, values=switch_groups)
sw_label = ttk.Label(root, text="Enter the switch group that needs to match:", padding=(50, 15))
switch = tk.StringVar()
sw_label_2 = ttk.Label(root, text="Switch to assign to the copied container:", padding=(50, 15))
sw_child_dropdown = ttk.Combobox(root, textvariable=switch, values=switches)

sw_checkbox.grid(column=1, row= 3, sticky= "EW")
cond_sw_label.grid(column=0, row=4, sticky= "EW")
sw_label.grid(column=0, row=4, sticky="EW")
sw_dropdown.grid(column=1, row=4, sticky="NSEW", padx=15, pady=15)
sw_dropdown.bind("<<ComboboxSelected>>", update_switches)

sw_label_2.grid(column=0, row=5, sticky="EW")
sw_child_dropdown.grid(column=1, row=5, sticky="NSEW", padx=15, pady=15)


# Main button
main_btn = ttk.Button(root, text="Copy Item", command=main)
main_btn.grid(column=3, row=5, columnspan=2, padx=15, pady=15, sticky="NS")



if __name__ == "__main__":
    with client:
        try:
            root.mainloop()
        except CannotConnectToWaapiException:
            show_error_message("Could not connect to Wwise Authoring API.")

        finally:
            client.disconnect()