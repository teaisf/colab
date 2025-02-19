import os
import shutil
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('ipth', nargs='?')

args = parser.parse_args()

directory = args.ipth or "/content/drive/MyDrive"


# Check if the directory exists
if not os.path.exists(directory):
    print(f"Error: Directory '{directory}' does not exist.")
else:
    # Iterate over all files in the directory
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
    
        # Check if it's a file, begins with a number, and has a size of 0 bytes
        if filename[0].isdigit() and os.path.getsize(filepath) == 0:
            if os.path.isdir(filename):
                shutil.rmtree(filepath)  # Delete the file
                print(f"Deleted: {filepath}")
            else:
                os.remove(filepath)  # Delete the file
                print(f"Deleted: {filepath}")
