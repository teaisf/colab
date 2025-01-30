import os
import argparse
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument('ipth', nargs='?')

args = parser.parse_args()

input_directory = args.ipth or "/content/drive/MyDrive"

# Check if the directory exists
if not os.path.exists(input_directory):
    print(f"Error: Directory '{input_directory}' does not exist.")
else:
    # Get a list of all items in the directory
    root_directory = Path(input_directory)
    x = [f for f in root_directory.glob('**/*') if f.is_file()]
    for y in x:
        if y.stem.startswith('Copy of '):
            y.rename(y.with_stem(y.stem[8:]))
