import googleapiclient
from simple_youtube_api.Channel import Channel

from settings import *


def delete_video(channel_credentials_file, youtube_video_id):
    channel = Channel()
    channel.login(
        CLIENT_SECRET_FILE,
        channel_credentials_file,
    )

    request = channel.get_login().videos().delete(id=youtube_video_id)
    try:
        response = request.execute()
    except googleapiclient.errors.HttpError as e:
        print(str(e))
        return False
    except Exception as e:
        return False

    return True