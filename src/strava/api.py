import requests
from urllib.parse import urljoin
from dataclasses import dataclass, fields, field
from typing import Union, Optional

from strava.models import (
    DetailedAthlete,
    SummaryActivity,
    ActivityTotal,
    ActivityStats,
)


@dataclass
class API:
    """
    custom api class
    """
    base_url: str = "https://www.strava.com/api/v3/"
    access_token: str = ""

    def _generate_url(self, endpoint: str) -> str:
        """
        generate the api url endpoint
        """
        return urljoin(self.base_url, endpoint)

    def _create_model(self, model, data: dict):
        """
        return the newly constructed model
        """
        new_model = model(**data)
        return new_model

    def _handle_response(self, response: requests.models.Response) -> Union[dict, None]:
        """
        return the json data from the response if the request was successful
        """
        if response.status_code != 200:
            print(f"{response.status_code=}, {response.text=}")
            return
        return response.json()

    def _get(self, url: str, params: dict = None) -> dict:
        """
        handle get requests
        """
        full_url = self._generate_url(url)
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        response = requests.get(full_url, headers=headers, params=params)
        data = self._handle_response(response)
        return data

    def get_athlete(self) -> DetailedAthlete:
        """
        get the current authenticated athlete.
        """
        data = self._get("athlete")
        athlete = self._create_model(
            model=DetailedAthlete,
            data=data
        )
        return athlete

    def get_athlete_stats(self, athlete_id: Optional[int] = None) -> ActivityStats:
        """
        return the stats of the athlete that was specified. if no athlete was specified,
        get the current logged in user
        """
        if athlete_id is None:
            athlete: DetailedAthlete = self.get_athlete()
            athlete_id = athlete.id

        url = f"athletes/{athlete_id}/stats"
        data = self._get(url)

        recent_ride_totals = self._create_model(
            model=ActivityTotal,
            data=data["recent_ride_totals"]
        )

        ytd_ride_totals = self._create_model(
            model=ActivityTotal,
            data=data["ytd_ride_totals"]
        )

        all_ride_totals = self._create_model(
            model=ActivityTotal,
            data=data["all_ride_totals"]
        )

        data = {
            "biggest_ride_distance": data["biggest_ride_distance"],
            "biggest_climb_elevation_gain": data["biggest_climb_elevation_gain"],
            "recent_ride_totals": recent_ride_totals,
            "ytd_ride_totals": ytd_ride_totals,
            "all_ride_totals": all_ride_totals
        }
        stats = self._create_model(
            model=ActivityStats,
            data=data
        )
        return stats

    def get_athlete_activities(self, count: Optional[int] = None) -> list:
        """
        returns the activities of the currently authenticated user
        """
        if count is None:
            count = 30

        params = {
            "page_count": count
        }
        data = self._get("athlete/activities", params=params)

        all_activities = []
        for idx, activity in enumerate(data):
            if idx >= count:
                break

            summary_activity = self._create_model(
                model=SummaryActivity,
                data=activity
            )
            all_activities.append(summary_activity)

        return all_activities
