import json
import requests
import webbrowser

from urllib.parse import urljoin, urlparse
from urllib.parse import parse_qs
from dataclasses import dataclass

from requests_oauthlib import OAuth2Session

@dataclass
class Auth:
    """
    custom auth class that handles retrieving access tokens
    """
    authorize_base_url: str = "https://www.strava.com/oauth/authorize"
    token_base_url: str     = "https://www.strava.com/oauth/token"

    access_token: str  = ""
    client_id: str     = ""
    client_secret: str = ""

    redirect_uri: str = "http://localhost"
    scope: str        = "read_all,profile:read_all,activity:read_all"

    def set_creds(self, file_name: str):
        """
        get strava access token from creds.json
        """
        with open(file_name) as f:
            creds = json.load(f)

        self.client_id = creds["client_id"]
        self.client_secret = creds["client_secret"]
        self.access_token = creds["access_token"]
        return

    def get_token_code(self, url: str) -> str:
        """
        parse the url for the token code
        """
        parsed_url = urlparse(url)
        code = parse_qs(parsed_url.query)["code"][0]
        return code

    def token_exchange(self, code: str):
        """
        get token 
        """
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code"
        }
        response = requests.post(self.token_base_url, data=data)

        # set access token
        if "access_token" not in response.json():
            print(f"error setting access token!")
            return

        access_token = response.json()["access_token"]
        self.access_token = access_token
        return

    def authorize(self):
        """
        authorize
        """
        print(f"authorizing...")

        # generate auth url
        strava = OAuth2Session(self.client_id, scope=self.scope, redirect_uri=self.redirect_uri)
        auth_url, state = strava.authorization_url(self.authorize_base_url)

        # open url in browser
        webbrowser.open(auth_url, new=1, autoraise=True)

        # authorize + parse url
        auth_url = input("paste authorization url: ")
        code = self.get_token_code(auth_url)

        # get access token
        self.token_exchange(code)
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
        return response.json()

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
    auth.set_creds("./.creds.json")
    auth.authorize()

    # api
    api = API(access_token=auth.access_token)
    api.get_all_activities()

    return


if __name__ == "__main__":
    main()
