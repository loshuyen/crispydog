import google_auth_oauthlib.flow
import os
print(os.getcwd())
flow = google_auth_oauthlib.flow.Flow.from_client_config(
    {
        "installed":
        {
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "project_id": "crispydog",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": os.getenv("GOOGLE_CLIENT_KEY"),
            "redirect_uris": ["http://localhost", "https://crispydog.xyz"]
        }
    },
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