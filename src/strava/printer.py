from dataclasses import dataclass, fields, field
from prettytable import PrettyTable
from typing import Optional
from strava.models import (
    SummaryActivity,
    DetailedAthlete,
    ActivityStats,
    ActivityTotal,
    DetailedSegment,
)


@dataclass
class Printer:
    """
    handles printing tables
    """
    printer: PrettyTable = PrettyTable(
        padding_width=1
    )

    def _print(self, model, field_names: Optional[list] = None, title: Optional[str] = None) -> None:
        """
        print the api model in a table format
        """
        # clear all data from table
        self.printer.clear()

        # if field names weren't specified, use all
        if field_names is None:
            field_names = model.dict().keys()

        # if title isn't specified, use model name instead
        if title is None:
            title = type(model).__name__

        row = []
        for field_name in field_names:
            data = eval(f"model.{field_name}")
            row.append(data)

        # set printer fields
        self.printer._title = title
        self.printer.field_names = field_names
        self.printer.add_row(row)

        # print
        print()
        print(self.printer)
        print()
        return

    def print_athlete(self, athlete: DetailedAthlete) -> None:
        """
        print athlete data
        """
        fields_to_print = [
            "id",
            "firstname",
            "lastname",
            "city",
            "state",
            "country",
            "sex",
            "premium",
            "created_at",
            "updated_at",
        ]
        self._print(athlete, field_names=fields_to_print, title="athlete")
        return

    def print_totals(self, activity_total: ActivityTotal, key: Optional[str] = None) -> None:
        """
        print activity total model
        key specifies what range of totals we are printing
        """
        fields_to_print = [
            "count",
            "distance_in_miles",
            "elevation_gain_in_feet",
            "moving_time_in_hours",
            "elapsed_time_in_hours",
            "achievement_count"
        ]
        self._print(activity_total, field_names=fields_to_print, title=key)
        return

    def print_athlete_stats(self, stats: ActivityStats) -> None:
        """
        print athlete stats data
        split each model into its own table
        """
        recent_ride_totals: ActivityTotal = stats.recent_ride_totals
        self.print_totals(recent_ride_totals, key="recent_ride_totals")

        ytd_ride_totals: ActivityTotal = stats.ytd_ride_totals
        self.print_totals(ytd_ride_totals, key="ytd_ride_totals")

        all_ride_totals: ActivityTotal = stats.all_ride_totals
        self.print_totals(all_ride_totals, key="all_ride_totals")

        data = {
            "biggest_ride_distance_in_miles",
            "biggest_climb_elevation_gain_in_feet"
        }
        self._print(stats, field_names=data, title="totals")
        return
