from waapi import CannotConnectToWaapiException
from wwise_helpers import show_error_message, set_client, get_selected_items, ask_user_input_str


def set_notes(client, item_id, notes):
    args = {
        "object": item_id,
        "value": f"{notes}"
    }
    result = client.call("ak.wwise.core.object.setNotes", args)


def main():
    client = set_client()
    try:
        with client:
            selected_items = get_selected_items(client)
            notes = ask_user_input_str("Input", "Enter the notes to inset to the items: ")
            if notes:
                for item in selected_items:
                    item_id = item["id"]
                    set_notes(client, item_id, notes)

    except CannotConnectToWaapiException:
        show_error_message("Could not connect to Wwise Authoring API.")
        return None


if __name__ == "__main__":
    main()
