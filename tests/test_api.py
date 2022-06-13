from strava.api import API

TEST_BASE_URL = "https://test.com"
TEST_API_ENDPOINT = "athelete/activities"


def test_can_generate_url():
  """
  Test that the api class can generate the correct url.
  """
  api = API()
  generated_url = api._generate_url(TEST_API_ENDPOINT)
  print(f"{generated_url=}")
  assert "https://www.strava.com/api/v3/athelete/activities" == generated_url


def test_can_generate_url_custom_base_url():
  """
  Test that the api class can generate the correct url
  using a custom base url.
  """
  api = API(base_url=TEST_BASE_URL)
  generated_url = api._generate_url(TEST_API_ENDPOINT)
  print(f"{generated_url=}")
  assert "https://test.com/athelete/activities" == generated_url
