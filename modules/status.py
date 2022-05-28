import requests
import sys
import pprint

import googleapiclient
from simple_youtube_api.YouTubeVideo import YouTubeVideo
from simple_youtube_api.Channel import Channel
from simple_youtube_api.YouTube import YouTube

from settings import *


def get_status(channel_credentials_file, youtube_video_id):
    channel = Channel()
    channel.login(
        CLIENT_SECRET_FILE,
        channel_credentials_file,
    )

    request = (
        channel.get_login()
        .videos()
        .list(
            id=youtube_video_id,
            part="processingDetails, status",
        )
    )

    response_items = None
    response = None

    try:
        response = request.execute()
        response_items = response["items"]

        if len(response_items) > 0:
            return {
                "uploadStatus": response_items[0]["status"]["uploadStatus"],
                "processingStatus": response_items[0]["processingDetails"][
                    "processingStatus"
                ],
            }
        else:
            return {"uploadStatus": "deleted"}

    except Exception as e:
        print("Error:")
        print(str(e))

        if response is not None:
            print("Response:")
            print(response)

    return None


def is_processing(channel_credentials_file, youtube_video_id):
    return get_status(channel_credentials_file, youtube_video_id) == "processing"
