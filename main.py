# To run and test the code you need to update 4 places:
# 1. Change MY_EMAIL/MY_PASSWORD to your own details.
# 2. Go to your email provider and make it allow less secure apps.
# 3. Update the SMTP ADDRESS to match your email provider.
# 4. Update birthdays.csv to contain today's month and day.
# See the solution video in the 100 Days of Python Course for explainations.


import smtplib
from email.mime.text import MIMEText
import datetime as dt
from random import randint
import pandas
import os

# import os and use it to get the Github repository secrets
SENDER_EMAIL = os.environ.get("MY_EMAIL")
SENDER_PASSWORD = os.environ.get("MY_PASSWORD")

# --- Configuration ---
SMTP_SERVER = 'smtp.fastmail.com'
PORT = 587 # or 465 for SSL
SUBJECT = 'Random Unrelated Email'


def sendmail():
    try:
        print(f"Connecting to {SMTP_SERVER}:{PORT}...")

        # 1. Connect to the server
        server = smtplib.SMTP(SMTP_SERVER, PORT)
        server.starttls()  # Secure the connection

        # 2. Log in
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        print("Login successful.")

        # 3. Send the email
        print(f"Attempting to send mail to {email}...")
        server.sendmail(SENDER_EMAIL, [email], msg.as_string())
        print("Email sent successfully!")

    except smtplib.SMTPDataError as e:
        # This block handles the server rejecting the message content
        print("\n **SMTPDataError Occurred!** ")
        print(f"Server Code: {e.smtp_code}")
        # The server's human-readable error message
        print(f"Server Message: {e.smtp_error.decode('utf-8')}")
        print("Possible causes: Recipient/Sender mismatch, invalid recipient, or content issues.")

    except smtplib.SMTPAuthenticationError:
        print(" Authentication failed. Check your username/password or App Password.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    finally:
        if 'server' in locals():
            server.quit()
            print("Connection closed.")

now = dt.datetime.now()
current_month = now.month
current_day = now.day

data = pandas.read_csv("birthdays.csv")
birthdays = data.to_dict(orient="records")
for entry in birthdays:
    if entry["month"] == current_month and entry["day"] == current_day:
        name = entry["name"]
        email = entry["email"]

        with open(f"letter_templates/letter_{randint(1,3)}.txt") as file:
            contents = file.read()
            contents = contents.replace("[NAME]", name)


        # --- Construct the message ---
        msg = MIMEText(contents)
        msg['Subject'] = SUBJECT
        # CRITICAL: This 'From' address should match SENDER_EMAIL
        msg['From'] = SENDER_EMAIL
        msg['To'] = email

        sendmail()
