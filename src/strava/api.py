import requests
from urllib.parse import urljoin
from dataclasses import dataclass

from strava.models import (
    DetailedAthlete,
    SummaryActivity,
    # DetailedSegmentEffort,
    DetailedSegment,
    ActivityTotal,
    ActivityStats,
    PolylineMap
)


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

    def get_athlete(self) -> DetailedAthlete:
        """
        get the current authenticated athlete.
        """
        url = self.generate_url("athlete")
        status_code, data = self.get(url)

        if status_code != 200:
            print(f"{status_code=}, {data=}")
            return

        athlete = DetailedAthlete(
            id=data["id"],
            firstname=data["firstname"],
            lastname=data["lastname"],
            profile=data["profile"],
            city=data["city"],
            state=data["state"],
            country=data["country"],
            sex=data["sex"]
        )

        return athlete

    def get_athlete_stats(self) -> ActivityStats():
        """
        get the activity stats of an athlete
        """
        athlete: DetailedAthlete = self.get_athlete()

        url = self.generate_url(f"athletes/{athlete.id}/stats")
        status_code, data = self.get(url)

        print(url)

        if status_code != 200:
            print(f"{status_code=}, {data=}")
            return

        print(data)

        recent_ride_totals = ActivityTotal(
            count=data["recent_ride_totals"]["count"],
            distance=data["recent_ride_totals"]["distance"],
            moving_time=data["recent_ride_totals"]["moving_time"],
            elapsed_time=data["recent_ride_totals"]["elapsed_time"],
            elevation_gain=data["recent_ride_totals"]["elevation_gain"],
            achievement_count=data["recent_ride_totals"]["achievement_count"],
        )

        ytd_ride_totals = ActivityTotal(
            count=data["ytd_ride_totals"]["count"],
            distance=data["ytd_ride_totals"]["distance"],
            moving_time=data["ytd_ride_totals"]["moving_time"],
            elapsed_time=data["ytd_ride_totals"]["elapsed_time"],
            elevation_gain=data["ytd_ride_totals"]["elevation_gain"],
            # achievement_count=data["ytd_ride_totals"]["achievement_count"],
        )

        all_ride_totals = ActivityTotal(
            count=data["all_ride_totals"]["count"],
            distance=data["all_ride_totals"]["distance"],
            moving_time=data["all_ride_totals"]["moving_time"],
            elapsed_time=data["all_ride_totals"]["elapsed_time"],
            elevation_gain=data["all_ride_totals"]["elevation_gain"],
            # achievement_count=data["all_ride_totals"]["achievement_count"],
        )

        stats = ActivityStats(
            biggest_ride_distance=data["biggest_ride_distance"],
            biggest_climb_elevation_gain=data["biggest_climb_elevation_gain"],
            recent_ride_totals=recent_ride_totals,
            ytd_ride_totals=ytd_ride_totals,
            all_ride_totals=all_ride_totals
        )

        return stats

    def get_segment(self, id) -> DetailedSegment:
        """
        return the specified segment
        """
        url = self.generate_url(f"segments/{id}")
        status_code, data = self.get(url)

        if status_code != 200:
            print(f"{status_code=}, {data=}")
            return

        segment_map = PolylineMap(
            id=data["map"]["id"],
            polyline=data["map"]["polyline"],
            # summary_polyline=data["map"]["summary_polyline"],
        )

        segment = DetailedSegment(
            segment_id=data["id"],
            name=data["name"],
            activity_type=data["activity_type"],
            distance=data["distance"],
            average_grade=data["average_grade"],
            maximum_grade=data["maximum_grade"],
            elevation_high=data["elevation_high"],
            elevation_low=data["elevation_low"],
            climb_category=data["climb_category"],
            city=data["city"],
            state=data["state"],
            country=data["country"],
            total_elevation_gain=data["total_elevation_gain"],
            effort_count=data["effort_count"],
            athlete_count=data["athlete_count"],
            hazardous=data["hazardous"],
            star_count=data["star_count"],
            segment_map=segment_map
        )

        return segment

    def get_segment_efforts(self) -> list:
        """
        get the set of the athletes segment efforts for a given segment
        """
        url = self.generate_url("athlete")
        status_code, data = self.get(url)

        if status_code != 200:
            print(f"{status_code=}, {data=}")
            return

        print(data)

        return

    def get_activities(self, count: int = 0) -> list:
        """
        TODO: refactor entire function...
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
