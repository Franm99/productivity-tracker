import pathlib
import os

MODULE_DIR = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
PAR_DIR = MODULE_DIR.parent
DB_DIR = PAR_DIR / 'db'
