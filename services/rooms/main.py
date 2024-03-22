from dataclasses import dataclass
from typing import Union
import uuid
from fastapi import FastAPI
import kafka_handler
from domain import Room
from repository import Repository

app = FastAPI(root_path="/api/rooms")
repository = Repository()

@app.get("")
def read_root():
    return {"Hello": "Rooms"}

@app.get("/create_room/{room_name}")
async def create_room(room_name: str):
    id = str(uuid.uuid4())
    repository.add_room(Room(id=id, name=room_name))
    await kafka_handler.send_one("main_topic", ("room_created", id))
    return {"room": repository.get_room(id)}

@app.get("/rooms")
async def read_rooms():
    return {"rooms": repository.rooms}