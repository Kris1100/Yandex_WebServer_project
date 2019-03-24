from flask import Flask, render_template, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test0.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class YandexLyceumStudent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    surname = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    group = db.Column(db.String(80), unique=False, nullable=False)
    year = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return '<YandexLyceumStudent {} {} {} {}>'.format(
            self.id, self.username, self.name, self.surname)


db.create_all()

user1 = YandexLyceumStudent(username='student1',
                            email='student1@yandexlyceum.ru',
                            name='ivan',
                            surname='ivanov',
                            group='pensa,lyceum2',
                            year=2)

user2 = YandexLyceumStudent(username='student2',
                            email='student2@yandexlyceum.ru',
                            name='petr',
                            surname='petrov',
                            group='moscow, lyceum1234',
                            year=1)


class SolutionAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(80), unique=False, nullable=False)
    code = db.Column(db.String(1000), unique=False, nullable=False)
    status = db.Column(db.String(50), unique=False, nullable=False)
    student_id = db.Column(db.Integer,
                           db.ForeignKey('yandex_lyceum_student.id'),
                           nullable=False)
    student = db.relationship('YandexLyceumStudent',
                              backref=db.backref('SolutionAttempts',
                                                 lazy=True))

    def __repr__(self):
        return '<SolutionAttempt {} {} {}>'.format(
            self.id, self.task, self.status)


db.session.add(user1)
db.session.add(user2)
db.session.commit()

print(YandexLyceumStudent.query.all())
print(YandexLyceumStudent.query.filter_by(name='petr').first())

user = YandexLyceumStudent.query.filter_by(name='petr').first()
attempt = SolutionAttempt(task='first task',
                          code='print("hello, yandex!")',
                          status='OK')
user.SolutionAttempts.append(attempt)
db.session.commit()
