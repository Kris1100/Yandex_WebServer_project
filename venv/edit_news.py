from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired


class AddNewsForm(FlaskForm):
    content = form-control('Text', validators=[DataRequired()])
    submit = SubmitField('Add')
