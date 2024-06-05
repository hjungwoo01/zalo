from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import requests
import os

app = FastAPI()


class ItemList(BaseModel):
    phone_numbers: List[str | int]
    body: str


def get_tokens():
    secret_key = "j4yC3G5MGCGC6OsB2AFe"
    app_id = "1726087278974764839"

    url = "https://oauth.zaloapp.com/v4/oa/access_token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "secret_key": secret_key,
    }
    data = {
        "code": "<your_oauth_code>",
        "app_id": app_id,
        "grant_type": "authorization_code",
    }

    response = requests.post(url, data=data, headers=headers)

    return response


@app.post("/bulk-sms")
async def bulk_sms(items: ItemList):
    token_file = "refresh_token.txt"
    if os.path.exists(token_file):
        pass
    tokens = get_tokens()
    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]

    with open(token_file, "w") as f:
        f.write(refresh_token)

    url = "https://openapi.zalo.me/v3.0/oa/message/cs"
    headers = {"Content-Type": "application/json", "access_token": access_token}
    numbers = items.phone_numbers
    for number in numbers:
        data = {
            "recipient": {"user_id": f"{number}"},
            "message": {"text": items.body},
        }

        response = requests.post(url, json=data, headers=headers)

        print(response.json())
