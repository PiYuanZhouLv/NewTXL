from flask import Blueprint
from auth import require, switch_current

bp = Blueprint('album', __name__, 'resources', url_prefix='/album')

# bp.before_request(lambda *_: None)

@bp.route('/<int:AlbumID>/')
@require("login")
@switch_current
def index(current, AlbumID):
    if current == "admin":
        return bp.send_static_file("admindashboard.html")
    else:
        return bp.send_static_file("userdashboard.html")
    # return f'<h1>Hello! This is the index page of album {albumID}'

@bp.route('/<int:AlbumID>/dashdata', methods=["POST"])
@require('login')
@switch_current
def dashdata(current, AlbumID):
    if current == 'admin':
        return {
            "title": "测试标题",
            "logined": {
                "percent": 0.8,
                "not-list": ["张小三", "李大四"]
            },
            "finished": {
                "percent": 0.5,
                "not-list": ["张小三", "李大四", "王老五", "刘第七", "奥老八"]
            },
            "status": "receiving"
        }
    else:
        return {
            "title": "测试标题",
            "task": {
                "finished": [
                    {"id": "0", "name": "测试任务", "required": False},
                ],
                "not-finished": [
                    {"id": "1", "name": "测试任务", "required": False},
                    {"id": "2", "name": "测试任务", "required": True}
                ]
            },
            "login-name": "测试名",
            "released": "early"
        }