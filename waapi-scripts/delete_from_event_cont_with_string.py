from waapi import CannotConnectToWaapiException
from wwise_helpers import show_success_message ,show_error_message, set_client, get_selected_items, ask_user_input_str


client = set_client()
remove_str = ask_user_input_str("Input", "Enter the pattern to match (for remove): ")
deleted = 0


def delete_containers_containing_string(id):
    waql = f'$ from object "{id}" select this, descendants where type = "Event"'
    args = {
        "waql": waql
    }

    result = client.call("ak.wwise.core.object.get", args)
    for obj in result["return"]:
        get_containers_from_events(obj)

def get_containers_from_events(obj):
    waql = f'$ from object "{obj["id"]}" select descendants'
    args = {
        "waql": waql,
        "options": {"return": ["id", "name", "@Target"]}}

    result = client.call("ak.wwise.core.object.get", args)
    for obj in result["return"]:
        if remove_str in obj["@Target"]["name"]:
            remove_reference(obj["id"])
            global deleted
            deleted += 1

def remove_reference(id):
    # pass
    result = client.call("ak.wwise.core.object.delete", {"object": id})
    

def main():
    try:
        with client:
            client.call("ak.wwise.core.undo.beginGroup")
            selected_items = get_selected_items(client)
            for item in selected_items:
                delete_containers_containing_string(item[0])

            if deleted: 
                show_success_message(f"Deleted {deleted} references!")
            else:
                show_error_message("No refereces were deleted!")

            client.call("ak.wwise.core.undo.endGroup", {"displayName": "Remove references containing string from event"})

    except CannotConnectToWaapiException:
        show_error_message("Could not connect to Wwise Authoring API.")
        return None
    
    finally:
        client.disconnect()

if __name__ == "__main__":
    main()
