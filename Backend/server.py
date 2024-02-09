from flask import Flask
import os
from frontInterface import bp as interfacebp
from album import bp as albumbp

app = Flask(__name__, static_folder='resources')

app.register_blueprint(interfacebp)
app.register_blueprint(albumbp)

@app.route('/')
@app.route("/<path:path>")
def home(path='homepage.html'):
    if not os.path.abspath(os.path.join('resources', path)).startswith(os.path.abspath('resources')):
        return 403
    else:
        return app.send_static_file(path)

if __name__ == '__main__':
    app.run('0.0.0.0', 11451, True)
