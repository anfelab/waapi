from waapi import CannotConnectToWaapiException
from wwise_helpers import show_error_message, show_message, show_success_message, set_client, get_selected_items


def check_for_unused(client, item_id):
    waql = f'from object "{item_id}" select this, descendants where type = "Event"'
    args = {
        "waql": waql,
        "options": {"return": ["id", "name", "@Target", "type", "isIncluded"]}
    }
    result = client.call("ak.wwise.core.object.get", args)
    unused = []
    included = []
    for item in result["return"]:
        actions = check_actions(client, item["id"])
        for action in actions:
            target_id = action["@Target"]["id"]
            target_name = action["@Target"]["name"]
            inclusion = check_inclusion(client, target_id)
            if not inclusion and item["isIncluded"]:
                print(f'{target_name} is not included! {item["name"]} inclusion will be set to Off!')
                # set_not_included(client, target_id)
                set_not_included(client, item["id"])
                unused.append(item)
            elif not item["isIncluded"] and inclusion:
                print(f'{target_name} has included objects!, {item["name"]} inclusion will be set to On!')
                # set_included(client, target_id)
                set_included(client, item["id"])
                included.append(item)
            else:
                continue

    if len(unused) > 1:
        show_success_message(f"{len(unused)} Unused event(s) set as NOT INCLUDED!")
    elif len(included) > 1:
        show_success_message(f"{len(included)} Event(s) with inclusions were set back as INCLUDED!")
    elif len(unused) == 0:
        show_error_message("No items were changed!")


def check_actions(client, item_id):
    waql = f'from object "{item_id}" select children'
    args = {
        "waql": waql,
        "options": {"return": ["id", "name", "@Target", "type"]}
    }
    result = client.call("ak.wwise.core.object.get", args)
    return result["return"]


def check_inclusion(client, target_id):
    waql = f'from object "{target_id}"'
    args = {
        "waql": waql,
        "options": {"return": ["isIncluded"]}
    }
    result = client.call("ak.wwise.core.object.get", args)
    return result["return"][0]["isIncluded"]


def set_not_included(client, item_id):
    args = {
        "object": item_id,
        "property": "Inclusion",
        "value": False
    }
    result = client.call("ak.wwise.core.object.setProperty", args)


def set_included(client, item_id):
    args = {
        "object": item_id,
        "property": "Inclusion",
        "value": True
    }
    result = client.call("ak.wwise.core.object.setProperty", args)


def main():
    client = set_client()
    try:
        with client:
            selected_items = get_selected_items(client)
            for item in selected_items:
                item_id = item["id"]
                check_for_unused(client, item_id)
                client.disconnect()

    except CannotConnectToWaapiException:
        show_error_message("Could not connect to Wwise Authoring API.")
        return None


if __name__ == "__main__":
    main()
