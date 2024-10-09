from waapi import CannotConnectToWaapiException
from wwise_helpers import show_error_message, set_client, get_selected_items, show_success_message


def get_sfx(client, item):
    waql = f'from object "{item["id"]}" select this, descendants where type = "Sound"'
    args = {
        "waql": waql
    }
    result = client.call("ak.wwise.core.object.get", args)
    return result["return"]


def del_sfx(client, items):
    for item in items:
        args = {
            "object": item["id"]
        }
        client.call("ak.wwise.core.object.delete", args)


def main():
    client = set_client()
    try:
        with client:
            total = 0
            selected_items = get_selected_items(client)
            for item in selected_items:
                del_items = get_sfx(client, item)
                del_sfx(client, del_items)
                total += len(del_items)

            if total == 0:
                show_error_message("No items were deleted!")
            else:
                show_success_message(f"{total} items were deleted!")


    except CannotConnectToWaapiException:
        show_error_message("Could not connect to Wwise Authoring API.")
        return None


if __name__ == "__main__":
    main()
