import os
from flask import Flask, render_template, g, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

users_db = SQLAlchemy(app)
DATEBASE = 'static/DB/dogs.db'

LOGIN = None
PASSWORD = None


class Users(users_db.Model):
    id = users_db.Column(users_db.Integer, primary_key=True, autoincrement=True)
    us_login = users_db.Column(users_db.String(15), nullable=False)
    us_password = users_db.Column(users_db.String(20), nullable=False)

    def __repr__(self):
        return f'<Users> {self.id} {self.us_login} {self.us_password}'


class Favorite(users_db.Model):
    id = users_db.Column(users_db.Integer, primary_key=True, autoincrement=True)
    us_login = users_db.Column(users_db.String(15), nullable=False)
    us_password = users_db.Column(users_db.String(20), nullable=False)
    breed = users_db.Column(users_db.String(100), nullable=False)

    def __repr__(self):
        return f'<Users> {self.us_login} {self.us_password} {self.breed}'


# для бд начало
def get_db():
    db = getattr(g, '_datebase', None)
    if db is None:
        db = g._datebase = sqlite3.connect(DATEBASE)
    db.row_factory = sqlite3.Row
    return db


def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


# для запуска связи с бд следующая строка
#with app.app_context():
   # for test in query_db('SELECT * FROM breeds'): #поиск в таблице тест
     #   print(test['breed'], 'has the id', test['size'])  # пишешь название столбца и получаешь значение



@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        pass
    else:
        return render_template("index.html")


@app.route('/help', methods=['POST', 'GET'])
def help():
    if request.method == 'POST':
        pass
    else:
        return render_template("help.html")


@app.route('/about', methods=['POST', 'GET'])
def about():
    if request.method == 'POST':
        pass
    else:
        return render_template("about.html")


@app.route('/europa', methods=['POST', 'GET'])
def europa():
    dogs_eu = []
    dogs_eu_phot = []
    eu = ["Германия", "Великобритания", "Италия", "Англия", "Франция", "Россия", "Франция", "Бельгия", "Швейцария",
          "Хорватия", "Бельгия", "Чехия", "Афганистан", "Венгрия", "Турция", "СССР", "Испания", "Ирландия",
          "Германская империя", "Финляндия", "Армения"]
    with app.app_context():
        for test in query_db('SELECT * FROM breeds'):  # поиск в таблице тест
            if test['Country_of_Origin'] in eu:
                dogs = [test['breed'], "Страна появления: " + str(test['Country_of_Origin']),
                        "Эпоха появления: " + str(test['Time_of_origin_of_the_breed']), "Вес: " + str(test['Weight']),
                        "Длина: " + str(test['Height']), "Продолжительность жизни: " + str(test['Lifespan'])]
                dogs_eu.append(dogs)
                pho = test['photo']
                dogs_eu_phot.append(pho)
    if request.method == 'POST':
        pass
    else:
        return render_template("europa.html", dogs_eu=dogs_eu, dogs_eu_phot=dogs_eu_phot)


@app.route('/test', methods=['POST', 'GET'])
def test():
    if request.method == 'POST':
        pass
    else:
        return render_template("test.html")


@app.route('/result_search', methods=['POST', 'GET'])
def result_search():
    if request.method == 'POST':
        pass
    else:
        return render_template("result_search.html")


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        us_login = request.form['us_login']
        us_password = request.form['us_password']

        if Users.query.filter(Users.us_login == us_login).first():
            return redirect('login_er')
        else:
            user = Users(us_login=us_login, us_password=us_password)

            try:
                users_db.session.add(user)
                users_db.session.commit()
                return redirect('/home')
            except:
                return "Ошибка при регистрации"
    else:
        return render_template("login.html")


@app.route('/sign-up', methods=['POST', 'GET'])
def sign():
    global LOGIN, PASSWORD
    if request.method == 'POST':
        us_login = request.form['us_login']
        us_password = request.form['us_password']
        if Users.query.filter(Users.us_login == us_login, Users.us_password == us_password).first():
            LOGIN = us_login
            PASSWORD = us_password
            return redirect('/home')
        else:
            return redirect('/sign-up_er')
    else:
        return render_template("sign-up.html")


@app.route('/sign-up_er', methods=['POST', 'GET'])
def sign_er():
    global LOGIN, PASSWORD
    if request.method == 'POST':
        us_login = request.form['us_login']
        us_password = request.form['us_password']
        if Users.query.filter(Users.us_login == us_login, Users.us_password == us_password).first():
            LOGIN = us_login
            PASSWORD = us_password
            return redirect('/home')
        else:
            return redirect('/sign-up_er')
    else:
        return render_template("sign-up_er.html")


@app.route('/login_er', methods=['POST', 'GET'])
def login_er():
    if request.method == 'POST':
        us_login = request.form['us_login']
        us_password = request.form['us_password']

        if Users.query.filter(Users.us_login == us_login).first():
            return redirect('login_er')
        else:
            user = Users(us_login=us_login, us_password=us_password)

            try:
                users_db.session.add(user)
                users_db.session.commit()
                return redirect('/home')
            except:
                return "Ошибка при регистрации"
    else:
        return render_template("login_er.html")


@app.route('/favorites', methods=['POST', 'GET'])
def favorites():
    global LOGIN, PASSWORD
    if request.method == 'POST':
        us_login = LOGIN
        us_password = PASSWORD

        breed = request.form['breed']
        if LOGIN == None or LOGIN == "" or PASSWORD == None or PASSWORD == "":
            return redirect('login')
        else:
            fav = Favorite(us_login=us_login, us_password=us_password, breed=breed)

            try:
                users_db.session.add(fav)
                users_db.session.commit()
                return redirect('/favorites')
            except:
                return "Ошибка при регистрации"
    else:
        fav = Favorite.query.filter(Favorite.us_login == LOGIN, Favorite.us_password == PASSWORD)
        return render_template("favorites.html", fav=fav)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    with app.app_context():
        users_db.create_all()
    app.run(debug=True)
