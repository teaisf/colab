import os
from pathlib import Path

try:
    BASEDIR = os.environ['BASEDIR']
except:
    BASEDIR = "/content/drive/MyDrive"


IDIR = os.path.join(BASEDIR, 'input')
ODIR = os.path.join(BASEDIR, 'output')
EDIR = os.path.join(BASEDIR, 'error')
DDIR = os.path.join(BASEDIR, 'trash')

paths = {
    "i": IDIR,
    "o": ODIR,
    "e": EDIR,
    "d": DDIR,
}

Path(IDIR).mkdir(parents=True, exist_ok=True)
Path(ODIR).mkdir(parents=True, exist_ok=True)
Path(EDIR).mkdir(parents=True, exist_ok=True)
Path(DDIR).mkdir(parents=True, exist_ok=True)