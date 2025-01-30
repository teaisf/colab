import os
import argparse
from pathlib import Path
from math import ceil


parser = argparse.ArgumentParser()
parser.add_argument('ipth', nargs='?')

args = parser.parse_args()

input_directory = args.ipth or "/content/drive/MyDrive"


# Function to calculate folder size recursively
def calculate_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            total_size += os.path.getsize(file_path)
    return total_size

# Convert bytes to GB
def bytes_to_gb(size_in_bytes):
    return size_in_bytes / (1024 ** 3)

# Check if the directory exists
if not os.path.exists(input_directory):
    print(f"Error: Directory '{input_directory}' does not exist.")
else:
    # Step 1: Get sizes of all folders
    folder_sizes = {}
    for folder in os.listdir(input_directory):
        folder_path = os.path.join(input_directory, folder)
        if os.path.isdir(folder_path):
            size_in_bytes = calculate_folder_size(folder_path)
            folder_sizes[folder] = size_in_bytes

    # Step 2: Separate folders > 15GB and group others
    over_15gb = {folder: size for folder, size in folder_sizes.items() if bytes_to_gb(size) > 15}
    under_15gb = {folder: size for folder, size in folder_sizes.items() if bytes_to_gb(size) <= 15}

    # Group folders under 15GB without exceeding 15GB per group
    sorted_folders = sorted(under_15gb.items(), key=lambda x: x[1], reverse=True)
    groups = []
    current_group = []
    current_group_size = 0

    for folder, size in sorted_folders:
        if bytes_to_gb(current_group_size + size) <= 15:
            current_group.append(folder)
            current_group_size += size
        else:
            groups.append(current_group)
            current_group = [folder]
            current_group_size = size

    if current_group:
        groups.append(current_group)

    # Step 3: Display results
    print("Folders exceeding 15GB:")
    for folder, size in over_15gb.items():
        print(f"  {folder}: {bytes_to_gb(size):.2f} GB")

    print("\nGroups of folders (each <= 15GB):")
    for i, group in enumerate(groups, 1):
        group_size = sum(folder_sizes[folder] for folder in group)
        print(f"  Group {i} ({bytes_to_gb(group_size):.2f} GB): {group}")