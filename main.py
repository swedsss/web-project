from flask import Flask, render_template
from data import db_session
from blueprints import users_bp
from constants import *

app = Flask(__name__)
app.config['SECRET_KEY'] = APP_SECRET_KEY


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
