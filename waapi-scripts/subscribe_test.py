from waapi import CannotConnectToWaapiException
from wwise_helpers import show_error_message, set_client

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

def assign_switch(client, child_id, switch_id):
    args = {
        "child": child_id,
        "stateOrSwitch": switch_id
    }
    client.call("ak.wwise.core.switchContainer.addAssignment", args)

def search_matching_container(client, child, not_assigned):
    assigned = False
    child_name = child["name"]
    for item in not_assigned:
        switch_name = item["name"]
        if switch_name.lower() in child_name.lower():
            assign_switch(client, child["id"], item["id"])
            not_assigned.remove(item)  # Remove the item from the not_assigned list
            assigned = True
    return assigned

def main():
    try:
        client = set_client()

    except CannotConnectToWaapiException:
        show_error_message("Could not connect to Wwise Authoring API.")
        return None
    else:
    # Callback function with a matching signature.
    # Signature (*args, **kwargs) matches anything, with results being in kwargs.
        def on_child_added(*args, **kwargs):
            parent_type = kwargs.get("parent").get("type")
            parent_id = kwargs.get("parent").get("id")
            child = kwargs.get("child")

            if parent_type != "SwitchContainer":
                return
            
            switch_group = get_switch_group(client, parent_id)
            not_assigned = get_assignments(client, parent_id, switch_group["id"])
            assigned = search_matching_container(client, child, not_assigned)
            if assigned:
                print(f"{child["name"]} was assigned!")
            client.disconnect()

    handler = client.subscribe("ak.wwise.core.object.childAdded", on_child_added, {"return": ["id", "name", "type"]})
    print("Subscribed to 'ak.wwise.core.object.childAdded'")


if __name__ == "__main__":
    main()
