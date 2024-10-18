from waapi import CannotConnectToWaapiException
from wwise_helpers import set_client, get_selected_items, show_error_message, \
    ask_user_input_num, show_success_message


def copy_objects(client, object_id):
    parent_list = get_selected_items(client, "parent")  # Import the list for the parent container
    if not parent_list:
        return
    parent_id = parent_list[0]["parent"]["id"]
    args = {
        "object": object_id,
        "onNameConflict": "rename",
        "parent": parent_id,
    }
    client.call("ak.wwise.core.object.copy", args)


def main():
    client = set_client()
    try:
        with client:
            selected_items = get_selected_items(client)
            if not selected_items:
                show_error_message("No items selected in Wwise.")
                return
            times = ask_user_input_num()  # Ask once for all items
            for item in selected_items:
                object_id = item["id"]  # Assuming each item has an 'id' key
                for _ in range(times):
                    copy_objects(client, object_id)
                show_success_message(f"Item {item[1]} copied {times} times!")

    except CannotConnectToWaapiException:
        show_error_message("Could not connect to Wwise Authoring API.")
        return None
    
    finally:
            client.disconnect()

if __name__ == "__main__":
    main()
