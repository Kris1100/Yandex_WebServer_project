import hashlib

from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy

from loginform import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(120), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User {} {}>'.format(
            self.id, self.username)


db.create_all()
db.session.commit()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///t.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db1 = SQLAlchemy(app)


class Text(db1.Model):
    id = db1.Column(db1.Integer, primary_key=True)
    user = db1.Column(db1.Integer, unique=False, nullable=False)
    text = db1.Column(db1.String(1024), unique=False, nullable=False)

    def __repr__(self):
        return '<Text {}>'.format(self.id)


db1.create_all()
db1.session.commit()


@app.route('/')
@app.route('/check_in', methods=['POST', 'GET'])
def form_sample():
    form = LoginForm()

    if request.method == 'GET':
        return render_template('check_in.html', title='Регистрация', form=form)
    elif request.method == 'POST':

        if request.form['password'] == request.form['password again'] and (request.form['accept'] == 'on') and \
                request.form['email']:
            for i in User.query.all():
                if i.email == request.form['email']:
                    return redirect('/login')
            user = User(username=request.form['about'],
                        email=request.form['email'],
                        password=hashlib.md5(request.form['password'].encode('utf-8')).hexdigest())

            db.session.add(user)
            db.session.commit()

            return redirect('/success')
    return render_template('check_in.html', title='Профиль', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        f = request.form['username']
        f1 = request.form['password']

        for i in User.query.all():

            if i.email == f and (hashlib.md5(f1.encode('utf-8')).hexdigest() == i.password):
                return redirect('/success')

    return render_template('login.html', title='Авторизация', form=form)


@app.route('/success')
def index():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('Profile.html', title='Профиль', form=form)
    elif request.method == 'POST':

        if request.form['password'] == request.form['password again'] and (request.form['accept'] == 'on') and \
                request.form['email']:
            for i in User.query.all():
                if i.email == request.form['email']:
                    return redirect('/login')

            db.session.commit()

            return redirect('/success')
    return render_template('Profile.html', title='Профиль', form=form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
