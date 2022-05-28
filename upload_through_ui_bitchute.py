# Standard library imports
from __future__ import unicode_literals
from os import remove, path
import os

# Third party imports
import gspread

# User imports
from settings import *
from modules.run_command import run_command
from modules.worksheet import worksheet_update

print("--- Upload videos to News Videos 1 Bitchute channel ---")

print("Connecting to Google sheets")
gc = gspread.service_account(filename=GSPREAD_SERVICE_ACCOUNT_FILE)
sh = gc.open_by_key("1omzU4IXQelzhtxHq-6eku_3_vxXH9j-TSzXv4sQodsM")
worksheet = sh.worksheet("cosmic_archives_nu")

current_row_num = 1
all_records = worksheet.get_all_records()

while current_row_num < worksheet.row_count:
    current_video_metadata = all_records[current_row_num]
    mp4_name = current_video_metadata["mp4 name"]

    if not mp4_name:
        current_row_num = current_row_num + 1
        continue

    if (
        current_video_metadata["Status"] == "uploaded"
        or current_video_metadata["Status"] == "wrong file"
        or current_video_metadata["Status"] == "filesize too small"
    ):
        current_row_num = current_row_num + 1
        continue

    print()
    print("---------")
    print("Row number " + str(current_row_num + 2))
    print("-")
    print(mp4_name)
    print("-")

    if not path.isfile(str(LOCAL_VIDEOS_FOLDER_PATH / mp4_name)):
        current_row_num = current_row_num + 1
        continue

    print()
    print("Uploading " + mp4_name + " to Bitchute")

    command = (
        "node upload-through-ui-bitchute.js "
        + " --cookies-file ./www.bitchute.com.cookies.json "
        + "--video-file "
        + str(LOCAL_VIDEOS_FOLDER_PATH / mp4_name)
    )

    return_code, output_lines = run_command(command.split(" "))
    video_link = output_lines[len(output_lines) - 1]

    worksheet_update(worksheet, "J" + str(current_row_num + 2), video_link)
    worksheet_update(worksheet, "K" + str(current_row_num + 2), "uploaded")

    # os.remove(str(LOCAL_VIDEOS_FOLDER_PATH / mp4_name))

    current_row_num = current_row_num + 1
