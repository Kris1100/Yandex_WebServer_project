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
        return '<YandexLyceumStudent {} {}>'.format(
            self.id, self.username)


# db.create_all()

user1 = User(username='student1',
             email='student1@yandexlyceum.ru',
             password=hashlib.md5('qwerty'.encode('utf-8')).hexdigest())

user2 = User(username='student2',
             email='student2@yandexlyceum.ru',
             password=hashlib.md5('password01'.encode('utf-8')).hexdigest())

# db.session.add(user1)
# db.session.add(user2)
db.session.commit()


@app.route('/')
@app.route('/check_in', methods=['POST', 'GET'])
def form_sample():
    if request.method == 'GET':
        return '''<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <meta name="viewport"
                            content="width=device-width, initial-scale=1, shrink-to-fit=no">
                            <link rel="stylesheet"
                            href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                            integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
                            crossorigin="anonymous">
                            <title>Пример формы</title>
                          </head>
                          <body>
                            <h1>Форма для регистрации в суперсекретной системе</h1>
                            <form method="post">
                                <input type="email" class="form-control" id="email" aria-describedby="emailHelp" placeholder="Введите адрес почты" name="email">
                                <input type="password" class="form-control" id="password" placeholder="Введите пароль" name="password">
                                <input type="password" class="form-control" id="password again" placeholder="Введите пароль еще раз" name="password again">
                                
                                <div class="form-group form-check">
                                    <input type="checkbox" class="form-check-input" id="acceptRules" name="accept">
                                    <label class="form-check-label" for="acceptRules">Готов быть добровольцем</label>
                                </div>
                                <button type="submit" class="btn btn-primary">Записаться</button>
                            </form>
                          </body>
                        </html>'''
    elif request.method == 'POST':

        if request.form['password'] == request.form['password again'] and (request.form['accept'] == 'on') and request.form['email']:
            for i in User.query.all():
                if i.email == request.form['email']:
                    return redirect('/login')
            user = User(username=request.form['email'].split('@')[0],
                         email=request.form['email'],
                         password=hashlib.md5(request.form['password'].encode('utf-8')).hexdigest())

            db.session.add(user)
            db.session.commit()

            return redirect('/success')



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
    return "Привет, Яндекс! Я - Кристина"


if __name__ == '__main__':
    app.run(port=8081, host='127.0.0.1')
