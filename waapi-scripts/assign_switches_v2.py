from waapi import CannotConnectToWaapiException
from wwise_helpers import show_error_message, show_success_message, set_client


# Get items selected in the UI
def get_selected_items(client):
    args = {"options": {"return": ["id", "name", "notes", "type"]}}
    result = client.call("ak.wwise.ui.getSelectedObjects", args)
    if result:
        return result["objects"]
    else:
        show_error_message("No items selected!")
        return None


# Get containers that are children to the main container:
def get_switch_containers(client, id):
    waql = f'from object "{id}" select descendants where type = "SwitchContainer"'
    args = {
        "waql": waql
    }
    result = client.call("ak.wwise.core.object.get", args)
    return result["return"]


# Get the SwitchGroup or ID for the items
def get_switch_group(client, container_id):
    waql = f'from object "{container_id}" select this, descendants where SwitchGroupOrStateGroup != "False"'
    args = {
        "waql": waql,
        "options": {"return": ["SwitchGroupOrStateGroup"]}
    }
    result = client.call("ak.wwise.core.object.get", args)
    if result["return"]:
        return result["return"][0]["SwitchGroupOrStateGroup"]
    else:
        show_error_message(f"No switch group was assigned to {container_id}")
        raise ValueError(f"No switch group was assigned to {container_id}")


# Get the switches that are not assigned:
def get_assignments(client, container_id, switch_group_id):
    assigned = []
    switches = get_switches(client, switch_group_id)
    args = {
        "id": container_id,
    }
    result = client.call("ak.wwise.core.switchContainer.getAssignments", args)
    if result:
        for item in result["return"]:
            assigned.append(item["stateOrSwitch"])
    # Remove assigned switches
    not_assigned = [d for d in switches if d["id"] not in assigned]
    return not_assigned


# Create containers with the Switch Name:
def create_container(client, container_id, switch_name, switch_id):
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
        assign_switch(client, new_cont_id, switch_id)
        objects_created += 1

    else:
        show_error_message(f"Failed to create Random Container for Switch {switch_name}")
    return objects_created


# Look for similar named containers
def search_matching_container(client, container_id, not_assigned):
    assigned = 0
    waql = f'from object "{container_id}" select children'
    args = {
        "waql": waql
    }
    result = client.call("ak.wwise.core.object.get", args)
    # print(not_assigned)
    for child in result["return"]:
        child_name = child["name"]
        # print(child_name)
        for item in not_assigned:
            switch_name = item["name"]
            # print(switch_name)
            # print(f"Checking if '{switch_name.lower()}' is in '{child_name.lower()}'")  # Debug print
            if switch_name.lower() in child_name.lower():
                # print(f"MATCH in {switch_name} and {child_name}")
                assign_switch(client, child["id"], item["id"])
                not_assigned.remove(item)  # Remove the item from the not_assigned list
                assigned += 1
    return assigned


# Assign container to switch:
def assign_switch(client, child_id, switch_id):
    args = {
        "child": child_id,
        "stateOrSwitch": switch_id
    }
    client.call("ak.wwise.core.switchContainer.addAssignment", args)


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


def create_containers(client, switch_name, switch_id, container_id):
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
        assign_switch(client, new_cont_id, switch_id)
        objects_created += 1

    else:
        show_error_message(f"Failed to create Random Container for Switch {switch_name}")
    return objects_created


def main():
    try:
        client = set_client()
        with client:
            selected_items = get_selected_items(client)
            switch_containers = []
            for item in selected_items:
                id = item["id"]
                type = item["type"]
                if type == "SwitchContainer":
                    switch_containers.append(item)
                children_switch_containers = get_switch_containers(client, id)
                if children_switch_containers:
                    for container in children_switch_containers:
                        switch_containers.append(container)

            changed = 0
            for container in switch_containers:
                container_id = container["id"]
                switch_group = get_switch_group(client, container_id)
                if not switch_group:
                    show_error_message(f"No switch group was assigned for {container_id}")
                    continue
                not_assigned = get_assignments(client, container_id, switch_group["id"])
                # Call search_matching_container before creating new containers
                assigned = search_matching_container(client, container_id, not_assigned)
                for item in not_assigned:
                    switch_id = item["id"]
                    switch_name = item["name"]
                    create_containers(client, switch_name, switch_id, container_id)
                    changed += 1
                changed += assigned

        if changed:
            show_success_message(f"Successfully assigned containers for {changed} switches!")
        else:
            show_error_message("No switches were assigned!")

    except CannotConnectToWaapiException:
        show_error_message("Could not connect to Waapi: Is Wwise running and Wwise Authoring API enabled?")


if __name__ == "__main__":
    main()
