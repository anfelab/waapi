from waapi import CannotConnectToWaapiException
from wwise_helpers import show_error_message, set_client, get_selected_items, ask_user_input_str
from pydub import AudioSegment


def get_wavs(client, item_id):
    waql = f'from object "{item_id}" select this, descendants where type = "Sound" and Notes != "@ignore"'
    args = {
        "waql": waql,
        "options": {"return": ["id", "name", "parent", "volume", "sound:OriginalWavFilePath"]}
    }
    result = client.call("ak.wwise.core.object.get", args)
    wavs = []
    for item in result["return"]:
        wav = item["sound:OriginalWavFilePath"]
        wavs.append(wav)
    return wavs


def normalize_wavs(wavs):
    normalized = 0
    target_dBFS = float(ask_user_input_str("Loudness", "Enter the target Loudness: "))
    if not target_dBFS:
        target_dBFS = -23

    for wav in wavs:
        def match_target_amplitude(wav, target_dBFS):
            change_in_dBFS = target_dBFS - wav.dBFS
            return sound.apply_gain(change_in_dBFS)

        sound = AudioSegment.from_file(wav, "wav")
        normalized_sound = match_target_amplitude(wav, target_dBFS)
        normalized_sound.export(wav, format="wav")
        normalized += 1
    return normalized


def main():
    client = set_client()
    try:
        with client:
            selected_items = get_selected_items(client)
            for item in selected_items:
                item_id = item["id"]
                wavs = get_wavs(client, item_id)
                normalize_wavs(wavs)

    except CannotConnectToWaapiException:
        show_error_message("Could not connect to Wwise Authoring API.")
        return None


if __name__ == "__main__":
    main()
