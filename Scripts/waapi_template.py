from wwise_helpers import get_clipboard_content, show_error_message, show_success_message, get_selected_items

# Now you can use these functions directly
def main():
    selected_items = get_selected_items()
    if not selected_items:
        show_error_message("No items selected in Wwise.")
        return

    # write code

if __name__ == "__main__":
    main()
