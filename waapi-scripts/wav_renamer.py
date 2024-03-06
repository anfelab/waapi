from wwise_helpers import show_error_message, set_client, show_success_message
import os
from waapi import WaapiClient, CannotConnectToWaapiException


def get_selected_objects(client):
    # Get selected objects
    result = client.call("ak.wwise.ui.getSelectedObjects")
    return result["objects"]


def get_wav_path(client, obj_id):
    args = {
        "from": {"id": [obj_id]},
        "transform": [{"select": ["descendants"]}],
        "options": {"return": ["originalWavFilePath"]}
    }
    result = client.call("ak.wwise.core.object.get", args)
    return result["return"][0]["originalWavFilePath"]

def rename_wav_file(wav_path, new_name):
    if os.path.exists(wav_path):
        # Get the directory of the wav file
        wav_dir = os.path.dirname(wav_path)
        # Get the extension of the wav file
        wav_ext = os.path.splitext(wav_path)[1]
        # Create the new path for the wav file
        new_wav_path = os.path.join(wav_dir, new_name + wav_ext)
        # Rename the file
        os.rename(wav_path, new_wav_path)
        return new_wav_path
    else:
        return None


def main():
    client = set_client()
    try:
        with client:
            # Get selected objects
            selected_objects = get_selected_objects(client)
            for obj in selected_objects:
                obj_id = obj["id"]
                wav_path = get_wav_path(client, obj_id)
                print(wav_path)

            show_success_message("Task completed successfully.")
    except CannotConnectToWaapiException:
        show_error_message("Could not connect to Wwise. Please make sure Wwise is running and try again.")


if __name__ == "__main__":
    main()


