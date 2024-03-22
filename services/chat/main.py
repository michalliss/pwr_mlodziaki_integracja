import asyncio
import json
from typing import Dict, List
from fastapi import FastAPI
import kafka_handler
from dataclasses import dataclass
from repository import Repository
from domain import Room
import socketio

app = FastAPI(root_path='/api/chat')
repository = Repository()


async def consume_handler(msg):
    match msg:
        case ('room_created', x):
            repository.add_room(Room(id=x, messages=[]))


asyncio.create_task(kafka_handler.consume('main_topic', consume_handler))


sio = socketio.AsyncServer()


@sio.on('echo')
def echo(sid, data):
    sio.emit('echo', {'data': 'echo'})


@app.get('/')
async def read_root():
    return {'Hello': 'Chat'}


@app.get("/rooms")
async def read_item():
    return {'rooms': repository.get_rooms()}
