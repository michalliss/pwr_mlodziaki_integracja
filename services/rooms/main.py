from dataclasses import dataclass
from typing import Union
import uuid
from fastapi import FastAPI
import kafka_handler

app = FastAPI(root_path="/api/rooms")

@dataclass
class Room:
    id: str
    name: str

rooms: dict[str, Room] = {}

@app.get("")
def read_root():
    return {"Hello": "Rooms"}

@app.get("/create_room/{room_name}")
async def create_room(room_name: str):
    id = str(uuid.uuid4())
    rooms[id] = Room(id=id, name=room_name)
    await kafka_handler.send_one("main_topic", ("room_created", id))
    return {"room": rooms[id]}

@app.get("/rooms")
async def read_rooms():
    return {"rooms": rooms}