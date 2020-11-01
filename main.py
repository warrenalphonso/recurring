import smtplib, ssl, csv, os
from datetime import date 
from email.mime.text import MIMEText


##
# SETUP MESSAGE 
##

# Choose post to email by counting days since starting 
start_date = date(2020, 10, 31)
today_date = date.today()

title = ""
url = ""
with open("links.csv") as f:
    r = csv.reader(f)
    for i, row in enumerate(r):
        if i == (today_date - start_date).days:
            title, url = row
    
message = MIMEText(
    f"""\
        <a href="{url}">{title}</a>\
        <br />\
        <p>Sent by github.com/warrenalphonso/recurring via Heroku!</p>\
    """, "html")
message["Subject"] = f"{title}"


##
# SETUP SMTP CLIENT
##

port = 465 # GMail requires connecting to port 465 if using SMTP_SLL() 

context = ssl.create_default_context()

sender = "warrenalphonso.recurring@gmail.com"
password = os.environ.get("EMAIL_PASSWORD", None)
recipient = "warrenalphonso02@gmail.com"

message["From"] = sender
message["To"] = recipient

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server: 
    if password:
        server.login(sender, password)

        server.sendmail(sender, sender, message.as_string())

