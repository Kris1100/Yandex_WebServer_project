from flask import Flask
from flask import redirect
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

from loginform import LoginForm

app = Flask(__name__)
PYTHONHASHSEED = 0

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
             password=hash('qwerty'))

user2 = User(username='student2',
             email='student2@yandexlyceum.ru',
             password=hash('password01'))


# db.session.add(user1)
# db.session.add(user2)
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        for i in User.query.all():
            if i.email == form.username and (hash(form.password) == i.password):
                return redirect('/success')

    return render_template('login.html', title='Авторизация', form=form)


db.session.commit()

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
