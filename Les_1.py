import hashlib

from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy

from add_news import AddNewsForm
from loginform import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

id_of_user = -2
f = ''
f1 = ''


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(120), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User {} {}>'.format(
            self.id, self.username)


class Text(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, unique=False, nullable=False)
    text = db.Column(db.String(3000), unique=False, nullable=False)

    def __repr__(self):
        return '<Text {}>'.format(self.id)


db.create_all()

user2 = User(username='student2',
             email='student2@yandexlyceum.ru',
             password=hashlib.md5('password01'.encode('utf-8')).hexdigest())

# db.session.add(user2)

db.session.commit()


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
    global f
    global f1
    global id_of_user

    form = LoginForm()
    if form.validate_on_submit():
        f = request.form['username']
        f1 = request.form['password']
        f1 = hashlib.md5(f1.encode('utf-8')).hexdigest()
        for i in User.query.all():
            if i.email == f and (f1 == i.password):
                id_of_user = i.id
                print(id_of_user)

                return redirect('/success')

    return render_template('login.html', title='Авторизация', form=form)


@app.route('/success')
def success():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('Profile.html', title='Профиль', form=form)

    elif request.method == 'POST':
        print(1)

    return render_template('Profile.html', title='Профиль', form=form)


@app.route('/add_news')
def add_news():
    global id_of_user
    form = AddNewsForm()

    if request.method == 'GET':
        return render_template('add_news.html', title='Добавить цель', form=form)

    elif request.method == 'POST':
        new = Text(user=id_of_user,
                   text=request.form['content'])

        db.session.add(new)
        db.session.commit()
        return redirect('/success')

    return render_template('add_news.html', title='Добавить цель', form=form)


# @app.route('/logout')
# def logout():
#     session.pop('username', 0)
#     session.pop('user_id', 0)
#     return redirect('/login')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
