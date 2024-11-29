from waapi import CannotConnectToWaapiException
from wwise_helpers import show_error_message, set_client, ask_user_input_str, get_selected_items, show_success_message

client = set_client()
# Define a dictionary to map abbreviations to full container names
container_types = {
    "a": "ActorMixer",
    "b": "BlendContainer",
    "f": "Folder",
    "sw": "SwitchContainer",
    "r": "RandomSequenceContainer"
}
# Check if the container_type is valid
container_type = ask_user_input_str("Input: ", r"""Enter the container type\n 
    "a": "ActorMixer",
    "b": "BlendContainer",
    "f": "Folder",
    "sw": "SwitchContainer",
    "r": "RandomSequenceContainer""")
if container_type not in container_types:
    show_error_message("Invalid container type. Please enter a valid type: r, sw, b, a, f")
    container_type = ask_user_input_str("Input: ", r"""Enter the container type\n 
    "a": "ActorMixer",
    "b": "BlendContainer",
    "f": "Folder",
    "sw": "SwitchContainer",
    "r": "RandomSequenceContainer""")

def get_children(id):
    waql = f'from object "{id}" select children'
    args = {
        "waql": waql
    }
    result = client.call("ak.wwise.core.object.get", args)
    return result["return"]

def rename_old_parent(id, name):
    args = {
        "object": id,
        "value": name+"_old"
        }
    result = client.call("ak.wwise.core.object.setName", args)
    return result

def create_new_parent(parent, name):
    args = {
        "parent": parent["id"],
        "type": container_types[container_type],
        "name": name,
        "onNameConflict": "merge"
    }
    result = client.call("ak.wwise.core.object.create", args)
    print(result)
    return result

def move_children(id, parent):
    args = {
        "object": id,
        "parent": parent,
        "onNameConflict": "rename"
    }
    result = client.call("ak.wwise.core.object.move", args)

def remove_old_parent(id):
    args = {
        "object": id,
        }
    result = client.call("ak.wwise.core.object.delete", args)
    return result


def main():
    try:
        with client:
            changed = 0
            selected_items = get_selected_items(client, "parent", "type")
            client.call("ak.wwise.core.undo.beginGroup")
            for item in selected_items:
                rename_old_parent(item["id"], item["name"])
                new_parent = create_new_parent(item["parent"], item["name"])
                children = get_children(item["id"])
                for child in children:
                    move_children(child["id"], new_parent["id"])
                remove_old_parent(item["id"])
                changed += 1
            
            client.call("ak.wwise.core.undo.endGroup",{"displayName":"Replace parent to new type"})
            if changed:
                show_success_message(f"{changed} items were changed!")
            else:
                show_error_message("No items were changed!")

    except CannotConnectToWaapiException:
        show_error_message("Could not connect to Wwise Authoring API.")
        return None

if __name__ == "__main__":
    main()
