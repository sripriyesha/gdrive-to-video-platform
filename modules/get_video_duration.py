import isodate
from simple_youtube_api.YouTubeVideo import YouTubeVideo
from simple_youtube_api.Channel import Channel
from simple_youtube_api.YouTube import YouTube
import sys

from settings import *


def get_video_duration(channel_credentials_file, youtube_video_id):
    channel = Channel()
    channel.login(
        CLIENT_SECRET_FILE,
        channel_credentials_file,
    )

    request = (
        channel.get_login().videos().list(id=youtube_video_id, part="contentDetails")
    )

    try:
        response = request.execute()
        duration = isodate.parse_duration(
            response["items"][0]["contentDetails"]["duration"]
        )
        print(duration.total_seconds())

        print(response)
        sys.exit()
    except Exception as e:
        print("TODO")
        print(str(e))

    return True