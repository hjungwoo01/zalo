from fastapi import FastAPI, responses, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
from typing import List
from datetime import datetime
import requests, json, time
import os, threading


class FlowModel(BaseModel):
    numbers: List[str]
    template: int
    auto_run: bool
    schedule: dict | None


class TemplateModel(BaseModel):
    name: str
    text: str


def read_json_file(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def write_json_file(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


def get_max_id(data):
    try:
        return max([item["id"] for item in data], default=0)
    except KeyError:
        return 0


def get_access_token():
    token_file = "tokens.json"

    data = read_json_file(token_file)

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

        write_json_file(token_file, tokens)
    else:
        print("access token still valid!")
    return access_token


def send_sms(numbers, body):
    access_token = get_access_token()

    url = "https://openapi.zalo.me/v3.0/oa/message/cs"
    headers = {"Content-Type": "application/json", "access_token": access_token}
    for number in numbers:
        data = {
            "recipient": {"user_id": number},
            "message": {"text": body},
        }

        response = requests.post(url, json=data, headers=headers)

        print(response.json())


def start_function(d):
    template_file = "./templates.json"
    data = read_json_file(template_file)

    result = next(
        (item["text"] for item in data if item["id"] == d["template"]),
        None,
    )
    if result is not None:
        t = threading.Thread(target=send_sms, args=(d["numbers"], result))
        t.start()


stop_flag = False


def cron_job():
    global stop_flag
    print("Cron job started...")
    while not stop_flag:
        flow_file = "./flows.json"

        data = read_json_file(flow_file)

        for d in data:
            if d["auto_run"]:
                schedule: dict = d["schedule"]
                for key, value in schedule.items():
                    current_time = datetime.now().strftime("%H:%M")
                    current_day = datetime.now().strftime("%A")
                    if current_time == value:
                        if key.lower() == "daily":
                            start_function(d)
                        elif key.title() == current_day:
                            start_function(d)
    print("Cron job stopped...")


@asynccontextmanager
async def lifespan(app: FastAPI):
    global stop_flag

    t = threading.Thread(target=cron_job)
    t.start()

    yield

    stop_flag = True


app = FastAPI(lifespan=lifespan)


@app.post("/add-template/", status_code=201)
async def add_template(data: TemplateModel):
    file_name = "./templates.json"
    tem = read_json_file(file_name)

    id = get_max_id(tem) + 1
    d = {"id": id, **data.dict()}
    tem.append(d)

    write_json_file(file_name, tem)

    return {"msg": "Template added successfully!"}


@app.get("/get-templates/")
async def get_templates():
    file_name = "./templates.json"
    tem = read_json_file(file_name)

    return tem


@app.delete("/delete-template/")
async def delete_template(id: int):
    file_name = "./templates.json"

    data = read_json_file(file_name)
    result = next((item for item in data if item["id"] == id), None)

    if result:
        data.remove(result)
        write_json_file(file_name, data)
        return responses.JSONResponse(
            content={"msg": "Template deleted successfully!"}, status_code=204
        )

    return responses.JSONResponse(
        content={"msg": "No template found with given id!"}, status_code=404
    )


@app.post("/create-flow/", status_code=201)
async def create_flow(data: FlowModel):
    template_file = "./templates.json"
    flow_file = "./flows.json"

    templates = read_json_file(template_file)

    print(type(data))
    if data.template not in {item["id"] for item in templates}:
        raise HTTPException(
            status_code=404,
            detail="No template found with the given id!",
        )

    tem = read_json_file(flow_file)

    new_id = get_max_id(tem) + 1

    d = {"id": new_id}
    d.update(data.dict())
    tem.append(d)

    write_json_file(flow_file, tem)

    return {"msg": "Flow added successfully!"}


@app.get("/get-flows/")
async def get_flows():
    file_name = "./flows.json"
    tem = read_json_file(file_name)

    return tem
