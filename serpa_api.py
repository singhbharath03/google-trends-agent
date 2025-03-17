import json

from config import get_settings
from serpapi import GoogleSearch


SERP_API_KEY = get_settings().serp_api_key


def get_google_trends_data(keyword: str):
    if not SERP_API_KEY:
        return get_sample_google_trends_data()

    params = {
        "engine": "google_trends",
        "q": keyword,
        "date": "now 7-d",
        "api_key": SERP_API_KEY,
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    _reduce_data_size(results)

    return results


def get_sample_google_trends_data():
    with open("google_trends_data.json", "r") as f:
        data = json.load(f)

    _reduce_data_size(data)

    return data


def _reduce_data_size(data: dict):
    data["interest_over_time"]["timeline_data"] = data["interest_over_time"][
        "timeline_data"
    ][-20:]
