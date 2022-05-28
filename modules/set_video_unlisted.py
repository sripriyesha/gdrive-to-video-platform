import re

import googleapiclient
from simple_youtube_api.Channel import Channel

from settings import *


def set_video_unlisted(channel_credentials_file, youtube_video_id, title, description):
    channel = Channel()
    channel.login(
        CLIENT_SECRET_FILE,
        channel_credentials_file,
    )

    title = title.replace("\n", "").replace("\r", "").replace("\t", "")
    # remove multiple spaces
    title = re.sub(" +", " ", title)

    title_length = len(title)

    if title_length > 100:
        print("Video title has to be 100 characters long maximum")
        print("current title length: " + str(title_length))
        return False

    request = (
        channel.get_login()
        .videos()
        .update(
            body={
                "id": youtube_video_id,
                "snippet": {
                    # title max 100 characters
                    "title": title,
                    # description max 5000 characters
                    "description": description,
                    "categoryId": 29,
                },
                "status": {"privacyStatus": "unlisted"},
            },
            part="snippet,status",
        )
    )

    response = None
    try:
        response = request.execute()
    except googleapiclient.errors.HttpError as e:
        if "The request metadata specifies an invalid or empty video title." in str(e):
            print("Issue while updating video")
            print()
            print("Error:")
            print(str(e))
        else:
            print("googleapiclient.errors.HttpError:")
            print(str(e))

        return False
    except Exception as e:
        print("Generic Exception:")
        print(str(e))
        return False

    return True