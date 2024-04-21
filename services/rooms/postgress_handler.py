import os
import psycopg2
import psycopg2.extras
import uuid

psycopg2.extras.register_uuid()

postgress_password = os.environ.get('POSTGRES_PASSWORD')
postgress_user = os.environ.get('POSTGRES_USER')
postgress_host = os.environ.get('POSTGRES_HOST')
postgres_port = os.environ.get('POSTGRES_PORT')
postgres_database = os.environ.get('POSTGRES_DB')

def connect_to_db():
    return psycopg2.connect(database=postgres_database,
                          host=postgress_host,
                          user=postgress_user,
                          password=postgress_password,
                          port=postgres_port)

def init_db():
    with connect_to_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id UUID PRIMARY KEY,
                user_name VARCHAR(255) NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS videos (
                id UUID PRIMARY KEY,
                length INTEGER NOT NULL,
                progress INTEGER NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS rooms (
                id UUID PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                owner_id UUID NOT NULL,
                status VARCHAR(255) NOT NULL,
                video_id UUID,
                CONSTRAINT status_check CHECK(status IN ('PLAYING', 'PAUSED', 'NO_VIDEO')),
                CONSTRAINT fk__rooms__video_id FOREIGN KEY(video_id) REFERENCES videos(id),
                CONSTRAINT fk__rooms__owner_id FOREIGN KEY(owner_id) REFERENCES users(id)
            );
            
            CREATE TABLE IF NOT EXISTS users_in_rooms (
                id uuid PRIMARY KEY,
                room_id UUID NOT NULL,
                user_id UUID NOT NULL,
                CONSTRAINT fk__users_in_rooms__room_id FOREIGN KEY(room_id) REFERENCES rooms(id),
                CONSTRAINT fk__users_in_rooms__user_id FOREIGN KEY(user_id) REFERENCES users(id)
            );""")

def add_demo_data():
    with psycopg2.connect(database=postgres_database,
                          host=postgress_host,
                          user=postgress_user,
                          password=postgress_password,
                          port=postgres_port) as conn:
        with conn.cursor() as cur:
            seba_id = uuid.uuid4()
            cur.execute("INSERT INTO users(id, user_name) VALUES (%s, 'Seba')", (seba_id,))
            animal_homes = [('Bear', 'Den'), ('Devin', 'Mancave'), ('Bird', 'Nest'), ('Dog', 'Kennel'),
                            ('Horse', 'Stable'), ('Spider', 'Web')]
            for i, (animal, home) in enumerate(animal_homes):
                room_id = uuid.uuid4()
                cur.execute("INSERT INTO rooms(id, name, owner_id, status, video_id) VALUES (%s, %s, %s, 'NO_VIDEO', null)", (room_id, f'{animal}\'s {home}', seba_id))
