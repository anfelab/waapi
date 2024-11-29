from waapi import CannotConnectToWaapiException
from wwise_helpers import show_error_message, set_client, get_selected_items, show_success_message

def get_references(client, id):
    args = {
            "from": {"id": [id], },
            "options": {"return": ["id", "name", "referencesTo"]}
        }
    result = client.call("ak.wwise.core.object.get", args)
    print(result)

def main():
    try:
        client = set_client()
        with client:
            selected_items = get_selected_items(client)
            for item in selected_items:
                get_references(client, item["id"])

    except CannotConnectToWaapiException:
        show_error_message("Could not connect to Wwise Authoring API.")
        return None


if __name__ == "__main__":
    main()
