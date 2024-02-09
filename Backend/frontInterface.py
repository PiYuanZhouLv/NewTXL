from flask import Blueprint
import os
import sys
sys.path.append(os.path.abspath('../'))
from DataShelf.client import Client

bp = Blueprint('api', __name__)

@bp.route('/new', methods="POST")
def new():
    ...

@bp.route('/search', methods="POST")
def search():
    ...
