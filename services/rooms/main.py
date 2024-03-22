import uuid
from fastapi import FastAPI
import kafka_handler
from domain import Room, RoomStatus, Video
from repository import Repository

app = FastAPI(root_path='/api/rooms')
repository = Repository()


@app.get('')
def read_root():
    return {'Hello': 'Rooms'}


@app.post('/create_room/{room_name}')
async def create_room(room_name: str):
    room_id = str(uuid.uuid4())
    repository.add_room(Room(id=room_id, name=room_name, users=[], status=RoomStatus.NO_VIDEO, video=None))
    await kafka_handler.send_one('main_topic', ('room_created', room_id))
    return {'room': repository.get_room(room_id)}


@app.delete('/delete_room/{room_id}')
async def delete_room(room_id: str):
    repository.delete_room(room_id)
    await kafka_handler.send_one('main_topic', ('room_deleted', room_id))
    return {'room': room_id}


@app.get('/room/{room_id}')
async def read_room(room_id: str):
    return {'room': repository.get_room(room_id)}


@app.get('/room/{room_id}/users')
async def read_room_users(room_id: str):
    room = repository.get_room(room_id)
    return {'users': room.users}


@app.post('/room/{room_id}/join/{user_id}')
async def join_room(room_id: str, user_id: str, user_name: str):
    room = repository.get_room(room_id)
    room.users.append((user_id, user_name))
    await kafka_handler.send_one('main_topic', ('user_joined', room_id, user_id))
    return {'room': room}


@app.delete('/room/{room_id}/leave/{user_id}')
async def leave_room(room_id: str, user_id: str):
    room = repository.get_room(room_id)
    room.users = [user for user in room.users if user[0] != user_id]
    await kafka_handler.send_one('main_topic', ('user_left', room_id, user_id))
    return {'room': room}


@app.post('/room/{room_id}/play')
async def play(room_id: str):
    room = repository.get_room(room_id)
    room.status = RoomStatus.PLAYING
    await kafka_handler.send_one('main_topic', ('video_played', room_id))
    return {'room': room}


@app.post('/room/{room_id}/pause')
async def pause(room_id: str):
    room = repository.get_room(room_id)
    room.status = RoomStatus.PAUSED
    await kafka_handler.send_one('main_topic', ('video_paused', room_id))
    return {'room': room}


@app.post('/room/{room_id}/set_video/{video_url}')
async def set_video(room_id: str, video_url: str):
    # TODO no video metadata is set
    room = repository.get_room(room_id)

    room.video = Video(url=video_url, length=0, progress=0)

    await kafka_handler.send_one('main_topic', ('video_set', room_id, video_url))
    return {'room': room}


@app.get('/room/{room_id}/video')
async def read_video(room_id: str):
    room = repository.get_room(room_id)

    if room.video is None:
        return {'video': None}

    return {'video': room.video.url}


@app.get('/room/{room_id}/status')
async def read_status(room_id: str):
    room = repository.get_room(room_id)
    return {'status': room.status}


@app.get('/room/{room_id}/progress')
async def read_progress(room_id: str):
    room = repository.get_room(room_id)

    if room.video is None:
        return {'progress': None}

    return {'progress': room.video.progress}


@app.get('/rooms')
async def read_rooms():
    return {'rooms': repository.rooms}
