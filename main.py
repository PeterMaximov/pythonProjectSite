from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dogs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
dogs_db = SQLAlchemy(app)


#class Dogs_Search(dogs_db.Model):
  #  pass


@app.route('/')
@app.route('/home', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        pass
    else:
        return render_template("index.html")


@app.route('/help')
def help():
    return render_template("help.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/test')
def test():
    return render_template("test.html")


@app.route('/result_search.html')
def result_search():
    return render_template("result_search.html")


if __name__ == '__main__':
    app.run(debug=True)
