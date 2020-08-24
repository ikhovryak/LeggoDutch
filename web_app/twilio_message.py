from twilio.rest import Client
import os

# refer to https://support.twilio.com/hc/en-us/articles/223181468-How-do-I-Add-a-Line-Break-in-my-SMS-or-MMS-Message-
# for message formatting opions

def send_message(from_number, to_number, message):

    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages.create(
                                body=message,
                                from_=from_number,
                                to=to_number
                            )