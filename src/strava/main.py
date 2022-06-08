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

  c: int = int(input("count: "))

  # api
  api = API(access_token=auth.access_token)
  activities = api.get_activities(count=c)

  # printer
  printer = Printer(activities=activities)
  printer.print_summary_with_total(count=c)

  return


if __name__ == "__main__":
  main()
