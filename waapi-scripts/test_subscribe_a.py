from waapi import WaapiClient, CannotConnectToWaapiException
from wwise_helpers import show_error_message, show_message, show_success_message, set_client



def main():
    try:
        client = set_client()
    except CannotConnectToWaapiException:
        print("Could not connect to Waapi: Is Wwise running and Wwise Authoring API enabled?")
    else:
        def on_selection_changed(*args, **kwargs):
            result = kwargs.get("objects")
            print(f"Selection changed to {result = }")
            client.disconnect()
 
    handler = client.subscribe("ak.wwise.ui.selectionChanged", on_selection_changed, {"return": ["id", "name", "type"]})
 
    print("Subscribed 'ak.wwise.ui.selectionChanged', select an object in Wwise")
    

if __name__ == "__main__":
    main()