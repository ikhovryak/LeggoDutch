from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField, DateField, IntegerField, FieldList, StringField, FormField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional,InputRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired
import datetime


class UploadForm(FlaskForm):
    receipt_image = FileField('Upload your receipt image', validators=[FileAllowed(['png', 'jpg']), FileRequired()])
    restaurant = TextField('Name of the restaurant', validators=[DataRequired()])
    date = DateField('Date' )
    num_friends = IntegerField("Number of friends", validators=[DataRequired()])
    submit = SubmitField('Submit')

class PersonDetailForm(FlaskForm):
    person_name = StringField('Name')
    person_telephone = StringField('Phone Number')

class PurchasePersonDetailsForm(FlaskForm):
    """A form for one or more addresses"""
    persons = FieldList(FormField(PersonDetailForm), min_entries=1)
    submit_person_details = SubmitField('Next')