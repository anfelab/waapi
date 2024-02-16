from waapi import WaapiClient, CannotConnectToWaapiException
from wwise_helpers import show_error_message, show_message, show_success_message, set_client

def main():
    client = set_client()
    try:
        with client:
            result = client.call("ak.wwise.core.getInfo")
            print(result)

    except CannotConnectToWaapiException:
        show_error_message("Could not connect to Wwise Authoring API.")
        return None
    
if __name__ == "__main__":
    main()
