from flask import Flask, render_template, g, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dogs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
dogs_db = SQLAlchemy(app)
DATEBASE = 'static/DB/dogs.db'


class Dogs(dogs_db.Model):
    __tablename__ = 'breeds'
    id = dogs_db.Column(dogs_db.Text(), primary_key=True)
    photo = dogs_db.Column(dogs_db.Text(), nullable=False)
    size = dogs_db.Column(dogs_db.INTEGER(), nullable=False)
    hairiness = dogs_db.Column(dogs_db.INTEGER(), nullable=False)
    aggressiveness = dogs_db.Column(dogs_db.INTEGER(), nullable=False)
    training = dogs_db.Column(dogs_db.INTEGER(), nullable=False)
    need_for_care = dogs_db.Column(dogs_db.INTEGER(), nullable=False)
    purpose = dogs_db.Column(dogs_db.INTEGER(), nullable=False)
    origin = dogs_db.Column(dogs_db.Text(), nullable=False)
    time_origin = dogs_db.Column(dogs_db.TEXT(), nullable=False)
    weight = dogs_db.Column(dogs_db.TEXT(), nullable=False)
    height = dogs_db.Column(dogs_db.Text(), nullable=False)
    lifespan = dogs_db.Column(dogs_db.TEXT(), nullable=False)

    def __repr__(self):
        return '<Dogs> %r' % self.id


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

# для бд конец
#@app.before_request
#def before_request():
    #global db


@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
def index():
    dogs_con = []
    #with app.app_context():
       # for test in query_db('SELECT * FROM breeds'):  # поиск в таблице тест
       #     dogs = test['breed']
        #    dogs_con.append(dogs)
    if request.method == 'POST':
        pass
        #search = request.form['search']
    else:
        return render_template("index.html")#, dog=dogs_con)


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
    eu = []
    with app.app_context():
        for test in query_db('SELECT * FROM breeds'):  # поиск в таблице тест
            dogs = test['breed']
            dogs_eu.append(dogs)
    if request.method == 'POST':
        pass
    else:
        return render_template("europa.html", dogs_eu=dogs_eu)


@app.route('/test', methods=['POST', 'GET'])
def test():
    if request.method == 'POST':
        pass
    else:
        return render_template("test.html")


@app.route('/result_search.html', methods=['POST', 'GET'])
def result_search():
    inf_search = Dogs.query.all
    if request.method == 'POST':
        pass
    else:
        return render_template("result_search.html")


if __name__ == '__main__':
    app.run(debug=True)
