from flask import render_template, Flask, request, redirect, url_for, session, g
from forms import LoginForm
from config import Config

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



users_passwords = {'1': '12', 'user2': 'password2', 'user3': 'password3',
                   'user4': 'password4', 'user5': 'password5', 'user6': 'password6', 'user7': 'password7',
                   'user8': 'password8'}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'userlogged' in session:
        return redirect(url_for('profile', username=session['userlogged']))
    elif request.method == 'POST' and request.form['username'] in users_passwords \
            and request.form['psw'] == users_passwords[request.form['username']]:
        session['userlogged'] = request.form['username']
        return redirect(url_for('start_page', username=session['userlogged']))
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)