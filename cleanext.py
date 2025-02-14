import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('ipth', nargs='?')
parser.add_argument('-e')

args = parser.parse_args()

root_dir = args.ipth or "/content/drive/MyDrive"
extens = args.e or ".srt"

# Check if the directory exists
if not os.path.exists(root_dir):
    print(f"Error: Directory '{root_dir}' does not exist.")
else:
    import os
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for file in filenames:
            if file.endswith(extens):  # Check for .srt files
                file_path = os.path.join(dirpath, file)
                with open(file_path, 'w'): pass
                os.remove(file_path)  # Delete the file
                print(f"Deleted: {file_path}")

    print(f"All {extens} files have been deleted.")
