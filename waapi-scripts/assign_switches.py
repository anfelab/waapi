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
    for item in result["objects"]:
        selected_items.append(item)
    return selected_items

def get_children(client, container_id):
    args = {
        "from": {"id": [container_id]},
        "transform":[{"select":["children"]}],
        "options": {"return": ["name", "id"]}
    }
    result = client.call("ak.wwise.core.object.get", args)
    if result:
        return result["return"]

def check_if_container_is_assigned(client,container_id,switch_list):  #(client, container_id,container_name,switch_list)
    unassaigned_switches = []
    assigned_switches = []
    args={
        "id":container_id,
    }
    result = client.call("ak.wwise.core.switchContainer.getAssignments",args)
    if result:
        for assingment in result["return"]:
            assigned_switches.append(assingment["stateOrSwitch"])
    else:
        print(f"No assignments found")

    unassaigned_switches = remove_values(assigned_switches,switch_list)
    return unassaigned_switches

def remove_values(list1, list2):
    return[item for item in list2 if item["id"] not in list1]

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

def create_container(client,container_id,container_name,switch_name, switch_id):
    objects_created = 0
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
        print(f"Created Random Container [{new_container_name}] and assigned to switch [{switch_name}]")
        assign_switch(client, new_cont_id,switch_id)
        objects_created += 1
        
    else:
        show_error_message(f"Failed to create Random Container for Switch {switch_name}")
    return objects_created

def assign_switch(client, child_id, switch_id):
    args = {
        "child":child_id,
        "stateOrSwitch":switch_id
    }
    client.call("ak.wwise.core.switchContainer.addAssignment",args)

def look_matching_item(client,switch_name, switch_id, child_name, current_child_id):
    result = switch_name.lower() in child_name.lower()
    if result:
        assign_switch(client,current_child_id, switch_id)

def main():
    try:
        client = set_client()
        with client:
            selected_items = get_selected_items(client)
            for item in selected_items:
                container_id = item["id"] #Get the ID for every container selected
                container_name = item["name"] #Get the name for every container selected
                switch_group_id = item["SwitchGroupOrStateGroup"]["id"] #Get the assigned Group Switch ID
                switch_group_name = item["SwitchGroupOrStateGroup"]["name"] #Get the assigned Group Switch Name
                if not switch_group_id or not switch_group_name:
                    show_error_message("No Switch Container selected or no switch group assigned!")
                    client.disconnect()
                current_children = get_children(client, container_id) #Look for preexisting containers
                switch_list = get_switches(client, switch_group_id)
                for current_child in current_children:
                    current_child_name = current_child["name"]
                    current_child_id = current_child["id"]
                    for switch in switch_list:
                        look_matching_item(client,switch["name"],switch["id"], current_child_name, current_child_id)
                unnasigned_switches = check_if_container_is_assigned(client, container_id,switch_list)

                if current_children:
                    for unnasigned_switch in unnasigned_switches:
                        unnasigned_switch_id = unnasigned_switch["id"]
                        unnasigned_switch_name = unnasigned_switch["name"]
                        create_result = create_container(client,container_id,container_name,unnasigned_switch_name,unnasigned_switch_id)              
                    
                else:
                    switch_list = get_switches(client, switch_group_id)
                    unnasigned_switches = switch_list
                    for unnasigned_switch in unnasigned_switches:
                        unnasigned_switch_id = unnasigned_switch["id"]
                        unnasigned_switch_name = unnasigned_switch["name"]
                        create_result = create_container(client,container_id,container_name,unnasigned_switch_name,unnasigned_switch_id)
            client.disconnect()

    except CannotConnectToWaapiException:
        show_error_message("Could not connect to Waapi: Is Wwise running and Wwise Authoring API enabled?")
        client.disconnect()

    show_success_message(f"Succesfully assigned containers for all switches!")
    
if __name__ == "__main__":
    main()