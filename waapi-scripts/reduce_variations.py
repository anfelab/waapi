from waapi import CannotConnectToWaapiException
from wwise_helpers import show_error_message, show_success_message, set_client, get_selected_items, ask_user_input_num
import re

var_num = ask_user_input_num("Variations", "Insert MAX number of variations: ")


def reduce_variations(client, item_id):
    waql = f'from object "{item_id}" select descendants where type = "Sound"'
    args = {
        "waql": waql
    }

    result = client.call("ak.wwise.core.object.get", args)
    reduce_list = []
    for obj in result["return"]:
        idx = re.split("_", obj["name"])
        idx = idx[-1]
        if idx.isdigit() and int(idx) > var_num:
            reduce_list.append(obj)

    for obj in reduce_list:
        args = {
            "object": obj["id"],
            "property": "Inclusion",
            "value": False
        }
        client.call("ak.wwise.core.object.setProperty", args)
    return reduce_list


def main():
    client = set_client()
    try:
        with client:
            selected_items = get_selected_items(client)
            changed = 0
            for item in selected_items:
                item_id = item[0]
                reduced = reduce_variations(client, item_id)
                changed += len(reduced)

            if changed > 0:
                show_success_message(f"Successfully reduced {changed} variations!")
            else:
                show_error_message("No changes were made!")

    except CannotConnectToWaapiException:
        show_error_message("Could not connect to Wwise Authoring API.")
        return None


if __name__ == "__main__":
    main()
