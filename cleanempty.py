import os
from pathlib import Path
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('ipth', nargs='?')

args = parser.parse_args()

root_dir = args.ipth or "/content/drive/MyDrive"

# Check if the directory exists
if not os.path.exists(root_dir):
    print(f"Error: Directory '{root_dir}' does not exist.")
else:
    # Function to check and delete empty folders
    for folder in Path(root_dir).iterdir():
        if folder.is_dir():
            try:
                # Get folder creation time
                creation_time = folder.stat().st_atime

                # Check if folder is empty and created in the last 24 hours
                if not any(folder.iterdir()) and creation_time == 0:
                    print(f"Deleting empty folder: {folder}")
                    # os.rmdir(folder)
            except Exception as e:
                print(f"Error processing {folder}: {e}")

# Run the function
print("Process completed.")
