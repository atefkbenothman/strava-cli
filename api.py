import json
import requests

from urllib.parse import urljoin
from dataclasses import dataclass

@dataclass
class Auth:
    """
    custom auth class that handles retrieving access tokens
    """
    authorize_url: str = "https://www.strava.com/oauth/authorize"
    client_id: str = ""
    client_secret: str = ""
    access_token: str = ""
    scope: str = "read_all,profile:read_all,activity:read_all"

    def set_creds(self, file_name: str):
        """
        get strava access token from config.json
        """
        with open(file_name) as f:
            creds = json.load(f)

        self.client_id = creds["client_id"]
        self.client_secret = creds["client_secret"]
        self.access_token = creds["access_token"]
        return

    def request_access(self, redirect_uri: str = "", response_type: str = ""):
        """
        initiate strava authorization
        """
        data = {
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "response_type": response_type,
            "scope": self.scope
        }
        response = requests.post(self.authorize_url, data=data)
        print(response.json())
        return


@dataclass
class API:
    """
    custom api class
    """
    base_url: str = "https://www.strava.com/api/v3/"
    access_token: str = ""

    def generate_url(self, endpoint: str) -> str:
        """
        generate the api url endpoint
        """
        return urljoin(self.base_url, endpoint)

    def get(self, url: str):
        """
        handle get requests
        """
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        response = requests.get(url, headers=headers)
        print(response.json())
        return

    def get_all_activities(self):
        """
        get all athlete activities
        """
        url = self.generate_url("athlete/activities")
        self.get(url)
        return


def main():
    # auth
    auth = Auth()
    auth.set_creds("./.config.json")
    auth.request_access(redirect_uri="localhost", response_type="code")

    # api
    api = API()
    # api.get_all_activities()

    return


if __name__ == "__main__":
    main()
