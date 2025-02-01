import os
import argparse
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument('ipth', nargs='?')
parser.add_argument('opth', nargs='?')

args = parser.parse_args()

input_directory = args.ipth or "/content/drive/MyDrive/input"
output_directory = args.opth or "/content/drive/MyDrive/output"


def get_recursive_folder_size(folder_path):
    """Calculate the total size of a folder recursively."""
    total_size = 0
    for root, _, files in os.walk(folder_path):
        total_size += sum(os.path.getsize(os.path.join(root, file)) for file in files)
    return total_size

def get_first_level_folder_sizes(directory):
    """Get the recursive sizes of first-level subfolders in a directory."""
    folder_sizes = {}
    for entry in os.scandir(directory):
        if entry.is_dir():
            folder_sizes[entry.name] = get_recursive_folder_size(entry.path)
    return folder_sizes

def compare_folders(input_dir, output_dir):
    """Compare folders and print first-level subfolders in input not in output, ordered by size."""
    input_sizes = get_first_level_folder_sizes(input_dir)
    output_subfolders = {entry.name for entry in os.scandir(output_dir) if entry.is_dir()}

    # Find subfolders in input not in output
    diff_folders = {folder: size for folder, size in input_sizes.items() if folder not in output_subfolders}

    # Sort by size in descending order
    sorted_diff_folders = sorted(diff_folders.items(), key=lambda x: x[1], reverse=True)

    # Print the results
    print(f"First-level subfolders in '{input_dir}' not in '{output_dir}':")
    for folder, size in sorted_diff_folders:
        print(f"{folder} - {size / (1024 * 1024):.2f} MB")

# Check if the directory exists
if not os.path.exists(input_directory):
    print(f"Error: Directory '{input_directory}' does not exist.")
elif not os.path.exists(output_directory):
    print(f"Error: Directory '{output_directory}' does not exist.")
else:
    # Get a list of all items in the directory
    compare_folders(input_directory, output_directory)
