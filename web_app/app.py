from flask import Flask, render_template, url_for, redirect, current_app, request, flash
from flask_sqlalchemy import SQLAlchemy
import secrets
from forms import UploadForm, PurchasePersonDetailsForm, PersonDetailForm
import os.path
from os import path
import time
import glob
from PIL import Image
import pandas as pd
import json
from twilio_message import send_message

from CRAFT import imgproc
from end2end.end2end import text_main_engine

app = Flask(__name__)
speech_key, service_region = "c87da06e1dfe4dd3b6e58fa41ec19c95", "eastus"
app.config['SECRET_KEY'] = "4cf9c9881c554ef032f3a12c7f225dea"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


def get_food_items_using_PyTorch(image):
    """ This is just a dummy function for now, replace with PyTorch algorithm.
    Input: Pillow image file (png or jpg)
    Output: Pandas Dataframe with "Food" and "Price" columns 
    """

    food = text_main_engine(image)

    # food = {
    #     "Pasta Bolognese":12.50,
    #     "Pasta Carbonara":13.00,
    #     "Pizza": 10.00,
    #     "Cheesecake": 8.00
    # }
    
    df = pd.DataFrame(list(food.items()), columns = ['Food','Price'])
    
    length = df.shape[0]
    df["Friend"] = ["" for i in range(length)]
    
    return df

class Params():
    """Params class to take care of data handling (my bad for not doing it properly with a database)"""
    # friends dictionary contains this by default, changes to new values once user inputs their guets names
    friends_dict = {
    "Iryna Khovryak":+14841111111,
    "Sam Tan": +14840000000,
    "Quan Phan": +14842222222
    }

    # FOOD_DF is the main df with food items, prices and owners, empty at the beginning
    FOODS_DF = pd.DataFrame() 



@app.route("/")
def home():
    return render_template('index.html', title="Reconnect - Main")


@app.route("/get_main_data",  methods=["GET", "POST"])
def get_main_data():
    """
    First page after index page. Takes in restaurant, date, guest number and photo receipt data.
    After form submission, redirects to the "people_details" page that gets the names and phones for each guest
    """
    upload_form = UploadForm()

    if upload_form.validate_on_submit():
        restaurant = upload_form.restaurant.data
        date = upload_form.date.data
        num_friends = int(upload_form.num_friends.data)

        if upload_form.receipt_image.data:
            # image = Image.open(upload_form.receipt_image.data)
            image = imgproc.loadImage(upload_form.receipt_image.data)

            Params.FOODS_DF = get_food_items_using_PyTorch(image)

            # when form is validated and submitted, go to entering individual people's details
            return redirect(url_for('people_details', restaurant=restaurant, date=date, count=num_friends))
    return render_template('get_main_data.html', title="Upload Data", upload_form=upload_form)


@app.route("/people_details", methods=["GET", "POST"])
def people_details():
    """
    Route to page for entering individual guests' info.
    After form submission, redirects to the "result" page with the table of foods and prices 
    """
    count = int(request.args.get('count'))
    

    if request.method == 'POST':
        restaurant = request.args.get('restaurant')
        date = request.args.get('date')
        names = request.form.getlist('names')
        phones = request.form.getlist('phones')
        Params.friends_dict = dict(zip(names, phones))
        return redirect(url_for('result', restaurant=restaurant, date=date))
        
    return render_template("people_details.html", title="Enter Guests", count=count)

@app.route("/result",  methods=["GET", "POST"])
def result():
    """
    Route to the page with data (food, price) extracted from receipt that lets you choose who ate what.
    After form submission, redirects to "final_individual_totals" page that shows individual totals
    """
    restaurant = request.args.get('restaurant')
    date = request.args.get('date')
    # length = Params.FOODS_DF.shape[0]
    # Params.FOODS_DF["Friend"] = ["" for i in range(length)]
    
    if request.method == 'POST':
        friends_items = request.form.getlist('friend_phone')
        
        names = []
        phones = []
        for friend in friends_items:
            cur_friend = eval(friend) 
            names.append(cur_friend[0])
            phones.append(cur_friend[1])

        Params.FOODS_DF["Friend"] = names
        Params.FOODS_DF["Phone"] = phones
        return redirect(url_for('final_individual_totals', restaurant=restaurant, date=date))

    return render_template("result.html", friends_list=Params.friends_dict, column_names=Params.FOODS_DF.columns.values, row_data=list(Params.FOODS_DF.values.tolist()), input_column="Friend", zip=zip)

@app.route("/final_individual_totals",  methods=["GET", "POST"])
def final_individual_totals():
    """
    Route to the page that displays summed up totals for each person.
    After clicking "Send text reminders" button, should send text messages to all the guests
    """
    restaurant = request.args.get('restaurant')
    date = request.args.get('date')
    personal_total_df = Params.FOODS_DF.groupby(['Friend']).sum().reset_index()
    # replace from_number with twilio phone number. Make sure you register the phone number you want to message to on twilio account if not your message will not reach
    # the phone number. This is a limitation of a trial account.
    from_number = "+17865634468"

    print(personal_total_df)
    if request.method == 'POST':
        for index, row in personal_total_df.iterrows():
            price = row['Price']
            message_text = "Hello! Just a reminder to pay $%.2f to the host for your meal at %s on %s!" % (price, restaurant, date)
            send_message(from_number, row['Phone'], message_text)

        
        flash('Text messages were sent!', 'success')
        pass


    return render_template("final_calculations.html", column_names=personal_total_df.columns.values, row_data=list(personal_total_df.values.tolist()), link_column="Food", zip=zip)

if __name__ == '__main__':
    app.run(debug=True)
