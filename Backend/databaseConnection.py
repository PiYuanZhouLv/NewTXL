import os
import sys
sys.path.append(os.path.abspath('../'))
from DataShelf.client import Client


def get_database() -> Client:
    return Client(('127.0.0.1', 12345))
