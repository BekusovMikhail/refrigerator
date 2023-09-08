from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db_api import *

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/api/cameras_by_username/{username}")
def get_cameras(username: str):
    user_id = select_user_id(username)
    return select_cameras(user_id)

@app.get("/api/counters_by_camera/{camera_id}")
def get_counters(camera_id: int):
    return select_counters(camera_id)

@app.get("/api/product_id_by_name/{name}")
def get_product_id(name: str):
    return {"product_id": select_product_id(name)}

@app.get("/api/user_id_by_name/{name}")
def get_product_id(name: str):
    return {"user_id": select_user_id(name)}

