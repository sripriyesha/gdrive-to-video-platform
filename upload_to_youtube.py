# Standard library imports
from __future__ import unicode_literals
import argparse
from ftplib import FTP_TLS
import questionary
import os
from os import remove, path
from pathlib import Path
import subprocess
from subprocess import CalledProcessError
import sys
import time
import urllib.request
from urllib.parse import urlparse
from urllib.error import HTTPError
import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

# Third party imports
from googleapiclient.errors import ResumableUploadError
import gspread
import requests

# User imports
from settings import *

from modules.worksheet import worksheet_update
from modules.youtube import (
    upload_to_youtube,
)


# FLOW

# 1. do we have videos in folder? V2
# 2. connect to Google Sheets
# 3. get youtube links of videos already uploaded
# 4. Are all links downloaded?
# 5. No. Download all cells values
# STEP_GET_VIDEO_DATA
# 6. get the next row of the video to download
# 7. extract the metadata from the all cells values data structure for this row
# 8. download the video locally
#
# 9. upload the video with the metadata
# 10. wait for completion of upload
# 11. Write target youtube channel link, status in Google Sheet in corresponding row
# GO BACK TO STEP_GET_VIDEO_DATA

DESTINATION_CHANNELS_NAMES = DESTINATION_CHANNELS_CONFIG.keys()

parser = argparse.ArgumentParser()
parser.add_argument(
    "-d",
    "--dest",
    dest="destination_channel",
    help="Choose a destination channel",
    choices=DESTINATION_CHANNELS_NAMES,
)
parser.add_argument(
    "-n",
    dest="max_video_uploads",
    help="Stops upload process after processing the number of videos specified",
)

args = parser.parse_args()
if not args.destination_channel:
    args.destination_channel = questionary.select(
        "On which channel do you want to upload the videos",
        choices=DESTINATION_CHANNELS_NAMES,
    ).ask()

if not args.destination_channel:
    sys.exit()

DESTINATION_CHANNEL_CONFIG = DESTINATION_CHANNELS_CONFIG[args.destination_channel]
YOUTUBE_CHANNEL_ID = DESTINATION_CHANNEL_CONFIG["id"]
CHANNEL_CREDENTIALS_FILE = CREDENTIALS_FOLDER / (
    "channel_credentials_" + YOUTUBE_CHANNEL_ID + ".json"
)

print(
    "--- Upload videos to " + args.destination_channel.title() + " YouTube channel ---"
)

print("Connecting to Google sheets")
gc = gspread.service_account(filename=GSPREAD_SERVICE_ACCOUNT_FILE)
sh = gc.open_by_key("1omzU4IXQelzhtxHq-6eku_3_vxXH9j-TSzXv4sQodsM")
worksheet = sh.worksheet("cosmic_archives_nu")

print("Getting row start number: ", end="")
current_row_num = 1
# current_row_num = worksheet.row_count
print(str(current_row_num))

all_records = worksheet.get_all_records()

i = 0
is_api_upload_limit_exceeded = False

while current_row_num < worksheet.row_count:
    if args.max_video_uploads and i == args.max_video_uploads:
        sys.exit()

    current_video_metadata = all_records[current_row_num]
    mp4_file = current_video_metadata["mp4 name"]

    if mp4_file == "":
        current_row_num = current_row_num + 1
        continue

    if current_video_metadata["Status"] == "uploaded":
        current_row_num = current_row_num + 1
        continue

    print()
    print("---------")
    print("Row number " + str(current_row_num))
    print("-")
    print(mp4_file)
    print("-")

    print()
    print("Uploading " + mp4_file + " to YouTube")

    try:
        youtube_video = upload_to_youtube(
            CHANNEL_CREDENTIALS_FILE, current_video_metadata
        )

        print("[SUCCESS]")
        youtube_link = "https://youtu.be/" + youtube_video.id
        print("Link to the uploaded video: " + youtube_link)

        worksheet_update(worksheet, "I" + str(current_row_num + 2), youtube_link)
        worksheet_update(worksheet, "J" + str(current_row_num + 2), "uploaded")

        os.remove(LOCAL_VIDEOS_FOLDER_PATH / mp4_file)
        print("[DONE]")
    except ResumableUploadError as e:
        print(str(e))

        # https://developers.google.com/youtube/v3/docs/errors#youtube.videos.insert-badRequest-uploadLimitExceeded
        if UPLOAD_LIMIT_EXCEEDED_ERROR in str(e):
            break

    except Exception as e:
        # print(e)
        print(str(e))

    current_row_num = current_row_num + 1
    i += 1
