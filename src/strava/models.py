import datetime
from dataclasses import dataclass


@dataclass
class PolylineMap:
    """
    polyline map
    """
    id: int = 0
    polyline: str = ""
    summary_polyline: str = ""


# https://developers.strava.com/docs/reference/#api-models-ActivityTotal
@dataclass
class ActivityTotal:
    """
    a roll up of metrics pertaining to a set of activities
    """
    count: int = 0
    distance: float = 0.0
    moving_time: int = 0
    elapsed_time: int = 0
    elevation_gain: float = 0.0
    achievement_count: int = 0


# https://developers.strava.com/docs/reference/#api-models-ActivityStats
@dataclass
class ActivityStats:
    """
    a set of rolled-up statistics and totals for an athlete
    """
    biggest_ride_distance: float = 0.0
    biggest_climb_elevation_gain: float = 0.0
    recent_ride_totals: ActivityTotal = None
    ytd_ride_totals: ActivityTotal = None
    all_ride_totals: ActivityTotal = None


@dataclass
class DetailedSegment:
    """
    detailed segment
    """
    segment_id: int = 0
    name: str = ""
    activity_type: str = ""
    distance: float = 0.0
    average_grade: float = 0.0
    maximum_grade: float = 0.0
    elevation_high: float = 0.0
    elevation_low: float = 0.0
    climb_category: int = -1
    city: str = ""
    state: str = ""
    country: str = ""
    total_elevation_gain: float = 0.0
    effort_count: int = 0
    athlete_count: int = 0
    hazardous: bool = False
    star_count: int = 0
    segment_map: str = ""


# https://developers.strava.com/docs/reference/#api-models-DetailedSegmentEffort
@dataclass
class DetailedSegmentEffort:
    """
    detailed segment effort model
    """
    id: int = 0
    activity_id: int = 0
    elapsed_time: int = 0
    start_date: datetime.datetime = datetime.datetime.now()
    distance: float = 0.0
    name: str = ""
    athlete: id = 0
    moving_time: int = 0
    average_heartrate: float = 0.0
    max_heartrate: float = 0.0


# https://developers.strava.com/docs/reference/#api-models-DetailedAthlete
@dataclass
class DetailedAthlete:
    """
    detailed activity model
    """
    id: int = 0
    firstname: str = ""
    lastname: str = ""
    profile: str = ""
    city: str = ""
    state: str = ""
    country: str = ""
    sex: str = ""


# https://developers.strava.com/docs/reference/#api-models-SummaryActivity
@dataclass
class SummaryActivity:
    """
    summary activity model
    """
    id: int = 0
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
           "id",
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
            self.id,
            self.name,
            f"{self.convert_meters_to_miles(self.distance):.2f}",
            self.convert_seconds_to_hours(self.moving_time),
            self.convert_seconds_to_hours(self.elapsed_time),
            f"{self.convert_meters_to_feet(self.total_elevation_gain):.2f}",
            f"{self.convert_meters_per_second_to_mph(self.avg_speed):.2f}",
            f"{self.convert_meters_per_second_to_mph(self.max_speed):.2f}",
        ]

    def get_totals_row_data(self, activity_list: list) -> list:
        """
        calculate the total for the given activities
        """
        total_distance: float = 0.0
        total_moving_time: int = 0.0
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
            id="-",
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
        total_moving_time: int = 0.0
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
            id="-",
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
            id="-",
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

    def convert_meters_per_second_to_mph(self, mps: float):
        """
        convert meters/sec to miles/hour
        """
        return mps * 2.2369
