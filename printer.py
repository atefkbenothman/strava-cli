from .models import SummaryActivity

from dataclasses import dataclass, field
from prettytable import PrettyTable

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