import gdown
from slugify import slugify
import gspread
import os
import os.path
from pathlib import Path
from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import enum

# User imports
from settings import *

from modules.worksheet import get_worksheet, worksheet_update
from modules.run_command import run_command

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

# Read sheet
gc = gspread.service_account(filename=GSPREAD_SERVICE_ACCOUNT_FILE)
sh = gc.open_by_key("1omzU4IXQelzhtxHq-6eku_3_vxXH9j-TSzXv4sQodsM")
worksheet = sh.worksheet("cosmic_archives_nu")

all_records = worksheet.get_all_records()
current_record_num = 1

CHANNEL_CREDENTIALS_FILE = CREDENTIALS_FOLDER / (
    "channel_credentials_UCIxZyNQt5TfxmREDDH6PPlA.json"
)

while current_record_num < worksheet.row_count:
    current_video_metadata = all_records[current_record_num]
    resource_type = current_video_metadata["Type"]
    status = current_video_metadata["Status"]
    converted = current_video_metadata["Converted to mp4"]
    md5 = current_video_metadata["Md5"]
    mp4_name = current_video_metadata["mp4 name"]

    md5_row_index = 1
    md5_found = False

    if not "video" in resource_type or mp4_name != "":
        current_record_num = current_record_num + 1
        continue

    # We check with md5 if file has already been downloaded
    # while md5_row_index < current_record_num:
    #     md5_row_metadata = all_records[md5_row_index]
    #     if md5 == md5_row_metadata["Md5"]:
    #         worksheet_update(worksheet, "I" + str(current_record_num + 2), "")
    #         worksheet_update(worksheet, "J" + str(current_record_num + 2), "yes")
    #         worksheet_update(
    #             worksheet,
    #             "K" + str(current_record_num + 2),
    #             md5_row_metadata["mp4 name"],
    #         )
    #         current_record_num = current_record_num + 1
    #         md5_found = True
    #         break

    #     md5_row_index = md5_row_index + 1

    # if md5_found:
    #     continue

    filename = current_video_metadata["Name"].replace("| ", "").replace("+--", "")
    basename = Path(filename).stem
    file_extension = Path(filename).suffix
    gdrive_id = current_video_metadata["GDrive Id"]

    url = "https://drive.google.com/uc?id=" + gdrive_id
    output = LOCAL_VIDEOS_FOLDER_PATH / (slugify(basename) + "_output" + file_extension)
    print(output)

    gdown.download(url, str(output), quiet=False)

    if not os.path.exists(str(output)):
        print(str(output) + " does not exist")
        worksheet_update(worksheet, "J" + str(current_record_num + 2), "Download again")
        current_record_num = current_record_num + 1
        continue

    destination_file = slugify(basename) + ".256" + file_extension + ".mp4"
    destination = LOCAL_VIDEOS_FOLDER_PATH / destination_file

    command = (
        "ffmpeg "
        + "-i "
        + str(output)
        + " -c:v libx264 "
        + "-b:v 256k "
        + "-c:a aac "
        + str(destination)
    )

    return_code, output_lines = run_command(command.split(" "))

    file_size_in_bytes = os.path.getsize(str(destination))
    file_size_MB = file_size_in_bytes / (1024 * 1024)

    if file_size_MB < 1:
        os.remove(str(destination))

        destination_file2 = slugify(basename) + ".512" + file_extension + ".mp4"
        destination_file = destination_file2
        destination2 = LOCAL_VIDEOS_FOLDER_PATH / destination_file2

        command = (
            "ffmpeg "
            + "-i "
            + str(output)
            + " -c:v libx264 "
            + "-b:v 512k "
            + "-c:a aac "
            + str(destination2)
        )

        return_code, output_lines = run_command(command.split(" "))

        file_size_in_bytes = os.path.getsize(str(destination2))
        file_size_MB = file_size_in_bytes / (1024 * 1024)

        if file_size_MB < 1:
            os.remove(str(destination2))

            destination_file3 = slugify(basename) + ".1024" + file_extension + ".mp4"
            destination_file = destination_file3
            destination3 = LOCAL_VIDEOS_FOLDER_PATH / destination_file3

            command = (
                "ffmpeg "
                + "-i "
                + str(output)
                + " -c:v libx264 "
                + "-b:v 1024k "
                + "-c:a aac "
                + str(destination3)
            )

            return_code, output_lines = run_command(command.split(" "))

            file_size_in_bytes = os.path.getsize(str(destination3))
            file_size_MB = file_size_in_bytes / (1024 * 1024)

            if file_size_MB < 1:
                os.remove(str(destination3))

                destination_file4 = (
                    slugify(basename) + ".2048" + file_extension + ".mp4"
                )
                destination_file = destination_file4
                destination4 = LOCAL_VIDEOS_FOLDER_PATH / destination_file4

                command = (
                    "ffmpeg "
                    + "-i "
                    + str(output)
                    + " -c:v libx264 "
                    + "-b:v 2048k "
                    + "-c:a aac "
                    + str(destination4)
                )

                return_code, output_lines = run_command(command.split(" "))

                file_size_in_bytes = os.path.getsize(str(destination4))
                file_size_MB = file_size_in_bytes / (1024 * 1024)

                if file_size_MB < 1:
                    os.remove(str(destination4))

                    destination_file5 = (
                        slugify(basename) + ".5096" + file_extension + ".mp4"
                    )
                    destination_file = destination_file5
                    destination5 = LOCAL_VIDEOS_FOLDER_PATH / destination_file5

                    command = (
                        "ffmpeg "
                        + "-i "
                        + str(output)
                        + " -c:v libx264 "
                        + "-b:v 5096k "
                        + "-c:a aac "
                        + str(destination5)
                    )

                    return_code, output_lines = run_command(command.split(" "))

                    file_size_in_bytes = os.path.getsize(str(destination5))
                    file_size_MB = file_size_in_bytes / (1024 * 1024)

                    if file_size_MB < 1:
                        os.remove(str(destination5))

                        destination_file6 = (
                            slugify(basename) + ".10192" + file_extension + ".mp4"
                        )
                        destination_file = destination_file6
                        destination6 = LOCAL_VIDEOS_FOLDER_PATH / destination_file6

                        command = (
                            "ffmpeg "
                            + "-i "
                            + str(output)
                            + " -c:v libx264 "
                            + "-b:v 10192k "
                            + "-c:a aac "
                            + str(destination6)
                        )

                        return_code, output_lines = run_command(command.split(" "))

    # worksheet_update(worksheet, "J" + str(current_record_num + 2), "")
    worksheet_update(worksheet, "L" + str(current_record_num + 2), "yes")
    worksheet_update(worksheet, "F" + str(current_record_num + 2), destination_file)
    os.remove(output)

    current_record_num = current_record_num + 1
