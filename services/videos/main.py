from typing import Union

from fastapi import FastAPI
from repository import Repository
from domain import Video

app = FastAPI(root_path='/api/videos')
repository = Repository()

@app.get('/')
def read_root():
    return {'Hello': 'Videos 3'}

@app.get('/items/{item_id}')
def read_item(item_id: int, q: Union[str, None] = None):
    return {'item_id': item_id, 'q': q}