from waapi import WaapiClient, CannotConnectToWaapiException
from wwise_helpers import show_error_message, ask_user_input_str, get_selected_items_type

#Set the WAAPI client
def set_client(ip="127.0.0.1", port=8080):
    waapi_port = f"ws://{ip}:{port}/waapi"
    client = WaapiClient(waapi_port)
    return client

def rename_objects(client, id_list):
    new_name = ask_user_input_str()  # Get the new base name from the user once
    total_items = len(id_list)

    for idx, object_id in enumerate(id_list, start=1):  # Start indexing from 1
        # Apply suffix only if more than one item is selected
        suffix = f"_{idx:02}" if total_items > 1 else ""
        args = {
            "object": object_id["id"],
            "value": f"{new_name}{suffix}"
        }
        client.call("ak.wwise.core.object.setName", args)
    print(f"Renamed {total_items} items.")

def main():
    try:
        client = set_client()
        with client:
            id_list = get_selected_items_type(client,"id")
            
            if not id_list:
                show_error_message("No items selected!")
                return  # Exit if no items are selected
            else:
                print(id_list)
                rename_objects(client, id_list)

    except CannotConnectToWaapiException:
            show_error_message("Could not connect to Wwise Authoring API.")
            return None

if __name__ == "__main__":
    main()
