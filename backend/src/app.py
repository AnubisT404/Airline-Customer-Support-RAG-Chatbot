from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.chatbot import ChatBot
from utils.load_config import LoadConfig
import requests
import time

app = FastAPI()
CFG = LoadConfig.load()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PREPARE_URL = "http://prepare_data:8001/prepare-data/"

def trigger_data_refresh():
    """
    Trigger data prepare by making an HTTP POST request to the data_prepare API.
    """
    try:
        print(f"Triggering data refresh on {DATA_PREPARE_URL}")
        response = requests.post(DATA_PREPARE_URL, json={"force_refresh": False})
        if response.status_code == 200:
            print("Data refresh triggered successfully:", response.json())
        else:
            print(f"Data refresh failed: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Failed to trigger data refresh on startup: {e}")

@app.on_event("startup")
async def startup_event():
    time.sleep(5)
    trigger_data_refresh()

class QueryRequest(BaseModel):
    query: str

# Endpoint to handle chatbot queries
@app.post("/query")
async def handle_query(request: QueryRequest):
    try:
        print("Received query:", request.query)
        chatbot_instance = ChatBot()
        message = request.query
        response, _, error = chatbot_instance.respond([], message)
        if error:
            print(f"Error from chatbot: {error}")
            return {"message": error}
        print(f"Response from chatbot: {response}")
        return {"message": response}
    except Exception as e:
        print(f"Exception while calling respond(): {e}")
        raise HTTPException(status_code=500, detail=str(e))
