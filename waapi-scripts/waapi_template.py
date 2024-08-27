from waapi import CannotConnectToWaapiException
from wwise_helpers import show_error_message, set_client, get_selected_items


def main():
    client = set_client()
    try:
        with client:
            selected_items = get_selected_items(client)
            for item in selected_items:
                item_id = item[0]
                print(item_id)
                client.call("ak.soundengine.postMsgMonitor", {"message": f"Hello Wwise!"})

    except CannotConnectToWaapiException:
        show_error_message("Could not connect to Wwise Authoring API.")
        return None


if __name__ == "__main__":
    main()
