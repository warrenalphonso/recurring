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
"""
import json
import os
from typing import TypedDict
from urllib.parse import urlencode
from urllib.request import urlopen

OAUTH_FILE = "oauth2_creds.json"


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


def source_env(path=".env"):
    """Source .env: https://stackoverflow.com/a/63484975/13697995"""
    with open(".env", "r") as f:
        for line in f.read().split("\n"):
            try:
                key, value = line.split('=')
                os.environ[key] = value
            except ValueError:
                pass


if __name__ == "__main__":
    try:
        source_env()

        # Variables Yagmail needs
        sender = os.environ["SENDER"]
        client_id = os.environ["CLIENT_ID"]
        client_secret = os.environ["CLIENT_SECRET"]
        refresh_token = os.environ["REFRESH_TOKEN"]
        # Make sure other environment variables exist
        os.environ["RECEIVER"]

        # Set access token so imaplib can use it
        access_token = refresh_access_token(
            client_id, client_secret, refresh_token)["access_token"]

        # Delete last line if it was already defined
        if os.environ.get("ACCESS_TOKEN", None):
            with open(".env", "r") as f:
                lines = f.readlines()
            with open(".env", "w") as f:
                for line in lines[:-1]:
                    f.write(line)

        # Append to .env
        with open(".env", "a") as f:
            f.write(f"ACCESS_TOKEN={access_token}")

        os.environ["ACCESS_TOKEN"] = access_token

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
