from flask import Flask, request, jsonify, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from urllib.parse import parse_qs, urlparse

import os
import csv

from helpers import apology, make_call, update_call, end_call
from prompt_helpers import generate_greeting, understand_intent, continue_conversation

# folder to upload files
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'uploads')

# Define allowed files
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)


# set the upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/group', methods=["POST", "GET"])
def group():
    if request.method == "GET":
        return render_template('group.html')
    else:
        file = request.files['csv_file']
        # get the filename
        data_filename = secure_filename(file.filename)

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], data_filename)

        if data_filename != '':
            # save the file to the upload folder
            file.save(file_path)

        phone_numbers = []

        with open(file_path, newline='') as csvfile:
            data = csv.DictReader(csvfile)
            for row in data:
                phone_numbers.append((row['name'], row['phone']))
                
        if len(phone_numbers) == 0:
            return apology("No phone numbers found", 400)
        
        # Iterate through each phone number and name
        for i in range(len(phone_numbers)):
            if phone_numbers[i][1] == "":
                continue
            print(phone_numbers[i])
            # Make a call to the phone number
            call_sid = make_call(phone_numbers[i][1], continue_conversation(phone_numbers[i][0], "interested"))

            # preint the call sid
            print(call_sid)

        return redirect("/")

# create a function to call a single number
@app.route("/call", methods=["POST"])
def call():

    # check if phone number and file are missing
    phone_number = request.form.get("phone_number")
    customer_name = request.form.get("customer_name")

    if phone_number == "":
        return apology("Missing phone number", 400)
    if customer_name == "":
        customer_name = "Mester"
    
    # make sure the phone and name
    print(phone_number, customer_name)

    # generate greeting
    greeting = generate_greeting(customer_name)

    # Make a call to the phone number
    call_sid = make_call(phone_number, greeting)

    # preint the call sid
    print(call_sid)
        
    return redirect("/")

######################################
# The flow for the Chatbot
######################################

@app.route("/gather", methods=["GET"])
def gather():
    parsed_url = urlparse(request.url)
    params = parse_qs(parsed_url.query)

    user_input = params.get("SpeechResult", [None])[0]
    call_sid = params.get("CallSid", [None])[0]

    # understand the user input
    intention = understand_intent(user_input)

    # branch the conversation based on the user's intention
    # these are the intention branches: interested, not_interested, not_sure, end_call
    if intention == "end_call":       
        end_call(call_sid)
    else:
        intention = "not_sure"
        speech = continue_conversation(user_input, intention)
        update_call(call_sid, speech)

    return intention
    
# Run the Flask app
if __name__ == "__main__":
    app.run()