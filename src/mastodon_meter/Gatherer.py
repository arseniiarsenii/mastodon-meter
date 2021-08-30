import typing as tp
from time import time

import httpx
from loguru import logger

from .Account import Account
from .Metering import Metering
from .Singleton import SingletonMeta
from .Types import ResponsePayload
from .database import MongoDbWrapper


class Gatherer(metaclass=SingletonMeta):
    """Gathers data for all the tracked accounts and stores it in the database"""

    def __init__(self) -> None:
        self.db_wrapper: MongoDbWrapper = MongoDbWrapper()

    async def gather_meterings(self) -> None:
        """do meterings for all the tracked accounts asynchronously"""
        t0: float = time()
        tracked_accounts: tp.List[Account] = self.db_wrapper.get_tracked_accounts()
        logger.info(f"Gathering meterings for {len(tracked_accounts)} accounts")
        async with httpx.AsyncClient() as client:
            responses: tp.List[httpx.Response] = [await client.get(acc.account_data_link) for acc in tracked_accounts]
        response_payloads: tp.List[ResponsePayload] = [response.json() for response in responses]
        meterings: tp.List[Metering] = [
            Metering(
                toot_count=response["statuses_count"],
                subscribers_count=response["followers_count"],
                parent_account_internal_id=account.internal_id,
            )
            for response, account in zip(response_payloads, tracked_accounts)
        ]
        self.db_wrapper.add_meterings(meterings)
        logger.info(f"Gathered {len(meterings)} meterings for in {round(time()-t0, 3)} seconds.")
