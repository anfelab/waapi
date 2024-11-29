from waapi import CannotConnectToWaapiException
from wwise_helpers import messagebox, set_client
from tkinter import messagebox

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
        messagebox.showerror(f"No switch group was assigned to {container_id}")
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
        messagebox.showerror(f"No switches found for Switch Group ID: {switch_group_id}")
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


class SwitchAssigner:
    def __init__(self, client):
        self.client = client
        self.handlers = {}
        self.is_subscribed = False

    def subscribe_to_events(self):
        if self.is_subscribed:
            messagebox.showinfo("Subscription", "Already subscribed")
            return

        def on_child_added(*args, **kwargs):
            parent_type = kwargs.get("parent", {}).get("type")
            parent_id = kwargs.get("parent", {}).get("id")
            child = kwargs.get("child")

            if parent_type != "SwitchContainer":
                return
            
            switch_group = get_switch_group(self.client, parent_id)
            not_assigned = get_assignments(self.client, parent_id, switch_group["id"])
            assigned = search_matching_container(self.client, child, not_assigned)
            if assigned:
                print(f'{child["name"]} was assigned!')

        def on_name_changed(*args, **kwargs):
            result = kwargs.get("object")
            parent = kwargs.get("object", {}).get("parent")
            print(result)

            if not parent :
                return
            if result["parent.type"] != "SwitchContainer":
                return
            
            switch_group = get_switch_group(self.client, result["parent"]["id"])
            not_assigned = get_assignments(self.client, result["parent"]["id"], switch_group["id"])
            assigned = search_matching_container(self.client, result, not_assigned)
            if assigned:
                print(f'{result["name"]} was assigned!')

        # Subscribing to multiple events
        self.handlers["childAdded"] = self.client.subscribe(
            "ak.wwise.core.object.childAdded",
            on_child_added,
            {"return": ["id", "name", "type", "parent"]}
        )

        self.handlers["nameChanged"] = self.client.subscribe(
            "ak.wwise.core.object.nameChanged",
            on_name_changed,
            {"return": ["id", "name", "parent", "parent.type"]}
        )

        messagebox.showinfo("Subscription", "Subscribed to events.")
        self.is_subscribed = True

    def unsubscribe_from_events(self):
        if not self.is_subscribed:
            messagebox.showerror("Subscription", "Not currently subscribed.")
            return

        for handler in self.handlers.values():
            self.client.unsubscribe(handler)

        self.handlers.clear()
        self.is_subscribed = False
        messagebox.showinfo("Subscription", "Unsubscribed from events.")

    def toggle_subscription(self):
        if self.is_subscribed:
            self.unsubscribe_from_events()
        else:
            self.subscribe_to_events()


def main():
    try:
        client = set_client()

    except CannotConnectToWaapiException:
        messagebox.showerror("Error", "Could not connect to Wwise Authoring API.")
        return None
    else:
        assigner = SwitchAssigner(client)

        while True:
            print("\nOptions:")
            print("1. Toggle subscription")
            print("2. Exit")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                assigner.toggle_subscription()
            elif choice == "2":
                if assigner.is_subscribed:
                    assigner.unsubscribe_from_events()
                client.disconnect()
                break
            else:
                print("Invalid choice. Please try again.")
                if assigner.is_subscribed:
                    assigner.unsubscribe_from_events()
                client.disconnect()
    finally:
        client.disconnect()

   
if __name__ == "__main__":
    main()