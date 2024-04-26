import os
import smtplib as s
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from gui.mysql_db import DatabaseHandler
from twilio.rest import Client
from datetime import datetime

database = DatabaseHandler()
conn, cursor = database.initialize_connection()

current_time = datetime.now().strftime("%H:%M:%S")

def send_email(image_filename, object_detected):
    # Send an email with the image as an attachment
    sender = os.environ['EMAIL_SENDER']
    password = os.environ['EMAIL_PASSWORD']

    query = "SELECT email FROM add_details"
    cursor.execute(query)
    rows = cursor.fetchall()
    
    receivers = [row[0] for row in rows]  # Extract email addresses from database rows
    if not receivers:
        print("No email addresses found in the add_details table.")
        return

    current_time = datetime.now().strftime("%H:%M:%S - %d/%m/%Y")
    subject = "Intruder detected - Please check logs and take action."
    email_body = f"<h1>Some stranger is trying to trespass, please ensure and assist. </h1><br>TimeStamp: {current_time}" 

    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = ', '.join(receivers)  # Convert the list of receivers to a comma-separated string
    message['Subject'] = subject
    message.attach(MIMEText(email_body, 'html'))

    if image_filename:
        # Attach the captured unknown face image
        filename = os.path.basename(image_filename)
        attachment = open(image_filename, "rb").read()

        image = MIMEImage(attachment, name=filename)
        message.attach(image)

    # SMTP connection
    with s.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=sender, password=password)

        connection.sendmail(
            from_addr=sender,
            to_addrs=receivers,
            msg=message.as_string(),
        )

    print(f"Email sent: {current_time}")


def call():
    account_sid = os.environ['TWILIO_SID']
    auth_token = os.environ['TWILIO_TOKEN']
    number = os.environ['TWILIO_NUMBER']

    client = Client(account_sid, auth_token)

    query = "SELECT phone_number FROM add_details"
    cursor.execute(query)
    rows = cursor.fetchall()
    if not rows:
        print("No phone numbers found in the add_details table.")
        return

    recpt = '+91' + str(rows[0][0])

    call = client.calls.create(
                            to=recpt,
                            from_=number,
                            url='https://handler.twilio.com/twiml/EH4ec1a9bb230f23eb949ccd0642754612',
                        )
    
    print(f"Call Initiated: {current_time}")

