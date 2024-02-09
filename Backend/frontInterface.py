from flask import Blueprint, request
import os
import sys
sys.path.append(os.path.abspath('../'))
from DataShelf.client import Client

bp = Blueprint('api', __name__, url_prefix='/api')
# db = Client(('127.0.0.1', 12345))

@bp.route('/new', methods=["POST"])
def new():
    return {
        "type": "success",
        "nid": 0
    } if request.form['invite code'] == '1145141919810' else {
        "type": "invite code invalid"
    }

@bp.route('/search', methods=["POST"])
def search():
    return [
        ('高二（1）班同学录', 0),
        ('高三（0）班同学录', 1),
        ('你猜是谁的同学录', 2),
        ('圆周率研究小组~', 3)
    ]
