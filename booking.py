from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
# from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Regexp

# All above no more needed for new version
from dataclasses import dataclass
from datetime import datetime
import re  #RegEx to control data provided by user

class BookingForm(FlaskForm):
    startDate = HiddenField('Start date', validators=[DataRequired(message='Date de début de séjour non sélectionnée')])
    endDate = HiddenField('End date', validators=[DataRequired(message='Date de fin de séjour non sélectionnée')])
    name = StringField('Name', validators=[DataRequired(message='Un nom est requis'), Length(min=10, max=50, message='Nom trop court/long')])
    mail = StringField('Mail', validators=[DataRequired(message='Un mail est requis'), Length(min=10, max=50, message='Mail trop court/long')]) #  Cannot get the regexp working: , Regexp('^[A-Z0-9+_.-]+@[A-Z0-9.-]+$', message='Format mail incorrect')
    phone = StringField('Phone', validators=[DataRequired(message='Un téléphone est requis'), Length(min=8, max=12, message='8 à 10 chiffres'), Regexp('[+]?\s?\d*', message='Format téléphone incorrect')])  # Optional +, optional space, repetition of numbers
    submit = SubmitField('Confirmer la réservation')

# # Previous version
# class Booking:
#     def __init__(self, startDate, endDate, room, name, mail, phone):
#         self.startDate = startDate
#         self.endDate = endDate
#         self.room = room
#         self.name = name
#         self.mail = mail
#         self.phone = phone


@dataclass
class Booking:
    roomId : str
    name : str = ''
    nameValid : str = ''
    mail : str = ''
    mailValid : str = ''
    phone : str = ''
    phoneValid : str = ''
    startDate : str = ''
    startDateValid : str = ''
    endDate : str = ''
    lockDays : list = ''

    def validate(self):
        if self.name == '': self.nameValid = 'is-invalid'
        else: self.nameValid = 'is-valid'
        print(len(self.startDate))
        if len(self.startDate) != 23:  # We did not receive the dates of stay
            self.startDateValid = 'is-invalid'
        else:
            self.endDate = self.startDate[13:23]
            self.startDate = self.startDate[0:10]
            # Need to control we have no lockDays inside the date selection
            # for range in self.lockDays:
            #     if datetime.strptime(range[0], '%Y-%m-%d') >= datetime.strptime(self.startDate, '%Y-%m-%d') and \
            #         datetime.strptime(range[0], '%Y-%m-%d') <= datetime.strptime(self.endDate, '%Y-%m-%d') or \
            #         datetime.strptime(range[1], '%Y-%m-%d') >= datetime.strptime(self.startDate, '%Y-%m-%d') and \
            #         datetime.strptime(range[1], '%Y-%m-%d') <= datetime.strptime(self.endDate, '%Y-%m-%d'):
            #         self.startDateValid = 'is-invalid'
            #         return
            self.startDateValid = 'is-valid'

        # mail at least one @
        if self.mail.find('@') == -1: self.mailValid = 'is-invalid'
        else: self.mailValid = 'is-valid'

        # phone must contains only +, digits, space
        # 6 digits or start with plus
        print(self.phone)
        self.phone = self.phone.replace(' ', '')
        if bool(re.match('^[0-9+]+$', self.phone)): 
            self.phoneValid = 'is-valid'
        else: self.phoneValid = 'is-invalid'

        if self.nameValid == 'is-invalid' or self.mailValid == 'is-invalid' or self.phoneValid == 'is-invalid' or self.startDateValid == 'is-invalid':
            print('validate=false')
            return False
        else:
            print('validate=true')
            return True
