import json
from urllib.parse import urljoin
from dataclasses import dataclass

@dataclass
class API:
    """
    custom api class
    """
    base_url: str = "https://www.strava.com/api/v3/"
    access_token: str = ""

    def set_token(self, file_name: str) -> str:
        """
        get strava access token from config.json
        """
        with open(file_name) as f:
            creds = json.load(f)

        client_id = creds["client_id"]
        client_secret = creds["client_secret"]
        access_token = creds["access_token"]

        self.access_token = access_token

        return access_token

    def generate_url(self, endpoint: str):
        """
        generate the api url endpoint
        """
        return urljoin(self.base_url, endpoint)

    def get(self, url: str):
        """
        handle get requests
        """
        return

    def get_all_activities(self):
        """
        get all athlete activities
        """
        url = self.generate_url("athlete/activities")
        self.get(url)
        return


def main():
    api = API()
    api.set_token("./.config.json")
    api.get_all_activities()

    return

if __name__ == "__main__":
    main()
