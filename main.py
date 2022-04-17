from flask import Flask, render_template
from flask_login import LoginManager
from data import db_session
from data.models import User
from blueprints import users_bp
from constants import *

app = Flask(__name__)
app.config['SECRET_KEY'] = APP_SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route("/")
def root():
    params = {
        'app_name': APP_NAME
    }
    return render_template('base.html', **params)


def main():
    db_session.global_init(DB_FILENAME)
    app.register_blueprint(users_bp.blueprint)
    app.run()


if __name__ == '__main__':
    main()
