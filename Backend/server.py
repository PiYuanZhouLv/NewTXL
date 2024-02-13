from flask import Flask
import os
import secrets
from frontInterface import bp as interfacebp
from album import bp as albumbp

app = Flask(__name__, static_folder='resources')

if not os.path.exists('secret'):
    open('secret', 'w').write(secrets.token_hex())
app.config['SECRET_KEY'] = open('secret').read()

app.register_blueprint(interfacebp)
app.register_blueprint(albumbp)

@app.route('/')
@app.route("/<path:path>")
def resource(path='homepage.html'):
    if not os.path.abspath(os.path.join('resources', path)).startswith(os.path.abspath('resources')):
        return 403
    else:
        return app.send_static_file(path)

if __name__ == '__main__':
    app.run('0.0.0.0', 11451, True)
