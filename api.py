import json
import requests

from models import SummaryActivity

from urllib.parse import urljoin, urlparse
from urllib.parse import parse_qs

from dataclasses import dataclass, field

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

    def get_activities(self, count: int = 0) -> list:
        """
        get athlete activities. if count param set to 0, get all
        """
        url = self.generate_url("athlete/activities")
        params = {
            "per_page": count
        }
        status_code, data = self.get(url, params=params)

        if status_code != 200:
            print(f"{status_code=}, {data=}")
            return

        all_activities = []
        for c, activity in enumerate(data):
            act = SummaryActivity(
                id=c+1,
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