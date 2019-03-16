from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class AddNewsForm(FlaskForm):
    title = StringField('��������� �������', validators=[DataRequired()])
    content = TextAreaField('����� �������', validators=[DataRequired()])
    submit = SubmitField('��������')
