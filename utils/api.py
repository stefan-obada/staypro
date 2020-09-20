import requests
import os
import webbrowser
from kivy.logger import Logger

from dotenv import load_dotenv

load_dotenv()


def login(username: str, password: str) -> bool:
    body = {"username": username,
            "password": password}
    try:
        response = requests.post(os.getenv("LOGIN_ENDPOINT"), json=body, timeout=10)
        if response.json()["ok"]:
            os.environ["STAYPRO_TOKEN"] = response.json()["token"]
            if "real_name" in response.json().keys():
                os.environ["STAYPRO_REAL_NAME"] = response.json()["real_name"]
            else:
                os.environ["STAYPRO_REAL_NAME"] = username
            Logger.info(f"LOGIN: Successful login {username}")
            return True
        else:
            return False
    except Exception as e:
        Logger.warn(f"LOGIN: Could not verify user {username}")
        return False


def register(username: str, password: str, email: str, real_name: str) -> bool:
    body = {"username": username,
            "password": password,
            "email": email,
            "real_name": real_name}

    try:
        response = requests.post(os.getenv("LOGIN_ENDPOINT"), json=body, timeout=10)
        return response.json()["ok"]
    except Exception as e:
        Logger.warn(f"REGISTER: Could not register user {username}")
        return False


def get_activities(token: str):
    body = {"token": token}

    try:
        response = requests.get(os.getenv("ACTIVITIES_ENDPOINT"), json=body)
        return response.json()["activities"]  # TODO CHANGE IN SERVER BEFORE, do not use !!
    except Exception as e:
        Logger.warn(f"ACTIVITIES: Could not get activities for token {token}")
        return False


def post_activity(token: str, activity: str, seconds: float) -> bool:
    body = {"token": token,
            "activities": {activity: seconds}}
    # TODO : add the timestamp too

    try:
        response = requests.post(os.getenv("ACTIVITIES_ENDPOINT"), json=body, timeout=10)
        Logger.info(f"API: Posted activity {activity} for {seconds} seconds.")
        return response.json()["ok"]
    except Exception as e:
        Logger.warn(f"ACTIVITIES: Could not post activities for token {token}")
        return False


def open_history(token: str):
    webbrowser.open(os.path.join(os.getenv("HISTORY_ENDPOINT"), token))
