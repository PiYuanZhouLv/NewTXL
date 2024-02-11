from flask import Blueprint, request, redirect
from databaseConnection import get_database
import hashlib
from auth import check_login, check_logout, change_pwd

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/new', methods=["POST"])
def new():
    db = get_database()
    if db.check_invite_code(request.form['invite code']):
        nid = db.new()
        table = db.set(nid)
        table['title'] = request.form['title']
        table['admin'] = hashlib.md5(request.form['password'].encode()).hexdigest()
        return {
            'type': 'success',
            'nid': nid
        }
    else:
        return {
            "type": "invite code invalid"
        }

@bp.route('/search', methods=["POST"])
def search():
    db = get_database()
    result = db.search(request.form['keyword'])
    return list(map(lambda x: (x[0], x[2], {"receiving":"正在收集", "paused": "暂停收集", "released": "已发布"}[db.get(x[2])['status']]), result))

@bp.route('/login', methods=["POST"])
def login():
    ok, need_change = check_login(request.form['AlbumID'], request.form['username'], request.form['password'])
    return {
        'ok': ok,
        'need_change': need_change
    }

@bp.route('/changepwd', methods=["POST"])
def changepwd():
    ok = change_pwd(request.form['AlbumID'], request.form['newpwd'])
    return {'ok': ok}

@bp.route('/logout', methods=["POST"])
def logout():
    ok = check_logout(request.form['AlbumID'])
    return {'ok': ok}
