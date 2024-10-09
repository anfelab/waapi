from waapi import CannotConnectToWaapiException
from wwise_helpers import show_error_message, show_success_message, set_client, get_selected_items
from pydub import AudioSegment


def get_volume_dif(client, item_id):
    waql = f'from object "{item_id}" select this, descendants where (type = "Sound" or type = "Voice") ' \
           f'and sound:OriginalWavFilePath != ""'
    args = {
        "waql": waql,
        "options": {"return": ["id", "name", "parent", "volume", "sound:OriginalWavFilePath", "notes"]}
    }
    result = client.call("ak.wwise.core.object.get", args)
    reset_list = []
    for target in result["return"]:
        volume = 0.0
        path = target["sound:OriginalWavFilePath"]
        if target["volume"] != 0 and target["notes"] != "@ignore":
            volume += target["volume"]
            reset_list.append(target)

        parent_waql = f'from object "{target["id"]}" select ancestors where volume != 0 and notes != "@ignore"'
        parent_args = {
            "waql": parent_waql,
            "options": {"return": ["id", "name", "volume", "notes"]}
        }
        vol_result = client.call("ak.wwise.core.object.get", parent_args)
        for item in vol_result["return"]:
            if item["notes"] != "@ignore":
                volume += item["volume"]
                reset_list.append(item)
                print(f'{target["name"]} volume changed by {volume}dB!')
        adjust_wav_volume(path, volume)

    return reset_list


def adjust_wav_volume(path, volume):
    file = AudioSegment.from_wav(path)
    new_file = file + volume
    # Save the output
    new_file.export(path, "wav")


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
            selected_items = get_selected_items(client)
            total = 0
            for item in selected_items:
                item_id = item["id"]
                reset_list = get_volume_dif(client, item_id)
                changed = reset_volumes(client, reset_list)
                total += changed
                
        if total == 0:
            show_error_message("No items were changed!")
        else:
            show_success_message(f"{total} items were changed!")
    except CannotConnectToWaapiException:
        show_error_message("Could not connect to Wwise Authoring API.")
        return None


if __name__ == "__main__":
    main()
