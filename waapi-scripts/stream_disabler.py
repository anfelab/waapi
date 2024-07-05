from waapi import WaapiClient, CannotConnectToWaapiException
from wwise_helpers import show_error_message, show_message, show_success_message, set_client, get_selected_items


def get_sound_or_voice_children(client, item_id):
    waql = f'$ from object "{item_id}" select descendants where type = "Sound" or "Voice"'
    args = {
        "waql": waql
    }
    result = client.call("ak.wwise.core.object.get", args)
    if result:
        return result["return"]
    else:
        show_error_message("No valid Sound or Voice in the selection")


def check_for_stream(client, child_id, child_name):
    # Check if the sound is streaming
    args = {
        "from": {"id": [child_id]},
        "options": {"return": ["IsStreamingEnabled"]}
    }

    check_stream = client.call("ak.wwise.core.object.get", args)
    is_stream = check_stream["return"][0]["IsStreamingEnabled"]
    if not is_stream:
        print(f"Streaming is already disabled for {child_name}")
        return
    else:
        disable_stream(client, child_id, child_name)


def disable_stream(client, child_id, child_name):
    args = {
        "objects": [{
            "object": child_id,
            "@IsStreamingEnabled": "False",
            "@IsZeroLatency": "False"
        }],

    }
    client.call("ak.wwise.core.object.set", args)

    print(f"Streaming is now disabled for {child_name}")


def main():
    client = set_client()
    try:
        with client:
            selected_items = get_selected_items(client)
            for item in selected_items:
                item_id = item[0]
                children = get_sound_or_voice_children(client, item_id)
                changed_items = 0
                for child in children:
                    child_id = child["id"]
                    child_name = child["name"]
                    check_for_stream(client, child_id, child_name)
                    changed_items += 1

        show_success_message(f"Stream disabled for {changed_items} selected item(s)")
        client.disconnect()

    except CannotConnectToWaapiException as e:
        print("Error connecting to Wwise: {}".format(e))
        client.disconnect()


if __name__ == "__main__":
    main()
