from flask import render_template, Flask, request, redirect, url_for, session, g, abort, flash
from config import Config
from database.sqldb import FDataBase


import os, sqlite3

app = Flask(__name__)
app.config.from_object(Config)
app.config.update(dict(DATABASE=os.path.join(app.root_path,'../users.db')))



def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
        return g.link_db

@app.route('/', methods=['GET', 'POST'])
def first_page():
    return redirect(url_for('start_page'))

@app.route('/profile_register', methods=['POST', 'GET'])
def prof_reg():
    db = get_db()
    database = FDataBase(db)
    if request.method == 'POST':
        if len(request.form['name']) > 3 and len(request.form['info']) > 6:
            res = database.addProfile(request.form['name'], session['userlogged'], request.form['info'])
            if not res:
                flash('Профиль добававлен успешно', category='success')
            else:
                flash('Ошибка добавления профиля', category='error')
        else:
            flash('Ошибка добавления профиля', category='error')

    return render_template('addprofile.html', title='Добавить профиль', menu=database.getMenu())

@app.route('/profile')
def profile():
    db = get_db()
    database = FDataBase(db)
    if 'userlogged' in session:
        if 'admin' in session['userlogged']:
            return render_template('admin.html', title='Admin', menu=database.getMenu())
        else:
            return render_template('profile.html', title="Профиль", menu=database.getMenu(), profile=database.getProfile('Петя', session['userlogged']))
    else:
        return redirect(url_for('start_page'))

#Main page
@app.route('/index', methods=['GET', 'POST'])
def start_page():
    db = get_db()
    database = FDataBase(db)
    return render_template('index.html', menu=database.getMenu())

#Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    db = get_db()
    database = FDataBase(db)
    if 'userlogged' in session:
        return redirect(url_for('start_page', username=session['userlogged']))
    if request.method == 'POST':
        if request.form['password'] == request.form['password2']:
            if database.addData(request.form["username"], request.form["password"]):
                session['userlogged'] = request.form['username']
                return redirect(url_for('start_page', username=session['userlogged']))
            else:
                return render_template('register.html', title='Регистрация')
    return render_template('register.html', title='Регистрация')

#Login
@app.route('/login', methods=['POST', 'GET'])
def login():
    db = get_db()
    database = FDataBase(db)
    if 'userlogged' in session:
        return redirect(url_for('start_page', username=session['userlogged']))
    elif request.method == 'POST' and database.getData(request.form['username'], request.form['password']):
        session['userlogged'] = request.form['username']
        return redirect(url_for('start_page', username=session['userlogged']))
    return render_template('login.html', title="Авторизация")

@app.route('/quit', methods=['GET', 'POST'])
def quit_login():
    db = get_db()
    database = FDataBase(db)
    if 'userlogged' in session:
        return render_template('quit_page.html', title='Выход', menu=database.getMenu())
    else:
        return redirect(url_for('start_page'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', title='Страница не найдена')

if __name__ == "__main__":
    app.run(debug=True)