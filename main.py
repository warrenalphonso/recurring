import os
import sendgrid
from sendgrid.helpers.mail import *
from datetime import date
import csv


sender = From("warrenalphonso.recurring@gmail.com")
recipient = To("warrenalphonso02@gmail.com")

# Setup messages to send
messages = {}
today_date = date.today()

# Diary
messages["Diary Email"] = \
    """\
    <p>Reply to this email to write an entry into your diary. Feel free to \
    attach images or videos.</p>\
    <br />\
    <p>Some starters: \
    <ul>\
        <li>What's the coolest thing you did today?</li>\
        <li>Who did you talk to today?</li>\
        <li>What are you excited about tomorrow?</li>\
    </ul>\
    <br />\
    <p>Sent by github.com/warrenalphonso/recurring via Heroku!</p>\
    """

# Sequences
# Choose post to send by counting days since starting
start_date_sequences = date(2020, 10, 31)
title_sequence = ""
url_sequence = ""
with open("sequences.csv", "r") as f:
    r = csv.reader(f)
    for i, row in enumerate(r):
        if i == (today_date - start_date_sequences).days:
            title_sequence, url_sequence = row
if title_sequence:
    messages[title_sequence] = \
        f"""\
        <a href="{url_sequence}">{title_sequence}</a>\
        <br />\
        <a href="https://roamresearch.com/#/app/warrenalphonso">Think in Roam</a>\
        <br />\
        <br />\
        <p>Sent by github.com/warrenalphonso/recurring via Heroku!</p>\
        """

# Schur's _1000 Most Important Words_
start_date_schur = date(2021, 4, 16)
title_schur = ""
with open("schur.csv", "r") as f:
    r = csv.reader(f)
    for i, row in enumerate(r):
        if i == (today_date - start_date_schur).days:
            title_schur, = row
if title_schur:
    messages[title_schur] = \
        f"""\
        <p>Look up <b>{title_schur}</b> today. Create as many Anki cards as \
        you can think of that will make you remember <i>when</i> to use this \
        word. Use <b><a href="https://www.websters1913.com/">Webster's 1913 \
        Dictionary</a></b> to find more definitions.</p>\
        <br />\
        <br />\
        <p>Sent by github.com/warrenalphonso/recurring via Heroku!</p>\
        """

# Toggl Montly Review and Anki Monthly Backup
if today_date.day == 1:
    messages["Time for Toggl Monthly Review"] = \
        """\
        <p>Download the Toggl Detailed Report for the past month in CSV \
        format and see how it went. <b>Push the CSV to GitHub repo.</b></p>\
        <br />\
        <p>Sent by github.com/warrenalphonso/recurring via Heroku!</p>\
        """

    # AnkiWeb stores 30 backups by default but just in case...
    messages["Backup Anki"] = \
        """\
        <p>Export Anki as a `.colpkg` file and push to GitHub repo.</p>\
        """


# GoodReads Annual Backup
if today_date.month == 1 and today_date.day == 1:
    messages["Download GoodReads Data"] = \
        """\
        <p>Download my GoodReads data and save it somewhere.</p>\
        <br />\
        <p>Sent by github.com/warrenalphonso/recurring via Heroku!</p>\
        """


# Send
try:
    key = os.environ.get("SENDGRID_API_KEY", None)
    if key is None:
        raise Exception(
            "If running locally, source .env file. If on Heroku, set"
            " environment variables."
        )
    sg = sendgrid.SendGridAPIClient(key)
    for subject, html_content in messages.items():
        message = Mail(
            from_email=sender,
            to_emails=recipient,
            subject=Subject(subject),
            html_content=HtmlContent(html_content)
        )
        response = sg.send(message=message)
        if response.status_code != 202:
            raise Exception(
                "Response status code wasn't 202. It was: ",
                response.status_code)
except Exception as e:
    print(e)
