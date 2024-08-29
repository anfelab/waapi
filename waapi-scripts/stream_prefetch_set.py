from waapi import CannotConnectToWaapiException
from wwise_helpers import show_error_message, show_success_message, set_client, get_selected_items, \
    ask_user_input_num


def get_sound_or_voice_children(client, item_id):
    waql = f'$ from object "{item_id}" select this, descendants where type = "Sound" or "Voice"'
    args = {
        "waql": waql
    }
    result = client.call("ak.wwise.core.object.get", args)
    if result:
        return result["return"]
    else:
        show_error_message("No valid Sound or Voice in the selection")


def set_prefetch(client, child_id, child_name, user_input):
    # Check if the sound is streaming
    args = {
        "from": {"id": [child_id]},
        "options": {"return": ["IsStreamingEnabled"]}
    }

    check_stream = client.call("ak.wwise.core.object.get", args)
    is_stream = check_stream["return"][0]["IsStreamingEnabled"]
    if is_stream:
        args = {
            "objects": [{
                "object": child_id,
                "@IsZeroLatency": "True",
                "@PreFetchLength": user_input
            }],

        }
        client.call("ak.wwise.core.object.set", args)
        print(f"Prefetch is set to {user_input}ms for {child_name}")
    else:
        raise Exception("Asset is not set for streaming")


def main():
    client = set_client()
    try:
        with client:
            client.subscribe()
            user_input = ask_user_input_num("Message", "Enter the desired prefetch length in ms")
            selected_items = get_selected_items(client)
            for item in selected_items:
                item_id = item[0]
                children = get_sound_or_voice_children(client, item_id)
                changed_items = 0
                for child in children:
                    child_id = child["id"]
                    child_name = child["name"]
                    set_prefetch(client, child_id, child_name, user_input)
                    changed_items += 1

        show_success_message(f"Prefetch value set to {user_input}ms for {changed_items} selected item(s)")
        client.unsubscribe()
        client.disconnect()

    except CannotConnectToWaapiException as e:
        print("Error connecting to Wwise: {}".format(e))
        client.unsubscribe()
        client.disconnect()


if __name__ == "__main__":
    main()