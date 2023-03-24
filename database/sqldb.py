import sqlite3 as sq
from flask import Flask, g, request
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)
app.config.update(dict(DATABASE=os.path.join(app.root_path,'../users.db')))

#Подключение базы данных

def create_db():
    '''Вспомогательная функция для создания таблиц БД '''
    db = connect_db()
    with app.open_resource('sql_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def connect_db():
    conn = sq.connect(app.config['DATABASE'])
    conn.row_factory = sq.Row
    return conn

def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
        return g.link_db

#Создаем класс
class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def addData(self, username, password):
        try:
            self.__cur.execute('INSERT INTO users VALUES(NULL, ?, ?)', (username, password))
            self.__db.commit()
        except sq.Error as e:
            print('Ошибка добавления в БД', str(e))
            return False
        return True

    def delData(self, id):
        try:
            if id == 0:
                self.__cur.execute("DELETE FROM users")
            else:
                self.__cur.execute("DELETE FROM users WHERE id = {}".format(id))
            self.__db.commit()
        except sq.Error as e:
            print('Fail', str(e))
            return False
        return True

    def getData(self, username, password):
        try:
            self.__cur.execute("SELECT username, password FROM users WHERE ? = username AND ? = password", (username, password))
            res = self.__cur.fetchall()
            return res
        except sq.Error as e:
            print(str(e))
            return False

    def addMenu(self, title, url):
        try:
            self.__cur.execute("INSERT INTO menu VALUES (NULL, ?, ?)", (title, url))
            self.__db.commit()
        except sq.Error as e:
            print(str(e))
            return False

    def delMenu(self, id=0):
        try:
            if id == 0:
                self.__cur.execute("DELETE FROM menu")
            else:
                self.__cur.execute(f"DELETE FROM menu WHERE id == {id}")
            self.__db.commit()
        except sq.Error as e:
            print(str(e))
            return False

    def getMenu(self):
        try:
            self.__cur.execute("SELECT * FROM menu")
            res = self.__cur.fetchall()
            if res: return res
        except sq.Error as e:
            print(str(e))
            return False

if __name__ == "__main__":
    from app import connect_db
    db = connect_db()
    db = FDataBase(db)
    #print(db.addData('bob','123'))
    #print(db.addData('jonny', '1'))
    #print(db.addData('jon', '321'))
    #print(db.addData('jek', '825a'))
    #print(db.getData())
    #create_db()
    #print(db.delMenu(5))
    #print(db.addMenu('Админ-панель', 'admin_panel'))
    #print(db.delMenu(0))
    #print(db.addMenu('Главная', 'start_page'))
    #print(db.addMenu('Регистрация', 'register'))
    #print(db.delMenu(9))
    #print(db.addMenu('Admin Page', 'admin_page'))

