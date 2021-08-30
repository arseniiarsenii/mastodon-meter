import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from _logging import CONSOLE_LOGGING_CONFIG, FILE_LOGGING_CONFIG
from mastodon_meter.Types import ResponsePayload
from mastodon_meter.models import (
    AccountRawData,
    AddAccountRequest,
    AddAccountResponse,
    DeleteAccountRequest,
    GraphRequest,
    ResponseBase,
    TrackedAccountList,
)

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


@api.post("/api/accounts/add", response_model=AddAccountResponse)
def add_tracked_account(account_data: AddAccountRequest) -> ResponsePayload:
    """add an account to the list of tracked"""
    raise NotImplementedError


@api.post("/api/accounts/remove", response_model=ResponseBase)
def remove_tracked_account(account_data: DeleteAccountRequest) -> ResponsePayload:
    """remove an account from the list of tracked"""
    raise NotImplementedError


@api.get("/api/accounts/tracked", response_model=TrackedAccountList)
def get_tracked_accounts() -> ResponsePayload:
    """return the list of tracked accounts"""
    raise NotImplementedError


@api.get("/api/{account_internal_id}/data", response_model=AccountRawData)
def get_account_data() -> ResponsePayload:
    """get raw data for an account"""
    raise NotImplementedError


@api.get("/api/{account_internal_id}/graph/subscribers")
def get_subscribers_graph(time_boundaries: GraphRequest) -> ResponsePayload:
    """get subscribers graph for an account"""
    raise NotImplementedError


@api.get("/api/{account_internal_id}/graph/toots")
def get_toots_graph(time_boundaries: GraphRequest) -> ResponsePayload:
    """get toots graph for an account"""
    raise NotImplementedError


@api.get("/api/{account_internal_id}/graph/common")
def get_common_graph(time_boundaries: GraphRequest) -> ResponsePayload:
    """get common (toots and subscribers) graph for an account"""
    raise NotImplementedError


if __name__ == "__main__":
    # start the server
    host: str = os.getenv("SERVER_HOST", default="0.0.0.0")
    port: int = int(os.getenv("SERVER_PORT", default=8080))
    logger.info(f"Server started at {host}:{port}")
    uvicorn.run("app:api", host=host, port=port)
