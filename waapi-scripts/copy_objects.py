from wwise_helpers import *

#Set the WAAPI port
waapi_port = set_waapi_port()

def copy_objects():
    id_list = get_selected_items_type("id") #Import the list of IDs
    parent_list = get_selected_items_type("parent") #Import the list for the parent container

    try:
        with WaapiClient(waapi_port) as client:
            for i in range(len(id_list)):
                object_id = id_list[i] 
                parent_id = parent_list[i]["id"]  
                args = {
                    "object": object_id,  
                    "onNameConflict": "rename",
                    "parent": parent_id,  
                }
                client.call("ak.wwise.core.object.copy", args)
                client.disconnect()
        
    except CannotConnectToWaapiException:
        show_error_message("Could not connect to Wwise Authoring API.")
        return None
    except Exception as e:
        show_error_message(f"An error occurred during copy: {str(e)}")
        return None
        
def main():
    selected_items = get_selected_items()
    if not selected_items:
        show_error_message("No items selected in Wwise.")
        return
    else:
        times = ask_user_input_num()
        execute_func_times(copy_objects,times)
        show_success_message(f"Item copied {times} times!")

            
if __name__ == "__main__":
    main()
