from waapi import CannotConnectToWaapiException
from wwise_helpers import show_error_message, show_success_message, set_client, get_selected_items, \
    ask_user_input_str
import os
import re
import shutil

destination_folder = ask_user_input_str("Enter Path",
                                        "Enter the path to backup the files: \n Default = D:\\file_backup")
if not destination_folder:
    destination_folder = "D:\\file_backup"


def get_sound_children(client, id):
    waql = f'from object "{id}" select this, descendants where (type = "Sound" or type = "Voice") and sound:OriginalWavFilePath != ""'
    args = {
        "waql": waql,
        "options": {"return": ["id", "name", "sound:originalWavFilePath","parent"]}
    }
    result = client.call("ak.wwise.core.object.get", args)
    if result:
        backup_files = []
        for item in result["return"]:
            backup_obj = {"file": item["sound:originalWavFilePath"], "folder": item["parent"]["name"]}
            backup_files.append(backup_obj)
        return backup_files


def backup_files(files):
    backup_files = []
    files_copied = 0
    for file in files:
        filename = file["file"].split("\\")[-1]
        folder_name = file["folder"]
        backup_file = {"filename": filename, "folder": folder_name}
        backup_files.append(backup_file)
        

    for file in files:
        # Extract the file name from the file path
        filename = os.path.basename(file["file"])
        if "type" in filename:
            pattern = r'_type\d{2}(_\d{2})?\.wav'
            folder_name = re.sub(pattern,"",filename)
        else:
            pattern = r'(_\d{2})?\.wav'
            folder_name = re.sub(pattern,"",filename)
        
        print(folder_name)
        # Create the full destination file path
        dest_file_path = os.path.join(destination_folder, folder_name)
        path_exist = os.path.exists(dest_file_path)
        if not path_exist:
            os.mkdir(dest_file_path)
        dest_file_path = os.path.join(destination_folder, folder_name, filename)
        if os.path.exists(dest_file_path):
            continue
        # Copy the file to the new destination
        shutil.copy(file["file"], dest_file_path)
        files_copied += 1

    return files_copied



def main():
    client = set_client()
    path_exist = os.path.exists(destination_folder)
    if not path_exist:
        os.mkdir(destination_folder)
    try:
        with client:
            selected_items = get_selected_items(client)
            for item in selected_items:
                id = item["id"]
                files = get_sound_children(client, id)
                copied = backup_files(files)

        if copied > 0:
            show_success_message(f"{copied} files backup made successfully")
        else:
            show_error_message("No files were copied!")


    except CannotConnectToWaapiException:
        show_error_message("Could not connect to Wwise Authoring API.")
        return None
    
    finally:
        client.disconnect()

if __name__ == "__main__":
    main()
