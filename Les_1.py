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
session = {}


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
        return '<Text {} {}>'.format(self.id, self.text)


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
            if User.query.filter_by(email=request.form['email'], password=f1).first():
                return redirect('/login')
            user = User(username=request.form['about'],
                        email=request.form['email'],
                        password=hashlib.md5(request.form['password'].encode('utf-8')).hexdigest())

            db.session.add(user)
            db.session.commit()
            return redirect('/login')
    return render_template('check_in.html', title='Профиль', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    global session

    form = LoginForm()

    user_name = form.username.data

    if form.validate_on_submit():
        f = request.form['username']
        f1 = request.form['password']
        f1 = hashlib.md5(f1.encode('utf-8')).hexdigest()
        if User.query.filter_by(email=f, password=f1).first():
            session['username'] = user_name
            session['user_id'] = User.query.filter_by(email=f, password=f1).first().id
            return redirect('/success')

    return render_template('login.html', title='Авторизация', form=form)


@app.route('/success')
def success():
    if 'username' not in session:
        return redirect('/login')
    form = LoginForm()
    if request.method == 'GET':
        return render_template('Profile.html', title='Профиль', form=form)

    elif request.method == 'POST':
        pass

    return render_template('Profile.html', title='Профиль', form=form)


@app.route('/add_news', methods=['GET', 'POST'])
def add_news():
    global session
    if 'username' not in session:
        return redirect('/login')

    form = AddNewsForm()
    if request.method == 'GET':
        return render_template('add_news.html', title='Добавить цель', form=form)

    elif request.method == 'POST':
        new = Text(user=session['user_id'],
                   text=request.form['content'])

        db.session.add(new)
        db.session.commit()
        return redirect('/success')

    return render_template('add_news.html', title='Добавить цель', form=form)


@app.route('/all_of', methods=['GET', 'POST'])
def all_of():
    global session

    form = AddNewsForm()

    if 'username' not in session:
        return redirect('/login')
    news = Text.query.filter_by(user=session['user_id'])
    for i in news:
        print(i)
    return render_template('all_of.html', title='Добавить цель', form=form, news=news)


@app.route('/delete_news/<int:news_id>', methods=['GET'])
def delete_news(news_id):
    if 'username' not in session:
        return redirect('/login')
    nm = Text.query.filter_by(user=session['user_id'])
    print(nm[news_id])
    nm.delete(news_id)
    return redirect("/success")


@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    return redirect('/login')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
