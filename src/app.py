import asyncio
import typing as tp

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from _logging import CONSOLE_LOGGING_CONFIG, FILE_LOGGING_CONFIG
from mastodon_meter.Account import Account
from mastodon_meter.Gatherer import Gatherer
from mastodon_meter.Metering import Metering
from mastodon_meter.Types import ResponsePayload
from mastodon_meter.database import MongoDbWrapper
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
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/accounts/add", response_model=tp.Union[AddAccountResponse, ResponseBase])  # type: ignore
async def add_tracked_account(account_data: AddAccountRequest) -> ResponsePayload:
    """add an account to the list of tracked"""
    logger.info("Adding account into the list of tracked")

    try:
        account: Account = Account(
            username=account_data.username,
            instance=account_data.instance,
            id=account_data.instance_id,
        )
        await MongoDbWrapper().add_tracked_account(account)

        message: str = f"Added account {account.internal_id} to the list of tracked"
        logger.info(message)

        response: ResponsePayload = {
            "status": True,
            "message": message,
            "account_internal_id": account.internal_id,
        }
        return response

    except Exception as e:
        message = f"An error occurred while adding the account: {e}"
        logger.error(message)
        return {"status": False, "message": message}


@app.post("/api/accounts/remove", response_model=ResponseBase)
async def remove_tracked_account(account_data: DeleteAccountRequest) -> ResponsePayload:
    """remove an account from the list of tracked"""
    logger.info(f"Deleting account {account_data.account_internal_id} from the list of tracked")

    try:
        await MongoDbWrapper().delete_tracked_account(account_data.account_internal_id)
        message: str = f"Removed account {account_data.account_internal_id} from the list of tracked"
        logger.info(message)

        if account_data.remove_associated_data:
            logger.info(f"Removing meterings associated with account {account_data.account_internal_id}")
            meterings: tp.List[Metering] = await MongoDbWrapper().get_all_meterings(account_data.account_internal_id)
            metering_ids: tp.Set[str] = {m.internal_id for m in meterings}
            await MongoDbWrapper().delete_meterings(metering_ids)
            logger.info(f"Removed all meterings associated with account {account_data.account_internal_id}")

        response: ResponsePayload = {
            "status": True,
            "message": message,
        }
        return response

    except Exception as e:
        message = f"An error occurred while removing the account: {e}"
        logger.error(message)
        return {"status": False, "message": message}


@app.get("/api/accounts/tracked", response_model=TrackedAccountList)
async def get_tracked_accounts() -> ResponsePayload:
    """return the list of tracked accounts"""
    logger.info("Gathering tracked accounts")

    try:
        tracked_accounts: tp.List[Account] = await MongoDbWrapper().get_tracked_accounts()
        response: ResponsePayload = {
            "status": True,
            "message": f"Gathered {len(tracked_accounts)} tracked accounts.",
            "tracked_accounts": [
                {
                    "internal_id": account.internal_id,
                    "username": account.username,
                    "instance": account.instance,
                    "instance_id": account.id,
                    "added_on": str(account.added_on),
                }
                for account in tracked_accounts
            ],
        }
        return response

    except Exception as e:
        message: str = f"An error occurred while gathering tracked accounts: {e}"
        logger.error(message)
        return {"status": False, "message": message}


@app.get("/api/{account_internal_id}/data", response_model=AccountRawData)
async def get_account_data(account_internal_id: str) -> ResponsePayload:
    """get raw data for an account"""
    logger.info(f"Gathering raw data for account {account_internal_id}")

    try:
        meterings: tp.List[Metering] = await MongoDbWrapper().get_all_meterings(account_internal_id)
        response: ResponsePayload = {
            "status": True,
            "message": f"Gathered raw data for account {account_internal_id}",
            "account_internal_id": account_internal_id,
            "data": [
                {
                    "toot_count": int(m.toot_count),
                    "subscribers_count": int(m.subscribers_count),
                    "metering_id": str(m.internal_id),
                    "timestamp": str(m.timestamp),
                }
                for m in meterings
            ],
        }
        return response

    except Exception as e:
        message: str = f"An error occurred while gathering raw data: {e}"
        logger.error(message)
        return {"status": False, "message": message}


@app.get("/api/{account_internal_id}/graph/subscribers")
def get_subscribers_graph(account_internal_id: str, time_boundaries: GraphRequest) -> ResponsePayload:
    """get subscribers graph for an account"""
    raise NotImplementedError


@app.get("/api/{account_internal_id}/graph/toots")
def get_toots_graph(account_internal_id: str, time_boundaries: GraphRequest) -> ResponsePayload:
    """get toots graph for an account"""
    raise NotImplementedError


@app.get("/api/{account_internal_id}/graph/common")
def get_common_graph(account_internal_id: str, time_boundaries: GraphRequest) -> ResponsePayload:
    """get common (toots and subscribers) graph for an account"""
    raise NotImplementedError


if __name__ == "__main__":
    # gather meterings
    asyncio.run(Gatherer().gather_meterings())
