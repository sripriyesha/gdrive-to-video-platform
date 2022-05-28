# Standard library imports
import logging
import time
from urllib.parse import urlparse, parse_qs
from urllib.error import HTTPError

# Third party imports
from pytube import YouTube
from pytube.cli import on_progress
import requests
from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo
from slugify import slugify
from tqdm import tqdm
from youtube_dl import YoutubeDL

# User imports
from settings import *

# TODO
def is_youtube_video_region_restricted(yt_link_or_video_id):
    params = {
        "part": "contentDetails",
        "id": extract_youtube_video_id(yt_link_or_video_id),
        "key": API_KEY_GOOGLE,
    }
    response = requests.get(URL_YOUTUBE_API_VIDEOS, params=params)
    return response.url


# TODO improve
def extract_youtube_video_id(value):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    query = urlparse(value)
    if query.hostname == "youtu.be":
        return query.path[1:]
    if query.hostname in ("www.youtube.com", "youtube.com"):
        if query.path == "/watch":
            p = parse_qs(query.query)
            return p["v"][0]
        if query.path[:7] == "/embed/":
            return query.path.split("/")[2]
        if query.path[:3] == "/v/":
            return query.path.split("/")[2]
    # fail?
    return None


def download_video_from_youtube(yt_link, output_filename):
    download_success = False

    while not download_success:
        try:
            yt = YouTube(yt_link, on_progress_callback=on_progress)

            yt.streams.first().download(
                output_path=LOCAL_VIDEOS_FOLDER_PATH, filename=output_filename
            )
            download_success = True
        except KeyError as e:
            # Video probably blocked in some countries
            if "streamingData" in str(e):
                raise

            print(e)
            time.sleep(10)
            download_success = False


def upload_to_youtube(channel_credentials_file, current_video_metadata):
    if not hasattr(upload_to_youtube, "channel"):
        channel = Channel()
        channel.login(CLIENT_SECRET_FILE, channel_credentials_file)
        upload_to_youtube.channel = channel

    video = LocalVideo(
        file_path=LOCAL_VIDEOS_FOLDER_PATH / current_video_metadata["mp4 name"]
    )

    video.set_title(current_video_metadata["mp4 name"])
    # video.set_description(current_video_metadata["Description"])
    video.set_privacy_status("public")
    return upload_to_youtube.channel.upload_video(video)


def get_channel_videos_list(all_uploads_playlist_id):
    """
    Returns a dictionary of format
    [
        {'video_title_1': 'youtube_video_id_1'},
        {'video_title_2': 'youtube_video_id_2'},
        ...
    ]
    """
    if hasattr(get_channel_videos_list, "title_id_dict"):
        return get_channel_videos_list.title_id_dict

    ytdl_opts = {
        "ignoreerrors": True,
        "extract_flat": "in_playlist",
        "dump_single_json": True,
        "quiet": True,
    }
    ytdl = YoutubeDL(ytdl_opts)

    channel_uploads_playlist_info = ytdl.extract_info(
        all_uploads_playlist_id, download=False
    )
    channel_videos = channel_uploads_playlist_info["entries"]
    channel_videos_by_title = {}

    for video in channel_videos:
        channel_videos_by_title[video["title"]] = video["id"]

    get_channel_videos_list.title_id_dict = channel_videos_by_title
    return channel_videos_by_title


def is_video_uploaded_on_destination_channel(channel_id, video_title):
    if not hasattr(is_video_uploaded_on_destination_channel, "title_id_dict"):
        is_video_uploaded_on_destination_channel.videos_list = get_channel_videos_list(
            # UC = User Channel
            # UU = User Uploads
            channel_id.replace("UC", "UU")
        )

    return video_title in is_video_uploaded_on_destination_channel.videos_list
