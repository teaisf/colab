import os
import shutil
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('ipth', nargs='?')

args = parser.parse_args()

input_directory = args.ipth or "/content/drive/MyDrive"


# Check if the directory exists
if not os.path.exists(input_directory):
    print(f"Error: Directory '{input_directory}' does not exist.")
else:
    # Get a list of all items in the directory
    items = os.listdir(input_directory)

    # Iterate through each item
    deleted_items = []
    for item in items:
        # Check if the item starts with 'DEL_'
        if item.startswith("DEL_"):
            item_path = os.path.join(input_directory, item)
            try:
                # Check if it's a file or folder and delete accordingly
                if os.path.isfile(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                deleted_items.append(item)
            except Exception as e:
                print(f"Failed to delete {item}: {e}")

    # Print the names of deleted files and folders
    if deleted_items:
        print("Deleted items:")
        for deleted_item in deleted_items:
            print(f"- {deleted_item}")
    else:
        print("No items with the prefix 'DEL_' found.")
