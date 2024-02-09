from flask import Blueprint

bp = Blueprint('album', __name__, url_prefix='/album')

@bp.route('/<int:albumID>')
def index(albumID):
    return f'<h1>Hello! This is the index page of album {albumID}'
