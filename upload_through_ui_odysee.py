# Standard library imports
from __future__ import unicode_literals
from os import remove, path

# Third party imports
import gspread

# User imports
from settings import *
from modules.run_command import run_command

print("--- Upload videos to News Videos 1 Odysee channel ---")

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

    print()
    print("---------")
    print("Row number " + str(current_row_num))
    print("-")
    print(mp4_name)
    print("-")

    if not path.isfile(str(LOCAL_VIDEOS_FOLDER_PATH / mp4_name)):
        current_row_num = current_row_num + 1
        continue

    print()
    print("Uploading " + mp4_name + " to Odysee")

    command = (
        "node upload-through-ui.js "
        + " --cookies-file ./odysee.com.cookies.json "
        + "--video-file "
        + str(LOCAL_VIDEOS_FOLDER_PATH / mp4_name)
    )

    return_code, output_lines = run_command(command.split(" "))

    current_row_num = current_row_num + 1
    exit()
