from flask import Flask, render_template
from data import db_session
from constants import *

app = Flask(__name__)
app.config['SECRET_KEY'] = APP_SECRET_KEY


@app.route("/")
def root():
    return render_template('base.html', title=APP_NAME)


def main():
    db_session.global_init(DB_FILENAME)
    app.run()


if __name__ == '__main__':
    main()

