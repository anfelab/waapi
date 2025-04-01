from waapi import CannotConnectToWaapiException
from wwise_helpers import show_error_message, set_client, get_selected_items, show_success_message
import os

def get_wav_paths(client, item_id):
    args = {
        "waql": f'from object "{item_id}" select this, descendants where type = '
                f'"Sound" and sound:OriginalWavFilePath != "" ',
        "options": {"return": ["id", "name", "path", "sound:originalWavFilePath"]}
    }
    result = client.call("ak.wwise.core.object.get", args)
    return result["return"]


def compare_names(client, sounds):
    changed = 0
    for item in sounds:
        wwise_name = os.path.split(item["path"])
        filename = os.path.split(item["sound:originalWavFilePath"])
        filename = filename[-1]
        temp_filename = filename.split(".")
        temp_filename = temp_filename[-2]

        if wwise_name[-1] != temp_filename:
            new_name = os.path.split(item["sound:originalWavFilePath"])
            file = wwise_name[-1] + ".wav"
            new_name = os.path.join(new_name[0], file)
            if os.path.exists(new_name):
                print(f"{file} already exists")
            else:
                rename_wav(item["sound:originalWavFilePath"], new_name)

            change_wwise_path(client, item, new_name)
            changed += 1
    return changed


def rename_wav(old_name, new_name):
    print(f'{old_name}\n Renamed to: \n {new_name}')
    os.rename(old_name, new_name)


def change_wwise_path(client, item, new_path):
    new_path = new_path.replace("\\", "/")
    path = item["path"].split("\\")
    last = "<Sound SFX>" + path[-1]
    path[-1] = last
    path = "\\".join(path)
    lang = "SFX"
    import_sfx_args = {
        "importOperation": "replaceExisting",
        "autoAddToSourceControl": True,
        "default": {
            "importLanguage": lang
        },
        "imports": [
            {
                "audioFile": new_path,
                "objectPath": path,
            }
        ]
    }
    client.call("ak.wwise.core.audio.import", import_sfx_args)


def main():
    client = set_client()
    try:
        with client:
            renamed = 0
            selected_items = get_selected_items(client)
            for item in selected_items:
                item_id = item["id"]
                sounds = get_wav_paths(client, item_id)
                renamed += compare_names(client, sounds)

        if renamed:
            show_success_message(f"Succesfully {renamed=} items")
        else:   
            show_error_message("No items were renamed")
    except CannotConnectToWaapiException:
        show_error_message("Could not connect to Wwise Authoring API.")


if __name__ == "__main__":
    main()
