from waapi import CannotConnectToWaapiException
from wwise_helpers import show_error_message, show_success_message, set_client
from wwise_helpers import get_selected_items


def delete_empty_containers(client, selected_obj_id):
    waql = f'from object "{selected_obj_id}" select this, descendants where (type = "RandomSequenceContainer" or ' \
           f'type = "SwitchContainer") and childrenCount = 0'
    args = {
        "waql": waql
    }
    result = client.call("ak.wwise.core.object.get", args)
    empty_items = result["return"]
    for item in empty_items:
        item_id = item["id"]
        del_args = {
            "object": item_id
        }
        del_result = client.call("ak.wwise.core.object.delete", del_args)
    return len(empty_items)


def main():
    client = set_client()
    try:
        with client:
            selected_obj = get_selected_items(client)
            for obj in selected_obj:
                selected_obj_id = obj[0]
                print(selected_obj_id)
                deleted = delete_empty_containers(client, selected_obj_id)
        if deleted:
            show_success_message(f"{deleted} empty containers were deleted!")
        else:
            show_error_message("No containers were deleted!")

    except CannotConnectToWaapiException:
        show_error_message("Could not connect to Wwise Authoring API.")
        return None


if __name__ == "__main__":
    main()
