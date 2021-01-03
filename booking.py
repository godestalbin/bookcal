from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
# from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Regexp

class BookingForm(FlaskForm):
    startDate = HiddenField('Start date', validators=[DataRequired(message='Date de début de séjour non sélectionnée')])
    endDate = HiddenField('End date', validators=[DataRequired(message='Date de fin de séjour non sélectionnée')])
    name = StringField('Name', validators=[DataRequired(message='Un nom est requis'), Length(min=10, max=50, message='Nom trop court/long')])
    mail = StringField('Mail', validators=[DataRequired(message='Un mail est requis'), Length(min=10, max=50, message='Mail trop court/long')]) #  Cannot get the regexp working: , Regexp('^[A-Z0-9+_.-]+@[A-Z0-9.-]+$', message='Format mail incorrect')
    phone = StringField('Phone', validators=[DataRequired(message='Un téléphone est requis'), Length(min=8, max=12, message='8 à 10 chiffres'), Regexp('[+]?\s?\d*', message='Format téléphone incorrect')])  # Optional +, optional space, repetition of numbers
    submit = SubmitField('Confirmer la réservation')