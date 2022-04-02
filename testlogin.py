import flask

app = flask.Flask(__name__)
app.secret_key = 'super secret string'  # Change this!

import flask_login

login_manager = flask_login.LoginManager()

login_manager.init_app(app)