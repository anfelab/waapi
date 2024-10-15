from waapi import CannotConnectToWaapiException
from wwise_helpers import show_error_message, set_client, get_selected_items, show_success_message
import re


#GLOBALS
client = set_client()


def create_parent(obj):
    name = obj["name"].split("_")
    if name[-1].isdigit():
        name.pop(-1)
    name.append("temp")    
    name = "_".join(name)
    args = {
        "parent": obj["parent"]["id"],
        "onNameConflict": "rename",
        "type": "BlendContainer",
        "name": name
    }
    result = client.call("ak.wwise.core.object.create", args)
    move_obj(obj, result)
    remove_temp_name(result)
    return result


def move_obj(obj, dest_obj):
    args = {
        "object": obj["id"],
        "parent": dest_obj["id"],
        "onNameConflict": "rename"
    }

    result = client.call("ak.wwise.core.object.move", args)
    return result


def remove_temp_name(obj):
    name = obj["name"].split("_")
    name.pop(-1)
    name = "_".join(name)
    args = {
        "object": obj["id"],
        "value": name
    }
    result = client.call("ak.wwise.core.object.setName", args)
    return result


def main():
    
    try:
        with client:
            client.call("ak.wwise.core.undo.beginGroup")
            selected_items = get_selected_items(client, "parent")
            created = 0
            for item in selected_items:
                created_obj = create_parent(item)
                created += 1

            client.call("ak.wwise.core.undo.endGroup", {"displayName": "Create new Switch Container parent with same name(s)"})
        if created:
            show_success_message(f"Succesfully created {created} object(s)!")
        else:
            show_error_message("No objects were created!")

    except CannotConnectToWaapiException:
        show_error_message("Could not connect to Wwise Authoring API.")
        return None


if __name__ == "__main__":
    main()
