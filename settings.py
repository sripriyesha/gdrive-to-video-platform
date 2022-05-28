from pathlib import Path

# Folders
LOCAL_VIDEOS_FOLDER_PATH = Path("./videos/")
CREDENTIALS_FOLDER = Path("./credentials/")


# FTP
FTP_HOST = "sripriyesha.com"
FTP_LOGIN = "ntvarchives@ntvarchives.sripriyesha.com"
FTP_PASSWORD = "W(wrQ}a~@'bg2fg9b2@vCN:Ad6(]"
FTP_PUBLIC_VIDEOS_FOLDER_URL_PATH = "https://ntvarchives.sripriyesha.com/videos/"

# Worksheet
# gspread: read, update google sheet
GSPREAD_SERVICE_ACCOUNT_FILE = CREDENTIALS_FOLDER / "gspread_service_account.json"
# Sri Nithya Priyeshananda's Google Api Key for gspread
API_KEY_GOOGLE = "AIzaSyBK3ozMZg05M8q9ryLjsb2xm4DbYoNjYpg"

# Youtube
CLIENT_SECRET_FILE = (
    CREDENTIALS_FOLDER
    / "client_secret_643144716324-64qgmn98m6jok9utg9o8mtpf382glp4q.apps.googleusercontent.com.json"
)
URL_YOUTUBE_API_VIDEOS = "https://www.googleapis.com/youtube/v3/videos"

DESTINATION_CHANNELS_CONFIG = {
    "news videos 1": {"id": "UC9VNa-B6sdHDF9dMuza6Gcg"},
}

UPLOAD_LIMIT_EXCEEDED_ERROR = (
    "The user has exceeded the number of videos they may upload."
)
