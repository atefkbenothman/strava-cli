import json
import requests
import webbrowser
import datetime

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
            "distance (mi)",
            "moving_time",
            "elapsed_time",
            "total_elevation_gain (ft)",
            "avg_speed",
            "max_speed"
        ]

    def get_row_data(self):
        """
        format data to be inputted into pretty table
        """
        return [
            self.name,
            f"{self.convert_meters_to_miles(self.distance):.2f}",
            self.convert_seconds_to_hours(self.moving_time),
            self.convert_seconds_to_hours(self.elapsed_time),
            f"{self.convert_meters_to_feet(self.total_elevation_gain):.2f}",
            f"{self.convert_meters_per_second_to_miles_per_hour(self.avg_speed):.2f}",
            f"{self.convert_meters_per_second_to_miles_per_hour(self.max_speed):.2f}",
        ]

    def get_totals_row_data(self, activity_list: list) -> list:
        """
        calculate the total for the given activities
        """
        total_distance: float = 0.0
        total_moving_time: int= 0.0
        total_elapsed_time: int = 0.0
        total_total_elevation_gain: float = 0.0

        rows = []
        for activity in activity_list:
            total_distance += activity.distance
            total_moving_time += activity.moving_time
            total_elapsed_time += activity.elapsed_time
            total_total_elevation_gain += activity.total_elevation_gain
            rows.append(activity)

        total = SummaryActivity(
            name="Total:",
            distance=total_distance,
            moving_time=total_moving_time,
            elapsed_time=total_elapsed_time,
            total_elevation_gain=total_total_elevation_gain,
            avg_speed=0.0,
            max_speed=0.0
        )
        activity_list.append(total)
        return activity_list

    def get_avg_row_data(self, activity_list: list) -> list:
        """
        calculate the avg for the given activities
        """
        total_distance: float = 0.0
        total_moving_time: int= 0.0
        total_elapsed_time: int = 0.0
        total_total_elevation_gain: float = 0.0
        total_avg_speed: float = 0.0
        total_max_speed: float = 0.0

        rows = []
        for activity in activity_list:
            total_distance += activity.distance
            total_moving_time += activity.moving_time
            total_elapsed_time += activity.elapsed_time
            total_total_elevation_gain += activity.total_elevation_gain
            total_avg_speed += activity.avg_speed
            total_max_speed += activity.max_speed
            rows.append(activity)

        total = SummaryActivity(
            name="Total:",
            distance=total_distance,
            moving_time=total_moving_time,
            elapsed_time=total_elapsed_time,
            total_elevation_gain=total_total_elevation_gain,
            avg_speed=0.0,
            max_speed=0.0
        )
        activity_list.append(total)

        # calculate average
        avg_distance = total_distance / len(rows)
        avg_moving_time = total_moving_time / len(rows)
        avg_elapsed_time = total_elapsed_time / len(rows)
        avg_elevation_gain = total_total_elevation_gain / len(rows)
        avg_avg_speed = total_avg_speed / len(rows)
        avg_max_speed = total_max_speed / len(rows)

        avg = SummaryActivity(
            name="Avg:",
            distance=avg_distance,
            moving_time=avg_moving_time,
            elapsed_time=avg_elapsed_time,
            total_elevation_gain=avg_elevation_gain,
            avg_speed=avg_avg_speed,
            max_speed=avg_max_speed
        )
        activity_list.append(avg)

        return activity_list

    def convert_meters_to_miles(self, distance: float):
        """
        convert meters to miles
        """
        return distance * 0.000621371192

    def convert_meters_to_feet(self, distance: float):
        """
        convert meters to feet
        """
        return distance / 0.3048

    def convert_seconds_to_hours(self, seconds: int):
        """
        convert seconds to hours
        """
        return str(datetime.timedelta(seconds=seconds))

    def convert_meters_per_second_to_miles_per_hour(self, mps: float):
        """
        convert meters/sec to miles/hour
        """
        return mps * 2.2369

@dataclass
class Printer:
    """
    handles printing tables 
    """
    printer = PrettyTable()
    activities: list = field(default_factory=list)

    def get_columns(self) -> list:
        """
        get the columns for the table
        """
        fields = SummaryActivity().get_fields()
        return fields

    def get_rows(self, activities: list) -> list:
        """
        get the rows for the table
        """
        rows = []
        for activity in activities:
            rows.append(activity.get_row_data())
        return rows

    def get_activities(self, count: int = 100) -> list:
        """
        get the rows for the table
        """
        activities = []
        counter = 0
        for activity in self.activities:
            if counter < count:
                activities.append(activity)
            counter += 1
        return activities

    def get_totals_row(self, activities: list) -> list:
        """
        get the totals row for the table
        """
        activities_with_total = SummaryActivity().get_totals_row_data(activities)
        return activities_with_total

    def get_avg_row(self, activities: list) -> list:
        """
        get the avg row for the table
        """
        activities_with_avg = SummaryActivity().get_avg_row_data(activities)
        return activities_with_avg

    def print_summary(self):
        """
        print summary table
        """
        if self.activities is None:
            print(f"no activities...")
            return

        self.printer.field_names = self.get_columns()
        self.printer.add_rows(self.get_activities(count=5))

        print(self.printer)
        return

    def print_summary_with_total(self, count: int = 10):
        """
        does the same thing as print summary but adds the 'total' row to the table
        """
        if self.activities is None:
            print(f"no activities...")
            return

        self.printer.field_names = self.get_columns()

        # add total row
        acts = self.get_activities(count=count)
        rows = self.get_rows(self.get_avg_row(acts))

        self.printer.add_rows(rows)

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
    p.print_summary_with_total(count=40)

    return


if __name__ == "__main__":
    main()
