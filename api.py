import json
import requests
import webbrowser

from urllib.parse import urljoin, urlparse
from urllib.parse import parse_qs
from dataclasses import dataclass, field
from requests_oauthlib import OAuth2Session
from prettytable import PrettyTable

@dataclass
class Auth:
    """
    custom auth class that handles retrieving access tokens
    """
    authorize_base_url: str = "https://www.strava.com/oauth/authorize"
    token_base_url: str = "https://www.strava.com/oauth/token"

    access_token: str = ""
    client_id: str = ""
    client_secret: str = ""

    redirect_uri: str = "http://localhost"
    scope: str = "read_all,profile:read_all,activity:read_all"

    def set_creds(self, file_name: str):
        """
        get strava access token from creds.json
        """
        with open(file_name) as f:
            creds = json.load(f)

        self.client_id = creds["client_id"]
        self.client_secret = creds["client_secret"]
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
        print(f"{access_token=}")
        return

    def authorize(self):
        """
        authorize
        """
        print(f"authorizing...")

        # first, ask if user already has an access token
        has_token = input("do you already have an access token? [y/N]: ")
        if has_token == "y":
            token = input("token: ")
            self.access_token = token
            return

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
class SummaryActivity:
    """
    summary activity model
    """
    name: str = ""
    distance: float = 0.0
    moving_time: int = 0
    elapsed_time: int = 0
    total_elevation_gain: float = 0.0
    avg_speed: float = 0.0
    max_speed: float = 0.0

    def get_fields(self) -> list:
        """
        get list of fields
        """
        return [
            "name",
            "distance (miles)",
            "moving_time",
            "elapsed_time",
            "total_elevation_gain",
            "avg_speed",
            "max_speed"
        ]

    def get_row_data(self):
        """
        format data to be inputted into pretty table
        """
        return [
            self.name,
            self.convert_meters_to_miles(self.distance),
            self.moving_time,
            self.elapsed_time,
            self.total_elevation_gain,
            self.avg_speed,
            self.max_speed
        ]

    def convert_meters_to_miles(self, distance: float):
        """
        convert meters to miles
        """
        return distance * 0.000621371192


@dataclass
class Printer:
    """
    handles printing tables 
    """
    printer = PrettyTable()
    count: int = 15
    activities: list = field(default_factory=list)

    def get_columns(self):
        """
        get the columns for the table
        """
        fields = SummaryActivity().get_fields()
        return fields

    def print_summary(self):
        """
        print summary table
        """
        if self.activities is None:
            print(f"no activities...")
            return

        self.printer.field_names = self.get_columns()
        count = 0
        for activity in self.activities:
            if count < self.count:
                self.printer.add_row(activity.get_row_data())
            count += 1
        print(self.printer)
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

    def get(self, url: str, params: dict = None) -> dict:
        """
        handle get requests
        """
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        response = requests.get(url, headers=headers, params=params)
        return response.status_code, response.json()

    def get_all_activities(self) -> list:
        """
        get all athlete activities
        """
        url = self.generate_url("athlete/activities")
        params = {
            "per_page": 100
        }
        status_code, data = self.get(url, params=params)

        if status_code != 200:
            print(f"{status_code=}, {data=}")
            return

        all_activities = []
        for activity in data:
            act = SummaryActivity(
                name=activity["name"],
                distance=activity["distance"],
                moving_time=activity["moving_time"],
                elapsed_time=activity["elapsed_time"],
                total_elevation_gain=activity["total_elevation_gain"],
                avg_speed=activity["average_speed"],
                max_speed=activity["max_speed"]
            )
            all_activities.append(act)

        return all_activities


def main():
    # auth
    auth = Auth()
    auth.set_creds("./.creds.json")
    auth.authorize()

    # api
    api = API(access_token=auth.access_token)
    activities = api.get_all_activities()

    # printer
    p = Printer(activities=activities)
    p.print_summary()

    return


if __name__ == "__main__":
    main()
