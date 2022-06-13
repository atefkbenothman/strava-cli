from datetime import datetime, timedelta
from dataclasses import dataclass
from pydantic import BaseModel, validator
from typing import Optional


# https://developers.strava.com/docs/reference/#api-models-PolylineMap
@dataclass
class PolylineMap(BaseModel):
    """
    polyline map
    """
    id: int
    polyline: str
    summary_polyline: Optional[str] = None


# https://developers.strava.com/docs/reference/#api-models-ActivityTotal
@dataclass
class ActivityTotal(BaseModel):
    """
    a roll up of metrics pertaining to a set of activities
    """
    count: int
    distance: float
    elevation_gain: float
    moving_time: int
    elapsed_time: int
    achievement_count: Optional[int] = None

    @property
    def distance_in_miles(self) -> str:
        return f"{self.distance * 0.000621371192:,.2f}"

    @property
    def elevation_gain_in_feet(self) -> str:
        return f"{self.elevation_gain / 0.3048:,.2f}"

    @property
    def moving_time_in_hours(self) -> str:
        return timedelta(seconds=self.moving_time)

    @property
    def elapsed_time_in_hours(self) -> str:
        return timedelta(seconds=self.elapsed_time)


# https://developers.strava.com/docs/reference/#api-models-ActivityStats
@dataclass
class ActivityStats(BaseModel):
    """
    a set of rolled-up statistics and totals for an athlete
    """
    biggest_ride_distance: float
    biggest_climb_elevation_gain: float
    recent_ride_totals: ActivityTotal
    ytd_ride_totals: ActivityTotal
    all_ride_totals: ActivityTotal

    @property
    def biggest_ride_distance_in_miles(self) -> str:
        return f"{self.biggest_ride_distance * 0.000621371192:,.2f}"

    @property
    def biggest_climb_elevation_gain_in_feet(self) -> str:
        return f"{self.biggest_climb_elevation_gain / 0.3048:,.2f}"


# https://developers.strava.com/docs/reference/#api-models-DetailedSegment
@dataclass
class DetailedSegment(BaseModel):
    """
    detailed segment
    """
    id: int
    name: str
    activity_type: str
    distance: float
    average_grade: float
    maximum_grade: float
    elevation_high: float
    elevation_low: float
    climb_category: int
    city: str
    state: str
    country: str
    total_elevation_gain: float
    effort_count: int
    athlete_count: int
    hazardous: bool
    star_count: int


# https://developers.strava.com/docs/reference/#api-models-DetailedSegmentEffort
@dataclass
class DetailedSegmentEffort(BaseModel):
    """
    detailed segment effort model
    """
    id: int
    activity_id: int
    elapsed_time: int
    start_date: datetime
    distance: float
    name: str
    athlete: dict
    moving_time: int
    average_heartrate: float
    max_heartrate: float


# https://developers.strava.com/docs/reference/#api-models-DetailedAthlete
@dataclass
class DetailedAthlete(BaseModel):
    """
    detailed athlete model
    """
    id: int
    username: Optional[str] = None
    bio: Optional[str] = None
    resource_state: int
    firstname: str
    lastname: str
    profile: str
    city: str
    state: str
    country: str
    sex: str
    premium: bool
    summit: bool
    created_at: datetime
    updated_at: datetime
    follower_count: int
    friend_count: int
    measurement_preference: str
    ftp: int
    weight: float


# https://developers.strava.com/docs/reference/#api-models-SummaryActivity
@dataclass
class SummaryActivity(BaseModel):
    """
    summary activity model
    """
    id: int
    name: str
    athlete: dict
    distance: float
    moving_time: int
    elapsed_time: int
    total_elevation_gain: float
    elev_high: float
    elev_low: float
    type: dict
    start_date: datetime
    timezone: str
    average_speed: float
    max_speed: float
