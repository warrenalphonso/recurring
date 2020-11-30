import smtplib, ssl, csv, os
from datetime import date 
from email.mime.text import MIMEText


##
# SETUP MESSAGE 
##

# Choose post to email by counting days since starting 
start_date_sequences = date(2020, 10, 31)
today_date = date.today()

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

##
# SETUP SMTP CLIENT
##

port = 465 # GMail requires connecting to port 465 if using SMTP_SLL() 

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
    else: 
        print("No password found!")
