from waapi import WaapiClient, CannotConnectToWaapiException
from wwise_helpers import set_client, get_selected_items, get_selected_items_type, show_error_message, show_message, show_success_message, ask_user_input_str

def get_parent(client):
    result = get_selected_items_type(client,"parent")
    parent_list = []
    for parent in result:
        parent_list.append(parent["parent"])
    return parent_list

def get_names_without_index(client):
    items = get_selected_items(client)  # Assuming this function returns a list of tuples (id, name)
    names = []
    names_no_idx = []

    for item in items:
        names.append(item[1])  # Extracting names from items

    for name in names:
        name_parts = name.split("_")
        if name_parts[-1].isnumeric():
            name_parts.pop()  # Remove the numeric index
            name_no_idx = "_".join(name_parts)  # Re-join the remaining parts
            names_no_idx.append(name_no_idx)
        else:
            names_no_idx.append(name)  # Append the original name if no numeric index

    names_no_idx = set(names_no_idx)  # Convert to a set for uniqueness
    return names_no_idx

def create_new_parent(client,container_type, parent_list, names):
    # Define a dictionary to map abbreviations to full container names
    container_types = {
        "a": "ActorMixer",
        "b": "BlendContainer",
        "f": "Folder",
        "sw": "SwitchContainer",
        "r": "RandomSequenceContainer"
    }
    # Check if the container_type is valid
    if container_type not in container_types:
        show_error_message("Invalid container type. Please enter a valid type: r, sw, b, a, f")
        container_type = ask_user_input_str("Input: ", "Enter the container type...")
    else:
        # Retrieve the full name of the container type
        container_type = container_types[container_type]
        created_objs = []
        for parent in parent_list:
            for name in names:
                args = {
                    "parent": parent["id"],
                    "type": container_type,
                    "name": name,
                    "onNameConflict":"merge"
                }
                result = client.call("ak.wwise.core.object.create",args)
                if result:
                    created_objs.append(result)
        return created_objs

def move_objects(client, children_list, created_objs):
    parent_names = [obj["name"] for obj in created_objs]
    parent_ids = [obj["id"] for obj in created_objs]
    for child in children_list:
        child_name = child[1]
        child_id = child[0]
        match_found, idx_match = look_for_match(child_name, parent_names)  # Use the revised look_for_match function
        if match_found:
            # print(f"Found a match for '{child_name}' in index {idx_match}")
            # Assuming you want to use the match to do something, like move the child to the matched parent
            args = {
                "object": child_id,
                "parent": parent_ids[idx_match],
            }
            client.call("ak.wwise.core.object.move",args)
        else:
            print(f"No match found for '{child_name}'")

def look_for_match(child_name, parent_names):
    for index, parent_name in enumerate(parent_names):
        if child_name.startswith(parent_name) and len(child_name) > len(parent_name):
            return True, index
    return False, -1

def main():
    client = set_client()
    try:
        parent_list = get_parent(client)
        if not parent_list:
            show_error_message("No parent selected.")
            return

        names = get_names_without_index(client)
        if not names:
            show_error_message("No names obtained from selected items.")
            return

        children_list = get_selected_items(client)
        if not children_list:
            show_error_message("No children selected.")
            return

        container_type_input = ask_user_input_str("Input: ", "Enter the container type (r, sw, b, a, f):")
        created_objs = create_new_parent(client, container_type_input, parent_list, names)
        if created_objs:
            move_objects(client, children_list, created_objs)
            show_success_message("New parent(s) created and children moved successfully.")
    except CannotConnectToWaapiException:
        show_error_message("Could not connect to Wwise Authoring API.")

if __name__ == "__main__":
    main()
