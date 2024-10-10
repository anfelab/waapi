from waapi import CannotConnectToWaapiException
from wwise_helpers import show_error_message, show_message, show_success_message, set_client, get_selected_items
import argparse 

client = set_client()
# Define arguments for the script
# parser = argparse.ArgumentParser(description='Automatically create new play events from the selection and replicate the work unit hierarchy.')
# parser.add_argument('ids', metavar='GUID', nargs='*', help='One or many guid of the form {01234567-89ab-cdef-0123-4567890abcde}. The script retrieves the current selected if no GUID specified.')
# args = parser.parse_args()

def get_events_path(id) -> str:
    waql = f'from object "{id}" select this, ancestors'
    args = {
            "waql": waql,
            "options": {"return": ["notes"]}
        }
    result = client.call("ak.wwise.core.object.get", args)
    notes = ""
    if result["return"]:
        paths = []
        for obj in result["return"]:
            if obj["notes"]:
                notes = obj["notes"]
                parts = notes.split("\r\n")
                for part in parts:
                    if "\\Events\\" in part:
                        paths.append(part)
        if len(paths) == 1:
            return paths[0].strip()
        elif len(paths) > 1:
            return paths[-1].strip()
        else:
            show_error_message("No paths were returned")
            return

                    
def check_for_loop(id):
    is_loop = False
    waql = f'from object "{id}" select this, descendants where IsLoopingEnabled'
    args = {
            "waql": waql
        }
    result = client.call("ak.wwise.core.object.get", args)
    if result["return"]:
        is_loop = True
    else:
        is_loop = False
    return is_loop

def create_play_event(item_id, item_name, path="\\Events\\Default Work Unit"):
    args = {
        "parent": path,
        "type": "Event",
        "name": f"Play_{item_name}",
        "onNameConflict": "merge",  
        "children": [
            {
                "name": "",
                "type": "Action",
                "@ActionType": 1,
                "@Target": f"{item_id}"
                    }
                ]
    }
            

    result = client.call("ak.wwise.core.object.create", args)
    return result


# Create a function to create a Stop event for the selected items
def create_stop_event(item_id, item_name, path="\\Events\\Default Work Unit"):
    args = {
        "parent": path,
        "type": "Event",
        "name": f"Stop_{item_name}",
        "onNameConflict": "merge",  
        "children": [
            {
                "name": "",
                "type": "Action",
                "@ActionType": 2,
                "@Target": f"{item_id}",
                "@FadeTime": 1
            }
                ]
    }
    result = client.call("ak.wwise.core.object.create", args)
    return result

def main():
    with client:
        selected = get_selected_items(client)
        created = 0
        client.call("ak.wwise.core.undo.beginGroup")
        for item in selected:
            events_path = get_events_path(item["id"])
            is_looping = check_for_loop(item["id"])
            create_play_event(item["id"], item["name"], events_path)
            created += 1
            if is_looping:
                create_stop_event(item["id"], item["name"], events_path)
                created += 1

        if created > 0: 
            show_success_message(f"{created} Events were created!")
        else: 
            show_error_message("No Events were created!")
        
        client.call("ak.wwise.core.undo.endGroup", {"displayName": "Create Events for selected objects in specific path"})


if __name__ == "__main__":
    main()
