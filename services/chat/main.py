import asyncio
import json
from typing import Dict, List
from fastapi import FastAPI, WebSocket
import kafka_handler
from dataclasses import dataclass
from repository import Repository
from domain import Room
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(root_path="/api/chat")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


repository = Repository()


async def consume_handler(msg):
    match msg:
        case ('room_created', x):
            repository.add_room(Room(id=x, messages=[]))


asyncio.create_task(kafka_handler.consume('main_topic', consume_handler))


@app.get("/")
async def read_root():
    return {'Hello': 'Chat'}


@app.get("/rooms")
async def read_item():
    return {"rooms": repository.get_rooms()}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
    
