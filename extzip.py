#!/usr/bin/env python

import os, glob
import zipfile
from pathlib import Path

def compress_files():
    # path = os.getcwd()
    path = "/content/drive/MyDrive"
    ipth = os.path.join(path, 'compressed')
    opth = os.path.join(path, 'extracted')
    files = glob.glob(ipth + "/*.zip")
    print(files)
    for c in files:
        with zipfile.ZipFile(c, 'r') as zipf:
            zipf.extractall(opth)
        os.remove(c)
        print(c)

compress_files()