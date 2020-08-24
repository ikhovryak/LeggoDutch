from flask_wtf import FlaskForm
from wtforms.fields import TextField, SubmitField, IntegerField, FormField, StringField, FieldList
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed, FileRequired

class PurchasePersonCountForm(FlaskForm):
    person_count = IntegerField('Type in the number of people you want to split the cost with:', validators=[DataRequired()])
    submit_person_count = SubmitField('Next')

class PersonDetailForm(FlaskForm):
    person_name = StringField('Name')
    person_telephone = StringField('Phone Number')

class PurchasePersonDetailsForm(FlaskForm):
    """A form for one or more addresses"""
    persons = FieldList(FormField(PersonDetailForm), min_entries=1)
    submit_person_details = SubmitField('Next')
