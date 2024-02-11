from wwise_helpers import *

#Set the WAAPI port
waapi_port = set_waapi_port()

def get_parent():
    parent = get_selected_items_type("parent")
    parent_id = parent[0]["id"]
    parent_name = parent[1]["name"]
    return parent_id, parent_name

def main():
   parent_id,parent_name = get_parent()
   print(f"ID: {parent_id}, Name: {parent_name}")
    
if __name__ == "__main__":
    main()
