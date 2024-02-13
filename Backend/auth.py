from flask import session, redirect, request
import json
from databaseConnection import get_database
import hashlib
from functools import wraps

# def before_request():
#     if not session.get('login'):
#         session['login'] = '{}'
#         g.login_info = {}
def md5(message):
    return hashlib.md5(message.encode()).hexdigest()

def check_login(nid, username, password):
    db = get_database()
    if username != "admin":
        user_table = db.get(nid)['user']
        if not (username not in user_table or (password != user_table[username]['password'] if user_table[username]["type"] == "initial" else md5(password) != user_table[username]["password"])):
            session["login"] = json.dumps(json.loads(session.get('login') or "{}")|{nid:username})
            return True, user_table[username]["type"] == "initial"
    else:
        if md5(password) == db.get(nid)["admin"]:
            session["login"] = json.dumps(json.loads(session.get('login') or "{}")|{nid:username})
            return True, False
    return False, False

def check_logout(nid):
    nid = str(nid)
    d = json.loads(session.get('login') or "{}")
    if nid in d:
        d.pop(nid)
        session["login"] = json.dumps(d)
        return True

def change_pwd(nid, newpwd):
    nid = str(nid)
    d = json.loads(session.get('login') or "{}")
    if nid in d:
        db = get_database()
        db.set(nid)['user'][d[nid]]["password"] = md5(newpwd)
        db.set(nid)['user'][d[nid]]["type"] = "hash"
        return True

def reset_pwd(nid, username):
    ...

def require(level):
    def factory(f):
        @wraps(f)
        def inner(AlbumID, *args, **kwargs):
            d = json.loads(session.get('login') or "{}")
            if level == "login":
                if str(AlbumID) not in d:
                    if request.method == "GET":
                        return redirect(f'/login.html?AlbumID={AlbumID}')
                    else:
                        return "Login required", 401
            elif level == "user":
                if str(AlbumID) not in d:
                    if request.method == "GET":
                        return redirect(f'/login.html?AlbumID={AlbumID}')
                    else:
                        return "Login required", 401
                elif d[str(AlbumID)] == "admin":
                    return "Please use user account to login", 401
            elif level == "admin":
                if str(AlbumID) not in d:
                    if request.method == "GET":
                        return redirect(f'/login.html?AlbumID={AlbumID}&login=admin')
                    else:
                        return "Login required", 401
                elif d[str(AlbumID)] != "admin":
                    return "Please use admin account to login", 401
            return f(AlbumID, *args, **kwargs)
        return inner
    return factory

def switch_current(f):
    @wraps(f)
    def inner(AlbumID, *args, **kwargs):
        d = json.loads(session.get('login') or "{}")
        if str(AlbumID) not in d:
            current = "anymous"
        elif d[str(AlbumID)] != "admin":
            current = "user"
        else:
            current = "admin"
        return f(current, AlbumID, *args, **kwargs)
    return inner
