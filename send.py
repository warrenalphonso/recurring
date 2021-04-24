"""
To send and receive emails, we need to authenticate ourselves with Gmail. The
two libraries I'm using the send (Yagmail) and receive (imaplib) email allow
for authentication via OAuth 2.0.

Authenticating with OAuth 2.0 requires a Client ID, Client Secret, and Refresh
Token. The former two can be found by going to Google Console and creating a
new credential:
    console.cloud.google.com/apis/credentials
I store my Client ID and secret in 1Password, though losing them isn't a big
deal because you can just create a new one.

Yagmail expects a JSON file with keys for the user email address, as well as
these three strings. We've also got to get this information to Heroku. I think
it's a little tricky to remember not to commit a JSON file like that so I'll
just use a `.env` file to store this information, and create a JSON file here,
so that Yagmail can use it.

Yagmail uses the SMTP (Simple Mail Transfer Protocol) to make sending mail
through Gmail really easy. I'm using it because it's the main library I've
found that makes it easy to authenticate with OAuth 2.0.
"""
import csv
from datetime import date
import json
import os

from dotenv import load_dotenv
import yagmail

OAUTH_FILE = "oauth2_creds.json"

if __name__ == "__main__":
    # Create JSON file for yagmail's OAuth2.0
    try:
        load_dotenv()
        # Variables Yagmail needs
        sender = os.environ["SENDER"]
        client_id = os.environ["CLIENT_ID"]
        client_secret = os.environ["CLIENT_SECRET"]
        refresh_token = os.environ["REFRESH_TOKEN"]
        # Make sure other environment variables exist
        os.environ["RECEIVER"]

    # https://stackoverflow.com/a/15032444/13697995
    except (OSError, IOError):
        raise Exception("Make sure a `.env` file exists.")

    except KeyError:
        raise Exception(
            "Make sure all environment variables are set in `.env`. See"
            " `example.env` for which keys are necessary."
        )

    # Store in JSON file so Yagmail can access
    with open(OAUTH_FILE, "w") as f:
        json.dump(
            dict(email_address=sender,
                 google_client_id=client_id,
                 google_client_secret=client_secret,
                 google_refresh_token=refresh_token
                 ), f)

    # Setup yagmail
    sender = os.environ["SENDER"]
    receiver = os.environ["RECEIVER"]
    today = date.today()

    yag = yagmail.SMTP(user=sender,
                       oauth2_file=OAUTH_FILE)

    # Diary
    yag.send(to=receiver, subject=f"Diary: {today.strftime('%b %d, %Y')}",
             contents=(
                 "Reply to this email to write an entry into your diary. Feel "
                 "free to attach images or videos.\n"
                 "\n"
                 "Some starters:"
                 "\n"
                 "- What's the coolest thing you did today?\n"
                 "- Who did you talk to today?\n"
                 "- What are you excited about tomorrow?\n"
                 "\n"
                 "Sent by warrenalphonso/recurring via Heroku!"
             ))

    # Sequences
    # Choose post to send by counting days since starting
    start_date_sequences = date(2020, 10, 31)
    title_sequence, url_sequence = "", ""
    with open("content/sequences.csv", "r") as f:
        r = csv.reader(f)
        for i, row in enumerate(r):
            if i == (today - start_date_sequences).days:
                title_sequence, url_sequence = row
    if title_sequence:
        yag.send(to=receiver, subject=title_sequence,
                 contents=(
                     f"<a href='{url_sequence}''>{title_sequence}</a>\n"
                     "\n"
                     "<a href='https://roamresearch.com/#/app/warrenalphonso'>"
                     "Think in Roam</a>\n"
                     "\n"
                     "Sent by warrenalphonso/recurring via Heroku!"
                 ))
    else:
        yag.send(to=receiver, subject="Finished Sequences!",
                 contents=(
                     "Congrats! You've finished reading The Sequences.\n"
                     "Remove it from `send.py` in `warrenalphonso/recurring`."
                 ))

    # Schur's _1000 Most Important Words_
    start_date_schur = date(2021, 4, 16)
    title_schur = ""
    with open("content/schur.csv", "r") as f:
        r = csv.reader(f)
        for i, row in enumerate(r):
            if i == (today - start_date_schur).days:
                title_schur, = row
    if title_schur:
        yag.send(to=receiver, subject=title_schur,
                 contents=(
                     f"Look up <b>{title_schur}</b> today. Create as many "
                     "Anki cards as you can think of that will make you "
                     "remember <i>when</i> to use this word. Use <b>"
                     "<a href='https://www.websters1913.com/'>Webster's 1913 "
                     "Dictionary</a></b>\n"
                     "\n"
                     "Sent by warrenalphonso/recurring via Heroku!"
                 ))
    else:
        yag.send(to=receiver, subject="Finsihed Schur!",
                 contents=(
                     "Congrats! You've finished reading Norman Schur's "
                     "<i>1000 Most Important Words</i>.\n"
                     "Remove it from `send.py` in `warrenalphonso/recurring`."
                 ))

    # Toggl Montly Review and Anki Monthly Backup
    if today.day == 1:
        yag.send(to=receiver, subject="Time for Toggl Monthly Review",
                 contents=(
                     "Download the Toggl Detailed Report for the past month "
                     "in CSV format and see how it went. <b>Push the CSV to "
                     "GitHub repo.</b>\n"
                     "\n"
                     "Sent by warrenalphonso/recurring via Heroku!"
                 ))

        # AnkiWeb stores 30 backups by default but just in case...
        yag.send(to=receiver, subject="Backup Anki",
                 contents=(
                     "Export Anki as a `.colpkg` file and push to GitHub repo."
                 ))

    # GoodReads Annual Backup
    if today.month == 1 and today.day == 1:
        yag.send(to=receiver, subject="Download GoodReads Data",
                 contents=(
                     "Download my GoodReads data and save it somewhere.\n"
                     "\n"
                     "Sent by warrenalphonso/recurring via Heroku!"
                 ))
