import json
import requests
import webbrowser

from dataclasses import dataclass

from requests_oauthlib import OAuth2Session

from urllib.parse import urlparse
from urllib.parse import parse_qs


@dataclass
class Auth:
  """
  custom auth handler for strava which uses oauth2
  """
  authorize_base_url: str = "https://www.strava.com/oauth/authorize"
  token_base_url: str = "https://www.strava.com/oauth/token"

  access_token: str = ""
  client_id: str = ""
  client_secret: str = ""

  redirect_uri: str = "http://localhost"
  scope: str = "read_all,profile:read_all,activity:read_all"

  def set_creds(self, file_name: str):
      """
      get strava access token from creds.json
      """
      with open(file_name) as f:
          creds = json.load(f)

      self.client_id = creds["client_id"]
      self.client_secret = creds["client_secret"]
      return

  def get_token_code(self, url: str) -> str:
      """
      parse the url for the token code
      """
      parsed_url = urlparse(url)
      code = parse_qs(parsed_url.query)["code"][0]
      return code

  def token_exchange(self, code: str):
      """
      get token
      """
      data = {
          "client_id": self.client_id,
          "client_secret": self.client_secret,
          "code": code,
          "grant_type": "authorization_code"
      }
      response = requests.post(self.token_base_url, data=data)

      # set access token
      if "access_token" not in response.json():
          print("error setting access token!")
          return

      access_token = response.json()["access_token"]
      self.access_token = access_token
      print(f"{access_token=}")
      return

  def authorize(self):
      """
      authorize
      """
      print("authorizing...")

      # first, ask if user already has an access token
      has_token = input("do you already have an access token? [y/N]: ")
      if has_token == "y":
          token = input("token: ")
          self.access_token = token
          return

      # generate auth url
      strava = OAuth2Session(
          self.client_id,
          scope=self.scope,
          redirect_uri=self.redirect_uri
        )
      auth_url, state = strava.authorization_url(self.authorize_base_url)

      # open url in browser
      webbrowser.open(auth_url, new=1, autoraise=True)

      # authorize + parse url
      auth_url = input("paste authorization url: ")
      code = self.get_token_code(auth_url)

      # get access token
      self.token_exchange(code)
      return
