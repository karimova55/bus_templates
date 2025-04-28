from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class RouteForm(FlaskForm):
    name = StringField('Yo‘nalish nomi', validators=[DataRequired()])
    description = StringField('Tavsif')
    submit = SubmitField('Saqlash')
