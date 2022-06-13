from dataclasses import dataclass, fields, field
from prettytable import PrettyTable

from strava.models import (
    SummaryActivity,
    DetailedAthlete,
    ActivityStats,
    DetailedSegment,
    # ActivityTotal
)


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
        for c, activity in enumerate(self.activities):
            if c >= count:
                break
            activities.append(activity)
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

    def print_athlete(self, athlete: DetailedAthlete) -> None:
        """
        print athlete table
        """
        self.printer.field_names = [field.name for field in fields(athlete)]
        row = [
            athlete.id,
            athlete.firstname,
            athlete.lastname,
            athlete.profile,
            athlete.city,
            athlete.state,
            athlete.country,
            athlete.sex
        ]
        self.printer.add_row(row)
        print(self.printer)
        return

    def print_detailed_segment(self, segment: DetailedSegment) -> None:
        """
        print detailed segment
        """
        self.printer.field_names = [field.name for field in fields(segment)]
        row = [
            segment.segment_id,
            segment.name,
            segment.activity_type,
            segment.distance,
            segment.average_grade,
            segment.maximum_grade,
            segment.elevation_high,
            segment.elevation_low,
            segment.climb_category,
            segment.city,
            segment.state,
            segment.country,
            segment.total_elevation_gain,
            segment.effort_count,
            segment.athlete_count,
            segment.hazardous,
            segment.star_count,
            segment.segment_map,
        ]
        self.printer.add_row(row)
        print(self.printer)
        return

    def print_athlete_stats(self, activity_stats: ActivityStats):
        """
        print athlete stats
        """
        self.printer.field_names = [field.name for field in fields(activity_stats)]
        row = [
            activity_stats.biggest_ride_distance,
            activity_stats.biggest_climb_elevation_gain,
            activity_stats.recent_ride_totals,
            activity_stats.ytd_ride_totals,
            activity_stats.all_ride_totals
        ]
        self.printer.add_row(row)
        print(self.printer)
        return

    def print_summary(self):
        """
        print summary table
        """
        if self.activities is None:
            print("no activities...")
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
            print("no activities...")
            return

        self.printer.field_names = self.get_columns()

        # set the alignment to the right
        self.printer.align = "r"

        # add total row
        acts = self.get_activities(count=count)
        rows = self.get_rows(self.get_avg_row(acts))

        self.printer.add_rows(rows)

        print(self.printer)
        return
