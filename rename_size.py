import os
import argparse
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument('ipth', nargs='?')

args = parser.parse_args()

input_directory = args.ipth


def get_directory_size(directory):
    """Recursively calculate the size of all files in a directory."""
    total_size = 0
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            # Add the file size if the file exists
            if os.path.isfile(filepath):
                total_size += os.path.getsize(filepath)
    return total_size

def rename_directories(base_path):
    """Rename directories by prefixing them with their sorted index based on size."""
    # List all directories in the base path
    directories = [
        os.path.join(base_path, d)
        for d in os.listdir(base_path)
        if os.path.isdir(os.path.join(base_path, d))
    ]

    # Calculate the size of each directory
    dir_sizes = [(d, get_directory_size(d)) for d in directories]

    # Sort directories by size in descending order
    sorted_dirs = sorted(dir_sizes, key=lambda x: x[1], reverse=True)

    # Rename directories with their index as a prefix
    for index, (dir_path, _) in enumerate(sorted_dirs):
        dir_name = os.path.basename(dir_path)
        new_name = os.path.join(base_path, f"{index+1}_{dir_name}")
        os.rename(dir_path, new_name)

# Check if the directory exists
if not os.path.exists(input_directory):
    print(f"Error: Directory '{input_directory}' does not exist.")
else:
    # Get a list of all items in the directory
    rename_directories(input_directory)
