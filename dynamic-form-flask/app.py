from flask import Flask, render_template, url_for, redirect, current_app, request
from forms import PurchasePersonCountForm, PersonDetailForm, PurchasePersonDetailsForm

app = Flask(__name__)

@app.route("/people", methods=["GET", "POST"])
def people_count():

    person_count_form = PurchasePersonCountForm()
    if person_count_form.submit_person_count.data and person_count_form.validate_on_submit():
        
        return redirect(url_for('people_details', count=person_count_form.person_count.data))

    return render_template('placeholder.html', person_count_form=person_count_form, title="Number of people")

@app.route("/people_details", methods=["GET", "POST"])
def people_details():
    count = request.args.get('count')
    person_details = []
    for i in range(count):
        person_details.append({"person_name": "Name", "person_telephone": "Telephone"})
    form = PurchasePersonDetailsForm(persons=person_details)

    if form.validate_on_submit():
        pass # .......

    return render_template("placeholder.html", form=form)

