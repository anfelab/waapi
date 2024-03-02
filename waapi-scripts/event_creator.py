from waapi import WaapiClient, CannotConnectToWaapiException
from wwise_helpers import show_error_message, show_message, show_success_message, set_client

# Create a function using waapi to get the id, name and path of the selected items in Wwise
def get_selected_items(client):
    args = {"options": {"return":["id", "name", "path"]}}
    result = client.call("ak.wwise.ui.getSelectedObjects", args)
    selected_items = []
    if "objects" in result:
        for obj in result["objects"]:
            obj_name = obj["name"]
            obj_id = obj["id"]
            obj_path = obj["path"]
            selected_items.append((obj_id, obj_name, obj_path))
        if not selected_items:
            show_error_message("No items selected.")
            return None
        return selected_items
    else:
        show_error_message("No items selected.")
        return None
# Creacte a function to create a Play event for the selected items
def create_play_event(client, item_id, item_name, wu_name):
    try:
        args = {
            "parent": "\\Events\\Default Work Unit",
            "type": "Folder",
            "name": f"{wu_name}",
            "onNameConflict": "merge",
            "children": [
                {
                    "type": "Event",
                    "name": f"Play_{item_name}",
                    "children": [
                        {
                            "name": "",
                            "type": "Action",
                            "@ActionType": 1,
                            "@Target": f"{item_id}"
                        }
                    ]
                }
            ]
        
        }
        result = client.call("ak.wwise.core.object.create", args)
        return result
    except Exception as e:
        print(f'Error: {e}')

# Create a function to create a Stop event for the selected items
def create_stop_event(client, item_id, item_name, wu_name):
    try:
        args = {
            "parent":"\\Events\\Default Work Unit",
            "type": "Folder",
            "name": f"{wu_name}",
            "onNameConflict": "merge",
            "children": [
        {
            "type": "Event",
            "name": f"Stop_{item_name}",
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
    ]

    
        }
        result = client.call("ak.wwise.core.object.create", args)
        return result
    except Exception as e:
        print(f'Error: {e}')
        
# Create a function to check if the selected item or one of its children is looping
def is_looping(client, item_id):
    is_loop = False
    try: 
        args = {
            "from": {"id": [item_id]},
            "transform": [{"select": ["descendants"]}],
            "options":{ "return":["@IsLoopingEnabled"]}
        }
        result = client.call("ak.wwise.core.object.get", args)
        if result["return"][0]["@IsLoopingEnabled"]:
            is_loop = True
        else:
            is_loop = False
        return is_loop
    except Exception as e:
        print(f'Error: {e}')

#create a function to retrieve the name of the Work Unit of the selected item
def get_work_unit_name(client, item_id):
    work_unit_name = []
    try:
        args = {
            "from": {"id": [item_id],},
            "transform": [{"select": ["ancestors"]}],
            "options":{ "return":["id","name","type", "path"]}
        }
        result = client.call("ak.wwise.core.object.get", args)
        for obj in result["return"]:
            if obj["type"] == "WorkUnit":
                work_unit_name.append(obj["name"])
        return work_unit_name[0]
    except Exception as e:
        print(f'Error: {e}')  

def main():
    client = set_client()
    event_created = False  # Add a flag for event creation
    try:
        with client:
            selected_items = get_selected_items(client)
            for item in selected_items:
                item_id = item[0]
                item_name = item[1]
                wu_name = get_work_unit_name(client, item_id)
                play_event = create_play_event(client, item_id, item_name, wu_name)
                if play_event:  # If an event is created, set the flag to True
                    event_created = True
                is_loop = is_looping(client, item_id)
                if is_loop:
                    stop_event = create_stop_event(client, item_id, item_name, wu_name)
                    if stop_event:  # If an event is created, set the flag to True
                        event_created = True
            if event_created:  # If the flag is True, show the success message
                show_success_message("Events created successfully!")
            else:
                show_error_message("No events were created.")

    except CannotConnectToWaapiException:
        show_error_message("Could not connect to Wwise Authoring API.")
        return None
    
if __name__ == "__main__":
    main()
