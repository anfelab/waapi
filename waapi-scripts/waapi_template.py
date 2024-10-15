from waapi import CannotConnectToWaapiException
from wwise_helpers import show_error_message, set_client, get_selected_items, show_success_message

#GLOBALS
client = set_client()

def main():
    
    try:
        with client:
            selected_items = get_selected_items(client)
            for item in selected_items:
                print(item["id"])

    except CannotConnectToWaapiException:
        show_error_message("Could not connect to Wwise Authoring API.")
        return None


if __name__ == "__main__":
    main()
