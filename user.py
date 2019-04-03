from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired


class UsForm(FlaskForm):
    photo = FileField('Photo', validators=[DataRequired()])

