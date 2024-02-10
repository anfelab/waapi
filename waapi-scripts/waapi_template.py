from wwise_helpers import *

#Set the WAAPI port
waapi_port = set_waapi_port()

def main():
    selected_items = get_selected_items()
    if not selected_items:
        show_error_message("No items selected in Wwise.")
        return
    for item in selected_items: #idx 0 for id, 1 for name
        print (item[1])
        
if __name__ == "__main__":
    main()
