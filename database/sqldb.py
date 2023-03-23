import sqlite3 as sq

#Подключение базы данных
def sql_on_start():
    global base, cur
    base = sq.connect('../login.db') #Если такой базы нету, то она создается
    cur = base.cursor()
    if base:
        print('DATABASE WAS CONNECTED SUCCESSFUL')
    base.execute("CREATE TABLE IF NOT EXISTS {}(id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT UNIQUE, password TEXT)".format("login"))
    base.commit()

#Функция объявляется
sql_on_start()


#Создаем класс
class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def addData(self, user, password):
        try:
            self.__cur.execute('INSERT INTO login VALUES(NULL, ?, ?)', (user, password))
            self.__db.commit()
        except sq.Error as e:
            print('Ошибка добавления в БД', str(e))
            return False
        return True

    def delData(self, id=0):
        try:
            if id == 0:
                self.__cur.execute("DELETE FROM login")
            else:
                self.__cur.execute(f"DELETE FROM login WHERE user == {id}")
            self.__db.commit()
        except sq.Error as e:
            print('Fail', str(e))
            return False
        return True

    def getData(self):
        try:
            self.__cur.execute("SELECT * FROM login")
            res = self.__cur.fetchall()
            return res
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
    print(db.getData())

