from waapi import WaapiClient, CannotConnectToWaapiException
from wwise_helpers import show_error_message, show_message, show_success_message, set_client, get_selected_items


def get_wav_paths(client, item_id):
    args = {
        "waql": "\"\\Actor-Mixer Hierarchy\" select descendants where type = 'Sound'",
        "options": {"return": ["id, name"]}
    }
    result = client.call("ak.wwise.core.object.get", args)
    print(result)


def main():
    client = set_client()
    try:
        with client:
            selected_items = get_selected_items(client)
            for item in selected_items:
                item_id = item[0]
                get_wav_paths(client, item_id)

    except CannotConnectToWaapiException:
        show_error_message("Could not connect to Wwise Authoring API.")
        return None


if __name__ == "__main__":
    main()
