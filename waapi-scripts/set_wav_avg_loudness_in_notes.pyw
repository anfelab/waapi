from waapi import CannotConnectToWaapiException
from wwise_helpers import show_error_message, set_client, get_selected_items
import soundfile as sf
import pyloudnorm as pyln


def get_paths_and_parent(client, item_id):
    waql = f'from object "{item_id}" select this, descendants where type = "Sound" and sound:OriginalWavFilePath != ""'
    args = {
        "waql": waql,
        "options": {"return": ["id", "name", "sound:originalWavFilePath","parent"]}
    }
    result = client.call("ak.wwise.core.object.get", args)
    return result["return"]


def get_loudness_for_wavs(client, objects):
    for i in objects:
        path = i["sound:originalWavFilePath"]
        data, rate = sf.read(path)
        meter = pyln.Meter(rate)
        loudness = meter.integrated_loudness(data)
        loudness = round(loudness, 2)
        i["loudness"] = loudness
        notes = f'Loudness = {i["loudness"]} LUFS'
        set_notes(client, i["id"], notes)
    return objects


def calculate_average_loudness(client, items):
    # Dictionary to store total loudness and count for each parent
    parent_loudness = {}

    for item in items:
        parent_id = item['parent']['id']
        loudness = item['loudness']

        if parent_id not in parent_loudness:
            parent_loudness[parent_id] = {'total_loudness': 0, 'count': 0}

        parent_loudness[parent_id]['total_loudness'] += loudness
        parent_loudness[parent_id]['count'] += 1

    # Calculate average loudness for each parent
    average_loudness = {}
    for parent_id, data in parent_loudness.items():
        average_loudness[parent_id] = data['total_loudness'] / data['count']
        avg = f'Average loudness = {round(average_loudness[parent_id], 2)} LUFS'
        set_notes(client, parent_id, avg)


def set_notes(client, item_id, notes):
    args = {
        "object": item_id,
        "value": f"{notes}"
    }
    result = client.call("ak.wwise.core.object.setNotes", args)


def main():
    client = set_client()
    try:
        with client:
            selected_items = get_selected_items(client)
            for item in selected_items:
                item_id = item[0]
                objects = get_paths_and_parent(client, item_id)
                objects = get_loudness_for_wavs(client, objects)
                calculate_average_loudness(client, objects)

    except CannotConnectToWaapiException:
        show_error_message("Could not connect to Wwise Authoring API.")
        return None


if __name__ == "__main__":
    main()
