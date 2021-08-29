import typing as tp
import os

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from _logging import CONSOLE_LOGGING_CONFIG, FILE_LOGGING_CONFIG

# apply logging configuration
logger.configure(handlers=[CONSOLE_LOGGING_CONFIG, FILE_LOGGING_CONFIG])

# global variables
api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    # start the server
    host: str = os.getenv("SERVER_HOST", default="0.0.0.0")
    port: int = int(os.getenv("SERVER_PORT", default=8080))
    logger.info(f"Server started at {host}:{port}")
    uvicorn.run("app:api", host=host, port=port)
