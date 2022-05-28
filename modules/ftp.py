# Standard library imports
from ftplib import FTP_TLS
import os

from tqdm import tqdm

# User imports
from settings import *


def ftp_connect():
    ftp = FTP_TLS(FTP_HOST)
    ftp.auth()
    # Set up secure data connection
    ftp.prot_p()
    ftp.login(FTP_LOGIN, FTP_PASSWORD)
    return ftp


def save_video_file_to_ftp(ftp, video_file_name_with_extension):
    file = open(LOCAL_VIDEOS_FOLDER_PATH / video_file_name_with_extension, "rb")
    ftp.cwd("videos")

    total_size = os.path.getsize(
        LOCAL_VIDEOS_FOLDER_PATH / video_file_name_with_extension
    )
    with tqdm(
        unit="blocks",
        unit_scale=True,
        leave=False,
        miniters=1,
        total=total_size,
    ) as tqdm_instance:
        ftp.storbinary(
            "STOR " + video_file_name_with_extension,
            file,
            2048,
            callback=lambda sent: tqdm_instance.update(len(sent)),
        )

    file.close()


def upload_video_to_ftp(video_file_name_with_extension):
    ftp = ftp_connect()
    ftp.encoding = "UTF-8"
    save_video_file_to_ftp(ftp, video_file_name_with_extension)
    ftp.quit()