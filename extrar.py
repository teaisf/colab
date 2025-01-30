import os
import argparse
import rarfile
import re
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument('ipth', nargs='?')
parser.add_argument('opth', nargs='?')

args = parser.parse_args()

input_dir = args.ipth or "input"
output_dir = args.opth or "output"

def remove_all(root, base_name):
    for file in root.iterdir():
        # Check if the file is a regular file and contains the search string
        if file.is_file() and (base_name in file.name):
            print(f"Removing: {file}")
            file.unlink()  # Delete the file

def extract_rars():
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    ipth = Path(input_dir)

    for rar_file in ipth.glob("*.rar"):
        rar_path = str(rar_file.resolve())

        match = re.match(r"(.*?)(\.part\d+)(.*?)?\.rar", rar_file.name)

        if match:
            base_name = match.group(1)

            if "part1" in rar_file.stem:
                with rarfile.RarFile(rar_path) as rf:
                    print(f"Extracting {rar_file.name}...")
                    rf.extractall(output_dir)
                remove_all(ipth, base_name)
        else:
            with rarfile.RarFile(rar_path) as rf:
                print(f"Extracting {rar_file.name}...")
                rf.extractall(output_dir)
            rar_file.unlink()

extract_rars()
