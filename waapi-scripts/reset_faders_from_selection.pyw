from waapi import CannotConnectToWaapiException
from wwise_helpers import show_error_message, set_client, get_selected_items, show_success_message


def get_reset_list(client, item_id):
    waql = f'from object "{item_id}" select descendants where volume != 0 and notes != "@ignore"'
    args = {"waql": waql}
    result = client.call("ak.wwise.core.object.get", args)
    reset_list = result["return"]
    return reset_list


def reset_volumes(client, reset_list):
    changed = 0
    for reset_obj in reset_list:
        reset_args = {
            "object": reset_obj["id"],
            "property": "Volume",
            "value": 0
        }
        client.call("ak.wwise.core.object.setProperty", reset_args)
        changed += 1
    return changed


def main():
    client = set_client()
    try:
        with client:
            total_changes = 0
            selected_items = get_selected_items(client)
            for item in selected_items:
                item_id = item[0]
                reset_list = get_reset_list(client, item_id)
                changed = reset_volumes(client, reset_list)
                total_changes += changed

            if total_changes == 0:
                show_error_message("No items were changed!")
            else:
                show_success_message(f"{total_changes} items were reset to 0dB!")

    except CannotConnectToWaapiException:
        show_error_message("Could not connect to Wwise Authoring API.")
        return None


if __name__ == "__main__":
    main()
