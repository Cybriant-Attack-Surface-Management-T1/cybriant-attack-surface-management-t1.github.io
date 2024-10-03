# This file handles making the API request, testing if container fucntions
# can be loaded through here
import requests
from auth import get_authenticated_sessiondxfagfdap;''

# Define the API endpoint
API_ENDPOINT = ''

def fetch_leaks():
    authed_session = get_authenticated_session()
    response = authed_session.get(API_ENDPOINT)

    if response.status_code == 200:
        data = response.json()
        # Process and display the leaks
        for leak in data['leaks']:
            print(f"Leak ID: {leak['']}, Description: {leak['']}")
    else:
        print(f"Error: {response.status_code}, {response.text}")

if __name__ == "__main__":
    fetch_leaks()
# can I find the leaks online