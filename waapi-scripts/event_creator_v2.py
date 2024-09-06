from waapi import CannotConnectToWaapiException
from wwise_helpers import show_error_message, show_message, show_success_message, set_client

client = set_client()


# Create a function using waapi to get the id, name and path of the selected items in Wwise
def get_selected_items():
    args = {"options": {"return": ["id", "name", "path"]}}
    result = client.call("ak.wwise.ui.getSelectedObjects", args)
    if result:
        return result["objects"]
    else:
        show_error_message("No items selected.")
        return None


# Create a function to create a Play event for the selected items
def create_play_event(item_id, item_name, wu_name, path="\\Events\\Default Work Unit"):
    try:
        args = {
            "parent": f"{path}",
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
def create_stop_event(item_id, item_name, wu_name, path="\\Events\\Default Work Unit"):
    try:
        args = {
            "parent": path,
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
def is_looping(item_id):
    is_loop = False
    try:
        args = {
            "from": {"id": [item_id]},
            "transform": [{"select": ["descendants"]}],
            "options": {"return": ["@IsLoopingEnabled"]}
        }
        result = client.call("ak.wwise.core.object.get", args)
        if result["return"][0]["@IsLoopingEnabled"]:
            is_loop = True
        else:
            is_loop = False
        return is_loop
    except Exception as e:
        print(f'Error: {e}')


# create a function to retrieve the name of the Work Unit of the selected item
def get_work_unit_name(item_id):
    work_unit_name = []
    try:
        args = {
            "from": {"id": [item_id], },
            "transform": [{"select": ["ancestors"]}],
            "options": {"return": ["id", "name", "type", "path"]}
        }
        result = client.call("ak.wwise.core.object.get", args)
        for obj in result["return"]:
            if obj["type"] == "WorkUnit":
                work_unit_name.append(obj["name"])
        return work_unit_name[0]
    except Exception as e:
        print(f'Error: {e}')


def define_event_path(wu_name):
    waql = f'from object "\\Events" select descendants where type = "workunit" and name ="{wu_name}"'
    try:
        args = {
            "waql": waql,
            "options": {"return": ["path"]}
        }
        result = client.call("ak.wwise.core.object.get", args)
        path = (result["return"][0]["path"])
        return path

    except Exception as e:
        print(f'Error: {e}')


def main():
    event_created = False  # Add a flag for event creation
    try:
        with client:
            selected_items = get_selected_items()
            for item in selected_items:
                wu_name = get_work_unit_name(item["id"])
                path = ""
                play_event = create_play_event(item["id"], item["name"], wu_name, path)
                if play_event:  # If an event is created, set the flag to True
                    event_created = True
                is_loop = is_looping(item["id"])
                if is_loop:
                    stop_event = create_stop_event(item["id"], item["name"], wu_name, path)
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
