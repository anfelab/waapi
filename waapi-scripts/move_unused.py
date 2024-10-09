from waapi import CannotConnectToWaapiException
from wwise_helpers import show_error_message, show_message, show_success_message, set_client, get_selected_items


def check_for_unused(client, item_id):
    waql = f'from object "{item_id}" select this, descendants where Inclusion = false and ' \
           f'(parent.type = "ActorMixer" or parent.type = "Folder")'
    args = {
        "waql": waql,
        "options": {"return": ["id", "name", "parent", "isIncluded"]}
    }
    result = client.call("ak.wwise.core.object.get", args)
    unchecked_items = [item for item in result["return"] if not item["isIncluded"]]
    return unchecked_items


def move_items(client, item_id, new_location):
    args = {
        "object": item_id,
        "parent": new_location
    }
    result = client.call("ak.wwise.core.object.move", args)
    return result


def set_not_included(client, item_id):
    args = {
        "object": item_id,
        "property": "Inclusion",
        "value": False
    }
    result = client.call("ak.wwise.core.object.setProperty", args)


def create_folder(client, unused):
    moved = 0
    for item in unused:
        item_id = item["id"]
        parent = item["parent"]["id"]
        args = {
            "parent": parent,
            "type": "Folder",
            "name": "unused",
            "onNameConflict": "merge",
        }
        result = client.call("ak.wwise.core.object.create", args)
        new_location = result["id"]
        set_not_included(client, new_location)
        if move_items(client, item_id, new_location):
            moved += 1
    return moved


def main():
    client = set_client()
    try:
        with client:
            selected_items = get_selected_items(client)
            for item in selected_items:
                item_id = item["id"]
                unused = check_for_unused(client, item_id)
                moved = create_folder(client, unused)
            if moved > 0:
                show_success_message(f"{moved} Items were moved to an unused folder")
            else:
                show_error_message("No items were moved!")
    except CannotConnectToWaapiException:
        show_error_message("Could not connect to Wwise Authoring API.")
        return None


if __name__ == "__main__":
    main()
