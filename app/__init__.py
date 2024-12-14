from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router

from app.lifespan import lifespan
from config import config

app = FastAPI(lifespan=lifespan)

origins = ["http://localhost:5173",
           "http://127.0.0.1:5173", config.app.client_url]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
