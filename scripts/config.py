import os
from collections import namedtuple
import yaml
from pathlib import Path

# getting content root directory
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)

CI_DATA_FOLDER = Path.home().joinpath("running_page_data")

OUTPUT_DIR = os.path.join(parent, "activities") if not os.getenv("CI") else CI_DATA_FOLDER.joinpath( "activities").__str__()
GPX_FOLDER = os.path.join(parent, "GPX_OUT") if not os.getenv("CI") else CI_DATA_FOLDER.joinpath( "GPX_OUT").__str__()
TCX_FOLDER = os.path.join(parent, "TCX_OUT") if not os.getenv("CI") else CI_DATA_FOLDER.joinpath( "TCX_OUT").__str__()
FIT_FOLDER = os.path.join(parent, "FIT_OUT") if not os.getenv("CI") else CI_DATA_FOLDER.joinpath( "FIT_OUT").__str__()
ENDOMONDO_FILE_DIR = os.path.join(parent, "Workouts") if not os.getenv("CI") else CI_DATA_FOLDER.joinpath( "Workouts").__str__()
FOLDER_DICT = {
    "gpx": GPX_FOLDER,
    "tcx": TCX_FOLDER,
    "fit": FIT_FOLDER,
}
SQL_FILE = os.path.join(parent, "scripts", "data.db") if not os.getenv("CI") else CI_DATA_FOLDER.joinpath( "data.db").__str__()
JSON_FILE = os.path.join(parent, "src", "static", "activities.json") if not os.getenv("CI") else CI_DATA_FOLDER.joinpath( "activities.json").__str__()
SYNCED_FILE_NAME = "imported.json"

# TODO: Move into nike_sync
BASE_URL = "https://api.nike.com/sport/v3/me"
TOKEN_REFRESH_URL = "https://unite.nike.com/tokenRefresh"
NIKE_CLIENT_ID = "HlHa2Cje3ctlaOqnxvgZXNaAs7T9nAuH"
BASE_TIMEZONE = "Asia/Shanghai"


start_point = namedtuple("start_point", "lat lon")
run_map = namedtuple("polyline", "summary_polyline")

try:
    with open("config.yaml") as f:
        _config = yaml.safe_load(f)
except:
    _config = {}


def config(*keys):
    def safeget(dct, *keys):
        for key in keys:
            try:
                dct = dct[key]
            except KeyError:
                return None
        return dct

    return safeget(_config, *keys)


# add more type here
TYPE_DICT = {
    "running": "Run",
    "RUN": "Run",
    "Run": "Run",
    "cycling": "Ride",
    "CYCLING": "Ride",
    "Ride": "Ride",
    "VirtualRide": "VirtualRide",
    "indoor_cycling": "Indoor Ride",
    "walking": "Hike",
    "hiking": "Hike",
    "Walk": "Hike",
    "Hike": "Hike",
    "Swim": "Swim",
    "rowing": "Rowing",
    "RoadTrip": "RoadTrip",
    "flight": "Flight",
    "kayaking": "Kayaking",
    "Snowboard": "Snowboard",
}

MAPPING_TYPE = [
    "Hike",
    "Ride",
    "VirtualRide",
    "Rowing",
    "Run",
    "Swim",
    "RoadTrip",
    "Kayaking",
    "Snowboard",
]

STRAVA_GARMIN_TYPE_DICT = {
    "Hike": "hiking",
    "Run": "running",
    "EBikeRide": "cycling",
    "VirtualRide": "VirtualRide",
    "Walk": "walking",
    "Swim": "swimming",
}
