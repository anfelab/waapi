from wwise_helpers import *

#Set the WAAPI port
waapi_port = set_waapi_port()
def get_switch_group():
    selected_items = get_selected_items()
    for item in selected_items:
        id = item[0]
        try:
            with WaapiClient(waapi_port) as client:
                args= {
                    "from":{"id":[id]},
                    "options":{"return":["id", "name","SwitchGroupOrStateGroup"]}
                }
                result = client.call("ak.wwise.core.object.get", args)
                print(result)
                switch_group_ids = []
                switch_group_ids.append(result["return"][0]['SwitchGroupOrStateGroup']["id"])
                switch_group_names = []
                switch_group_names.append(result["return"][0]['SwitchGroupOrStateGroup']["name"])

                if not switch_group_ids:
                    show_error_message("No switch container selected or no SwitchGroup assigned!")
            return switch_group_ids, switch_group_names

        except CannotConnectToWaapiException:
            show_error_message("Could not connect to Wwise Authoring API.")

def get_switches(switch_group_ids):
    switch_id_list = []
    switch_name_list = []
    for switch_group_id in switch_group_ids:
        try:
            with WaapiClient(waapi_port) as client:
                # Fetch switches within the Switch Group
                args = {
                    "from": {"id": [switch_group_id]},
                    "transform": [{"select": ['children']}],
                    "options": {"return": ["id", "name", "@SwitchGroupOrStateGroup"]}
                }
                result = client.call("ak.wwise.core.object.get", args)
                switches = result.get('return', [])
                print(switches)
                
                if not switches:
                    show_error_message(f"No switches found for Switch Group ID: {switch_group_id}")
                    continue
                for switch in switches:
                    switch_id = switch['id']
                    switch_name = switch["name"]
                    switch_id_list.append(switch_id)
                    switch_name_list.append(switch_name)
        except CannotConnectToWaapiException:
            show_error_message("Could not connect to Wwise Authoring API.")
    client.disconnect()
    return switch_id_list, switch_name_list

def get_assignments(container_id, switch_id):
    with WaapiClient(waapi_port) as client:
        children_args = {
                "from": {"id": [container_id]},
                "transform": [{"select": ['children']}],
                "options": {"return": ["id", "name", "@SwitchOrState"]}
            }
        assignments = client.call("ak.wwise.core.object.get", children_args)
        print(assignments)

        if not assignments:
        # If no assignments found, create a random container and assign it
            create_and_assign_container(client, switch_id)
        else:
            print(f"Switch {switch_id} already has assignments, skipping.")

def create_and_assign_container(switch_id, container_id):
    # Implementation for creating a random container and assigning it to the switch
    # Placeholder for creating a random container
    container_name = switch_id  #Example container name, adjust as needed
    with WaapiClient(waapi_port) as client:
        container_args = {
            "parent": container_id,
            "type": "RandomSequenceContainer",  # or any other container type
            "name": container_name
        }
        create_result = client.call("ak.wwise.core.object.create", container_args)
        if create_result:
            print(f"Created random container {container_name} and assigned to switch {switch_id}")
        else:
            print(f"Failed to create random container for switch {switch_id}")

def main():
        selected_items = get_selected_items_type("id")
        print(selected_items)
        for container_id in selected_items:
            switch_group_id, switch_group_name = get_switch_group()
            print(f"Switch group is {switch_group_id},{switch_group_name}")
            switch_id_list, switch_name_list = get_switches(switch_group_id)
            for switch_id in switch_id_list:
                print(switch_id)
    
if __name__ == "__main__":
    main()
