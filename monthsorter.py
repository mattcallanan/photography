from os import listdir, path, makedirs
from datetime import datetime
import shutil
import sys

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("target_dir", help="Destination directory to create folders and move items")
parser.add_argument("--real", help="Do it for real (no-noop)", action="store_true")
args = parser.parse_args()

print("args: {1}.", args)


def get_dest_dirname(date):
    return date.strftime('%Y-%m (%b)')

if (len(sys.argv) < 2):
    raise ValueError("No directory name provided.")

files_to_move = listdir(args.target_dir)
print(files_to_move)

def get_date_taken(filepath):
    """pip install Pillow"""
    from PIL import Image
    try:
        date_taken = Image.open(filepath)._getexif()[36867]
        return datetime.strptime(date_taken[0:10], "%Y:%m:%d")
    except:
        mtime = path.getmtime(filepath)
        return datetime.fromtimestamp(mtime)

for f in files_to_move:
    filepath = path.join(args.target_dir, f)
    if path.isfile(filepath):
        filetime = get_date_taken(filepath)
        dest_dirpath = path.join(args.target_dir, get_dest_dirname(filetime))
        if args.real:
            if not path.exists(dest_dirpath):
                makedirs(dest_dirpath)
            shutil.move(filepath, dest_dirpath)
        print("{0}Moved {1} to {2}".format("" if args.real else "(noop) ", f, dest_dirpath))
    else:
        print("Skipping {0} (non-file)".format(f))
