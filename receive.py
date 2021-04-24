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
import json
import os
from typing import TypedDict
from urllib.parse import urlencode
from urllib.request import urlopen

from dotenv import load_dotenv
from imap_tools import MailBox


class Token(TypedDict):
    access_token: str
    token_type: str
    expires_in: int


def refresh_access_token(client_id, client_secret, refresh_token) -> Token:
    """Generate a refreshed access token.

    Inspired by:
        https://github.com/kootenpv/yagmail/blob/f24af871c670c29f30c34ef2a4ab5abc3b17d005/yagmail/oauth2.py#L63
    Background information:
        https://developers.google.com/youtube/v3/live/guides/auth/server-side-web-apps#OAuth2_Refreshing_a_Token
    """
    params = dict(client_id=client_id, client_secret=client_secret,
                  refresh_token=refresh_token, grant_type="refresh_token")
    encoded_params = urlencode(params).encode("utf-8")
    response = urlopen("https://accounts.google.com/o/oauth2/token",
                       encoded_params).read().decode("utf-8")
    return json.loads(response)


if __name__ == "__main__":
    load_dotenv()

    sender = os.environ["SENDER"]
    receiver = os.environ["RECEIVER"]
    access_token = os.environ["ACCESS_TOKEN"]

    # Use OAuth 2.0
    # mailbox.fetch() returns an iterator, so we can break early
    with MailBox("imap.gmail.com").xoauth2(sender, access_token) as mailbox:
        subjects = [msg.subject for msg in mailbox.fetch()]
        print(len(subjects))
