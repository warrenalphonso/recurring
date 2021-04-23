"""
Yagmail uses the SMTP (Simple Mail Transfer Protocol) to make sending mail
through Gmail really easy. I'm using it because it's the main library I've
found that makes it easy to authenticate with OAuth 2.0.
"""
import os
import yagmail
from main import OAUTH_FILE, source_env

if __name__ == '__main__':
    source_env()

    sender = os.environ["SENDER"]
    receiver = os.environ["RECEIVER"]

    yag = yagmail.SMTP(user=sender,
                       oauth2_file=OAUTH_FILE)

    yag.send(to=receiver, subject="Hi from Yagmail",
             contents="Hey, it worked!")
