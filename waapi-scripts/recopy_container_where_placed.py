from waapi import CannotConnectToWaapiException
from wwise_helpers import show_error_message, set_client, get_selected_items, show_success_message

def get_copies(client, id, name):
    waql = f'where !(id = "{id}") and name = "{name}"'
    args = {
        "waql": waql,
        "options": {"return": ["id", "name", "parent"]}
    }
    result = client.call("ak.wwise.core.object.get", args)
    print(result["return"])
    return result["return"]

def delete_copy(client, id):
    args = {"object": id}
    client.call("ak.wwise.core.object.delete", args)

def copy_item(client, id, parent):
    args = {
        "object": id,
        "parent": parent["id"],
        "onNameConflict": "replace",
    }
    client.call('ak.wwise.core.object.copy', args)
    

def main():
    try:
        client = set_client()
        with client:
            selected_items = get_selected_items(client)
            client.call("ak.wwise.core.undo.beginGroup")
            copied = 0
            for item in selected_items:
                copies = get_copies(client, item["id"], item["name"])
                for i in copies: 
                    if i["id"] and i["parent"] and i["id"]:
                        delete_copy(client, i["id"])
                        copy_item(client, item["id"], i["parent"])
                        copied += 1
                    else:
                        show_error_message("No items copied")
                        client.call("ak.wwise.core.undo.cancelGroup")
            if copied:
                show_success_message(f"Copied {copied} items")

            client.call("ak.wwise.core.undo.endGroup", {"displayName": "Re-Copy Item in previous places"})


    except CannotConnectToWaapiException:
        show_error_message("Could not connect to Wwise Authoring API.")
        return None


if __name__ == "__main__":
    main()
