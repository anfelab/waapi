from waapi import WaapiClient, CannotConnectToWaapiException
from wwise_helpers import show_error_message, show_message, show_success_message

#Set the WAAPI port
def set_client(ip = "127.0.0.1", port = 8080):
    waapi_port = f"ws://{ip}:{port}/waapi"
    print(f"Client set to: {waapi_port}")
    client = WaapiClient(waapi_port)
    return client

def get_selected_items(client):
    selected_items = []
    args = {"options": {"return":["id", "name","SwitchGroupOrStateGroup"]}}
    result = client.call("ak.wwise.ui.getSelectedObjects", args)
    print(result)
    for item in result["objects"]:
        selected_items.append(item)
    return selected_items

def get_switches(client, switch_group_id):
    switch_list = []
    args = {
        "from": {"id": [switch_group_id]},
        "transform": [{"select": ['children']}],
        "options": {"return": ["id", "name"]}
    }
    result = client.call("ak.wwise.core.object.get", args)
    switches = result["return"]
    for switch in switches:
        switch_list.append(switch)
    
    if not switches:
        show_error_message(f"No switches found for Switch Group ID: {switch_group_id}")
    return switch_list

def get_assignments(client, container_id):
    args = {
        "id": container_id
    }
    result = client.call("ak.wwise.core.switchContainer.getAssignments", args)
    assigned_switches = [assignment['stateOrSwitch'] for assignment in result['return']]
    return assigned_switches

def find_unassigned_switches(client, container_id, switch_group_id):
    all_switches = get_switches(client, switch_group_id)
    assigned_switches = get_assignments(client, container_id)
    for assign in assigned_switches:
        print(f"{assign} is already assigned!. Skipping")
    unassigned_switches = [switch for switch in all_switches if switch not in assigned_switches]
    return unassigned_switches

def create_container(client,container_id,container_name,switch_name, switch_id):
    new_container_name = f"{switch_name.lower()}"
    container_args = {
        "parent": container_id,
        "type": "RandomSequenceContainer",  # or any other container type
        "name": new_container_name,
        "onNameConflict": "merge"
    }
    create_result = client.call("ak.wwise.core.object.create", container_args)
    new_cont_id = create_result["id"]
    if create_result:
        print(f"Created random container {new_container_name} and assigned to switch {switch_name}")
        assign_switch(client, new_cont_id,switch_id)
        
    else:
        print(f"Failed to create random container for switch {switch_name}")
    return create_result

def assign_switch(client, child_id, switch_id):
    args = {
        "child":child_id,
        "stateOrSwitch":switch_id
    }
    client.call("ak.wwise.core.switchContainer.addAssignment",args)

def main():
    try:
        client = set_client()
        with client:
            selected_items = get_selected_items(client)
            for item in selected_items:
                container_id = item["id"]
                container_name = item["name"]
                switch_group_id = item["SwitchGroupOrStateGroup"]["id"]
                switch_group_name = item["SwitchGroupOrStateGroup"]["name"]
                if not switch_group_id:
                    show_error_message("No Switch Container selected or no switch group assigned!")
                    client.disconnect()
                print(f"Current container is {container_name}, ID: {container_id}")
                print(f"Assigned to {switch_group_name}, {switch_group_id}")
                
                not_assigned = find_unassigned_switches(client,container_id,switch_group_id)
                
                for not_assigned_item in not_assigned:
                    not_assigned_id = not_assigned_item["id"]
                    not_assigned_name = not_assigned_item["name"]
                    create_container(client,container_id,container_name,not_assigned_name,not_assigned_id)
            client.disconnect()
             
    except CannotConnectToWaapiException:
        print("Could not connect to Waapi: Is Wwise running and Wwise Authoring API enabled?")
    
if __name__ == "__main__":
    main()