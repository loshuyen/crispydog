import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import os

flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    "/Users/shuyen/Desktop/projects/crispydog/static/google_secret.json",
    scopes=["https://www.googleapis.com/auth/userinfo.profile"])
flow.redirect_uri = os.getenv("GOOGLE_AUTH_REDIRECT_URL")

def fetch_auth():
    authorization_url, state = flow.authorization_url(
    access_type="offline",
    include_granted_scopes="true",
    prompt="consent")
    return authorization_url

def get_credential(code):
    flow.fetch_token(code=code)
    credentials = flow.credentials
    return credentials