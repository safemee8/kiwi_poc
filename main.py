import json

from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from starlette import status
from starlette.responses import JSONResponse, Response
import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models import MeetingsReqModel

api_key = "945B596952E66032A1A3F5307F48B3EB"
api_secret = "961de5806ebf327baebd854f1946b289c27616cf297850f883c8f0e190c0be56"
webhook_url = "http://google.com"

events = []

app = FastAPI(title="Kiwi.app API", docs_url=None, redoc_url=None, openapi_url=None)
templates = Jinja2Templates(directory="static")


@app.get("/openapi.json")
async def open_api_endpoint():
    return JSONResponse(get_openapi(title="SaleAssist Internal API", version="1", routes=app.routes))


@app.get("/docs")
async def get_docs():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


@app.get("/redoc")
async def get_redoc():
    return get_redoc_html(openapi_url="/openapi.json", title="redoc")


@app.get("/ping")
def api_ping():
    return {"ping": "pong!"}


@app.get("/")
def homepage():
    return HTMLResponse(templates.get_template("index.html").render({"port": 8002}))


@app.post("/webhook")
async def capture_events(request: Request):
    request_body = await request.body()
    if type(request_body) is bytes:
        request_body = request_body.decode('utf-8')
        try:
            response = json.loads(request_body)
            events.append(response["event_type"] + " " + response["payload"]["id"])
            print(json.dumps(json.loads(request_body), indent=4))
            print(events)
            return True
        except Exception as e:
            print(request_body)
            print(e)
            return True


@app.get("/events")
async def get_events(request: Request):
    return events


@app.get("/flush_events")
async def flush_events(request: Request):
    global events
    events = []
    return events


@app.post("/create_meeting")
async def create_meeting(model: MeetingsReqModel, request: Request):
    api_response = requests.post(
        url="https://platform.saleassist.ai/api/meetings/v1",
        json=model.dict(),
        headers={
            "api_key": api_key,
            "api_secret": api_secret
        }
    )
    print(json.dumps(json.loads(api_response.content.decode('utf-8')), indent=4))
    if api_response.status_code == 200:
        return json.loads(api_response.content.decode('utf-8'))
    else:
        return "failed"


@app.get("/start_meeting/{meeting_id}")
async def start_meeting(meeting_id: str, request: Request):
    api_response = requests.get(
        url="https://platform.saleassist.ai/api/meetings/v1/start/" + meeting_id,
        headers={
            "api_key": api_key,
            "api_secret": api_secret
        }
    )
    if api_response.status_code == 200:
        return json.loads(api_response.content.decode('utf-8'))
    else:
        return "failed"


@app.get("/end_meeting/{meeting_id}")
async def end_meeting(meeting_id: str, request: Request):
    api_response = requests.get(
        url="https://platform.saleassist.ai/api/meetings/v1/end/" + meeting_id,
        headers={
            "api_key": api_key,
            "api_secret": api_secret
        }
    )

    if api_response.status_code == 200:
        return json.loads(api_response.content.decode('utf-8'))
    else:
        return "failed"


@app.get("/get_meeting_document/{meeting_id}")
async def end_meeting(meeting_id: str, request: Request):
    api_response = requests.get(
        url="https://platform.saleassist.ai/api/meetings/v1/meeting_document/" + meeting_id,
        headers={
            "api_key": api_key,
            "api_secret": api_secret
        }
    )

    if api_response.status_code == 200:
        return json.dumps(json.loads(api_response.content.decode('utf-8')), indent=4)
    else:
        return "failed"
