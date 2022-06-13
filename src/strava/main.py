from strava.auth import Auth
from strava.api import API
from strava.printer import Printer


def main():
  """
  start
  """
  # auth
  auth = Auth()
  auth.set_creds("./.creds.json")
  auth.authorize()

  # api
  api = API(access_token=auth.access_token)
  athlete = api.get_athlete()
  stats = api.get_athlete_stats(athlete.id)
  activities = api.get_athlete_activities(30)

  # printer
  printer = Printer()
  printer.print_athlete(athlete)
  # printer.print_athlete_stats(stats)
  printer.print_athlete_activities(activities)

  return


if __name__ == "__main__":
  main()
