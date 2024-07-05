from waapi import CannotConnectToWaapiException
from wwise_helpers import show_success_message, set_client, get_selected_items


def search_for_similar_wu_events(client, name):
    waql = f'from object "\\Actor-Mixer Hierarchy", "\\Events", "\\SoundBanks" select descendants where type = "WorkUnit" and name = "{name}"'
    args = {
        "waql": waql
    }
    result = client.call("ak.wwise.core.object.get", args)
    return result["return"]

def copy_notes_to_wu(client, id, notes):
    args = {
        "object": id,
        "value": f"{notes}"
    }
    result = client.call("ak.wwise.core.object.setNotes", args)


def main():
    client = set_client()
    try:
        with client:
            selected_objects = get_selected_items(client)
            items_changed = 0
            for item in selected_objects:
                item_name = item[1]
                item_notes = item[2]
                workunits = search_for_similar_wu_events(client, item_name)

                if workunits:
                    for wu in workunits:
                        wu_id = wu["id"]
                        copy_notes_to_wu(client, wu_id, item_notes)
                        items_changed += 1

            if items_changed > 0:
                show_success_message(f"Notes were copied to {items_changed} similar WorkUnit(s)!")

        client.disconnect()

    except CannotConnectToWaapiException as e:
        print("Error connecting to Wwise: {}".format(e))
        client.disconnect()


if __name__ == "__main__":
    main()
