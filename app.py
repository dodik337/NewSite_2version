from flask import render_template, Flask, request, redirect, url_for, session, g
from config import Config
from database.sqldb import FDataBase

import os, sqlite3

app = Flask(__name__)
app.config.from_object(Config)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'login.db')))

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
        return g.link_db

@app.route('/index', methods=['GET', 'POST'])
def start_page():
    return render_template('index.html', title='Главная')


@app.route('/login', methods=['POST', 'GET'])
def login():
    db = get_db()
    database = FDataBase(db)
    for data in database.getData():
        if 'userlogged' in session:
            return redirect(url_for('profile', username=session['userlogged']))
        elif request.method == 'POST' and request.form['username'] in data['user'] and request.form['psw'] in data['password']:
            session['userlogged'] = request.form['username']
            return redirect(url_for('start_page', username=session['userlogged']))
        return render_template('login_2var.html', title="Авторизация")

if __name__ == "__main__":
    app.run(debug=True)