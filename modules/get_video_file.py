# Standard library imports
from os import remove, path
import sys
import urllib.request

# Third party imports
import requests
from slugify import slugify

# User imports
from settings import *

from modules.ftp import upload_video_to_ftp
from modules.youtube import download_video_from_youtube


def uri_exists_stream(uri: str) -> bool:
    try:
        with requests.get(uri, stream=True) as response:
            try:
                response.raise_for_status()
                return True
            except requests.exceptions.HTTPError:
                return False
    except requests.exceptions.ConnectionError:
        return False
    except requests.exceptions.MissingSchema:
        return False


def get_video_file(title, source_channel_yt_link):
    video_title_slug = slugify(title)
    video_filename_with_extension = video_title_slug + ".mp4"

    video_path_on_ftp = (
        FTP_PUBLIC_VIDEOS_FOLDER_URL_PATH + video_filename_with_extension
    )
    video_path_in_local_folder = (
        LOCAL_VIDEOS_FOLDER_PATH / video_filename_with_extension
    )

    is_video_on_ftp = uri_exists_stream(video_path_on_ftp)
    is_video_in_local_folder = path.exists(video_path_in_local_folder)

    # if not is_video_in_local_folder:
    #     print("Video not in local folder")

    # if not is_video_on_ftp:
    # print("Video not on FTP server")
    try:
        print("Downloading video from YouTube...")
        download_video_from_youtube(source_channel_yt_link, video_title_slug)
        print("[DONE]")
    except Exception as e:
        raise

    # print("Uploading video to FTP server")
    # upload_video_to_ftp(video_filename_with_extension)
    # print("[DONE]")
    # else:
    #     print("Downloading video from FTP server", end=" ")
    #     sys.stdout.flush()
    #     urllib.request.urlretrieve(video_path_on_ftp, video_path_in_local_folder)
    #     print("[DONE]")
    # else:
    #     print("Video already in local folder")

    #     if not is_video_on_ftp:
    #         print("Video not on FTP server")
    #         print("Uploading video to FTP server", end=" ")
    #         sys.stdout.flush()
    #         upload_video_to_ftp(video_filename_with_extension)
    #         print("[DONE]")

    return {
        "title_slug": video_title_slug,
        "name_with_extension": video_filename_with_extension,
        "path_on_ftp": video_path_on_ftp,
        "path_in_local_folder": video_path_in_local_folder,
    }