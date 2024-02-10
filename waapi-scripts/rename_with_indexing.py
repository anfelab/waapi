from wwise_helpers import *

# Set the WAAPI port once
waapi_port = set_waapi_port()

def rename_objects():
    id_list = get_selected_items_type("id")
    if not id_list:
        show_error_message("No items selected!")
        return  # Exit if no items are selected

    new_name = ask_user_input_str()  # Get the new base name from the user once
    total_items = len(id_list)

    for idx, object_id in enumerate(id_list, start=1):  # Start indexing from 1
        # Apply suffix only if more than one item is selected
        suffix = f"_{idx:02}" if total_items > 1 else ""

        try:
            with WaapiClient(waapi_port) as client:
                args = {
                    "object": object_id,
                    "value": f"{new_name}{suffix}"
                }
                client.call("ak.wwise.core.object.setName", args)
        except CannotConnectToWaapiException:
            show_error_message("Could not connect to Wwise Authoring API.")
            return None
        except Exception as e:  # Catch other potential exceptions
            show_error_message(f"An error occurred: {str(e)}")
            return None

    print(f"Renamed {total_items} items.")

def main():
    rename_objects()

if __name__ == "__main__":
    main()
