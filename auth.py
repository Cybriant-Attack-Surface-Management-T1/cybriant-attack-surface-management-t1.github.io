# This file handles the authentication, testing if container functions can
# be loaded through here
from google.oauth2 import service_account
import google.auth.transport.requests

# Path to your service account key file
SERVICE_ACCOUNT_FILE = ''

# Define the required scopes
SCOPES = ['']

def get_authenticated_session():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return google.auth.transport.requests.AuthorizedSession(credentials)
