from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import requests, json, time

app = FastAPI()


class ItemList(BaseModel):
    phone_numbers: List[str]
    body: str


def get_access_token():
    token_file = "tokens.json"

    with open(token_file, "r") as f:
        data = json.loads(f.read())

    refresh_token = data["refresh_token"]
    access_token = data["access_token"]
    expires_in = int(data["expires_in"])
    token_time = data["created_time"]

    if time.time() - token_time > expires_in:
        secret_key = "j4yC3G5MGCGC6OsB2AFe"
        app_id = "1726087278974764839"

        url = "https://oauth.zaloapp.com/v4/oa/access_token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "secret_key": secret_key,
        }
        data = {
            "refresh_token": refresh_token,
            "app_id": app_id,
            "grant_type": "refresh_token",
        }

        tokens = requests.post(url, data=data, headers=headers).json()

        access_token = tokens["access_token"]
        tokens["created_time"] = time.time()

        with open(token_file, "w") as f:
            json.dump(tokens, f, indent=4)
    else:
        print("access token still valid!")
    return access_token


@app.post("/bulk-sms/")
async def bulk_sms(items: ItemList):
    access_token = get_access_token()

    url = "https://openapi.zalo.me/v3.0/oa/message/cs"
    headers = {"Content-Type": "application/json", "access_token": access_token}
    numbers = items.phone_numbers
    for number in numbers:
        data = {
            "recipient": {"user_id": number},
            "message": {"text": items.body},
        }

        response = requests.post(url, json=data, headers=headers)

        print(response.json())
    
    return {"msg": "Messages send successfully!"}