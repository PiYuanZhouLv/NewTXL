from flask import Blueprint
from auth import require, switch_current

bp = Blueprint('album', __name__, 'resources', url_prefix='/album')

# bp.before_request(lambda *_: None)

@bp.route('/<int:AlbumID>')
@require("login")
@switch_current
def index(current, AlbumID):
    if current == "admin":
        return bp.send_static_file("admindashboard.html")
    else:
        return bp.send_static_file("userdashboard.html")
    # return f'<h1>Hello! This is the index page of album {albumID}'
