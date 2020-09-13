import requests
import os
from kivy.logger import Logger

from dotenv import load_dotenv
load_dotenv()


def login(username: str, password: str) -> bool:
    body = {"username": username,
            "password": password}
    try:
        response = requests.post(os.getenv("LOGIN_ENDPOINT"))
        return response.json()["ok"]
    except Exception as e:
        Logger.warn(f"Could not verify user {username}")
        return False

def register(username: str, password:str, email: str) -> bool:
    pass