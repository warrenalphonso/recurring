"""
The IMAP (Internet Message Access Protocol) lets us retrieve email messages
from an email server and manipulate them locally. It's not meant to support
sending emails - that's what SMTP (Simple Mail Transfer Protocol) is for.

This file uses IMAP via the imap_tools module, a wrappepr of Python's built-in
imaplib library. I found the imaplib library to be way too low-level.

Currently, all this file does is check for received emails over the last 24
hours from [email] and with the words "diary email" in the Subject. It stores
the contents of these emails in S3 container.
"""
import os
from imap_tools import MailBox
from main import source_env

if __name__ == "__main__":
    source_env()

    sender = os.environ["SENDER"]
    receiver = os.environ["RECEIVER"]
    access_token = os.environ["ACCESS_TOKEN"]

    # Use OAuth 2.0
    # mailbox.fetch() returns an iterator, so we can break early
    with MailBox("imap.gmail.com").xoauth2(sender, access_token) as mailbox:
        subjects = [msg.subject for msg in mailbox.fetch()]
        print(len(subjects))
