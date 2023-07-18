import json
import time
from datetime import datetime
from config import SYNCED_FILE_NAME

import pytz
import os

try:
    from rich import print
except:
    pass
from generator import Generator
from stravalib.client import Client
from stravalib.exc import RateLimitExceeded


def adjust_time(time, tz_name):
    tc_offset = datetime.now(pytz.timezone(tz_name)).utcoffset()
    return time + tc_offset


def adjust_time_to_utc(time, tz_name):
    tc_offset = datetime.now(pytz.timezone(tz_name)).utcoffset()
    return time - tc_offset


def adjust_timestamp_to_utc(timestamp, tz_name):
    tc_offset = datetime.now(pytz.timezone(tz_name)).utcoffset()
    delta = int(tc_offset.total_seconds())
    return int(timestamp) - delta


def to_date(ts):
    # TODO use https://docs.python.org/3/library/datetime.html#datetime.datetime.fromisoformat
    # once we decide to move on to python v3.7+
    ts_fmts = ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f"]

    for ts_fmt in ts_fmts:
        try:
            # performance with using exceptions
            # shouldn't be an issue since it's an offline cmdline tool
            return datetime.strptime(ts, ts_fmt)
        except ValueError:
            print("Error: Can not execute strptime")
            pass

    raise ValueError(f"cannot parse timestamp {ts} into date with fmts: {ts_fmts}")


def make_activities_file(sql_file, data_dir, json_file, file_suffix="gpx"):
    generator = Generator(sql_file)
    generator.sync_from_data_dir(data_dir, file_suffix=file_suffix)
    activities_list = generator.load()
    with open(json_file, "w") as f:
        json.dump(activities_list, f, indent=0)


def make_activities_file_only(sql_file, data_dir, json_file, file_suffix="gpx"):
    generator = Generator(sql_file)
    generator.sync_from_data_dir(data_dir, file_suffix=file_suffix)
    activities_list = generator.loadForMapping()
    with open(json_file, "w") as f:
        json.dump(activities_list, f, indent=0)


def make_strava_client(client_id, client_secret, refresh_token):
    client = Client()

    refresh_response = client.refresh_access_token(
        client_id=client_id, client_secret=client_secret, refresh_token=refresh_token
    )
    client.access_token = refresh_response["access_token"]
    return client


def get_strava_last_time(client, is_milliseconds=True):
    """
    if there is no activities cause exception return 0
    """
    try:
        activity = None
        activities = client.get_activities(limit=10)
        activities = list(activities)
        activities.sort(key=lambda x: x.start_date, reverse=True)
        # for else in python if you don't know please google it.
        for a in activities:
            if a.type == "Run":
                activity = a
                break
        else:
            return 0
        end_date = activity.start_date + activity.elapsed_time
        last_time = int(datetime.timestamp(end_date))
        if is_milliseconds:
            last_time = last_time * 1000
        return last_time
    except Exception as e:
        print(f"Something wrong to get last time err: {str(e)}")
        return 0


def upload_file_to_strava(client, file_name, data_type):
    with open(file_name, "rb") as f:
        try:
            r = client.upload_activity(activity_file=f, data_type=data_type)
        except RateLimitExceeded as e:
            timeout = e.timeout
            print()
            print(f"Strava API Rate Limit Exceeded. Retry after {timeout} seconds")
            print()
            time.sleep(timeout)
            r = client.upload_activity(activity_file=f, data_type=data_type)
        print(
            f"Uploading {data_type} file: {file_name} to strava, upload_id: {r.upload_id}."
        )


def save_synced_data_file_list(data_dir: str, file_list: list):
    data_dir = os.path.abspath(data_dir)
    synced_json_file = os.path.join(data_dir, SYNCED_FILE_NAME)

    old_list = []
    if os.path.exists(synced_json_file):
        with open(synced_json_file, "r") as f:
            try:
                old_list = json.load(f)
            except Exception as e:
                print(f"json load {synced_json_file} \nerror {e}")
                pass

    with open(synced_json_file, "w") as f:
        file_list.extend(old_list)

        json.dump(file_list, f)


def load_synced_file_list(data_dir: str):
    data_dir = os.path.abspath(data_dir)
    synced_json_file = os.path.join(data_dir, SYNCED_FILE_NAME)

    if os.path.exists(synced_json_file):
        with open(synced_json_file, "r") as f:
            try:
                return json.load(f)
            except Exception as e:
                print(f"json load {synced_json_file} \nerror {e}")
                pass

    return []
