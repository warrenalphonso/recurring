import smtplib
import ssl
import csv
import os
from datetime import date
from email.mime.text import MIMEText


##
# SETUP MESSAGE
##
today_date = date.today()

# Sequences
# Choose post to email by counting days since starting
start_date_sequences = date(2020, 10, 31)

title_sequences = ""
url_sequences = ""
with open("sequences.csv") as f:
    r = csv.reader(f)
    for i, row in enumerate(r):
        if i == (today_date - start_date_sequences).days:
            title_sequences, url_sequences = row

message_sequences = MIMEText(
    f"""\
        <a href="{url_sequences}">{title_sequences}</a>\
        <br />\
        <a href="https://roamresearch.com/#/app/warrenalphonso">Think in Roam</a>\
        <br />\
        <br />\
        <p>Sent by github.com/warrenalphonso/recurring via Heroku!</p>\
    """, "html")
message_sequences["Subject"] = f"{title_sequences}"

# Toggl Monthly Review
toggl = today_date.day == 1
message_toggl = MIMEText(
    f"""\
        <p>Download the Toggl Detailed Report for the past month in CSV format \
        and see how it went. <b>Push the CSV to GitHub repo.</b></p>
        <br />\
        <p>Sent by github.com/warrenalphonso/recurring via Heroku!</p>\
    """, "html")
message_toggl["Subject"] = "Time for Toggl Monthly Review"

# GoodReads Annual Backup
goodreads = today_date.month == 1 and today_date.day == 1
message_goodreads = MIMEText(
    f"""\
        <p>Download my GoodReads data and save it somewhere.</p>\
        <br />\
        <p>Sent by github.com/warrenalphonso/recurring via Heroku!</p>\
    """, "html")
message_goodreads["Subject"] = "Download GoodReads Data"

##
# SETUP SMTP CLIENT
##

port = 465  # GMail requires connecting to port 465 if using SMTP_SLL()

context = ssl.create_default_context()

sender = "warrenalphonso.recurring@gmail.com"
password = os.environ.get("EMAIL_PASSWORD", None)
recipient = "warrenalphonso02@gmail.com"

message_sequences["From"] = sender
message_sequences["To"] = recipient

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    if password:
        server.login(sender, password)
        server.sendmail(sender, recipient, message_sequences.as_string())
        if toggl:
            message_toggl["From"] = sender
            message_toggl["To"] = recipient
            server.sendmail(sender, recipient, message_toggl.as_string())
        if goodreads:
            message_goodreads["From"] = sender
            message_goodreads["To"] = recipient
            server.sendmail(sender, recipient, message_goodreads.as_string())
    else:
        print("No password found!")
