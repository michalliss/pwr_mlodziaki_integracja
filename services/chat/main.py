import asyncio
import json
from typing import Dict, List
from fastapi import FastAPI
import kafka_handler
from dataclasses import dataclass

app = FastAPI(root_path="/api/chat")

@dataclass
class Room:
    id: str
    messages: List[str]

rooms: Dict[str, Room] = {}


async def consume_handler(msg):
    print(f"Consumed: {msg}")
    match msg:
        case ("room_created", x):
            rooms[x] = Room(id=x, messages=[])



asyncio.create_task(kafka_handler.consume("main_topic", consume_handler))


@app.get("/")
async def read_root():
    return {"Hello": "Chat"}


@app.get("/rooms")
async def read_item():
    return {"rooms": rooms}