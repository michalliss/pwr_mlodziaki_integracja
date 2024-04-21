from typing import Dict
import uuid
import random
from domain import Room, RoomStatus, User, Video


class Repository:
    def __init__(self, postgres_handler):
        self.postgres_handler = postgres_handler

    def get_rooms(self):
        with self.postgres_handler.connect_to_db() as conn:
            with conn.cursor() as cur:
                cur.execute("""SELECT * FROM rooms""")
                return cur.fetchall()

    def add_room(self, room: Room):
        with self.postgres_handler.connect_to_db() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO rooms(id, name, owner_id, status, video_id) VALUES (%s, %s, %s, 'NO_VIDEO', null)", (room.id, room.name, room.owner, room.status, room.video_id))
                return cur.fetchone()

    def get_room(self, room_id: str):
        with self.postgres_handler.connect_to_db() as conn:
            with conn.cursor() as cur:
                cur.execute("""SELECT * FROM rooms WHERE id=%s""", (room_id,))
                return cur.fetchone()

    def delete_room(self, room_id):
        with self.postgres_handler.connect_to_db() as conn:
            with conn.cursor() as cur:
                cur.execute("""DELETE FROM rooms WHERE id=%s""", (room_id,))
        del self.rooms[room_id]