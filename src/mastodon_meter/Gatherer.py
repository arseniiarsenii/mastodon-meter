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
        self._db_wrapper: MongoDbWrapper = MongoDbWrapper()

    async def gather_meterings(self) -> tp.Tuple[int, float]:
        """do meterings for all the tracked accounts asynchronously"""
        t0: float = time()
        tracked_accounts: tp.List[Account] = await self._db_wrapper.get_tracked_accounts()
        meterings: tp.List[Metering] = []
        logger.info(f"Gathering meterings for {len(tracked_accounts)} accounts")

        async with httpx.AsyncClient() as client:
            for account in tracked_accounts:
                response: httpx.Response = await client.get(account.account_data_link)
                response_payload: ResponsePayload = response.json()
                meterings.append(
                    Metering(
                        toot_count=response_payload["statuses_count"],
                        subscribers_count=response_payload["followers_count"],
                        parent_account_internal_id=account.internal_id,
                    )
                )

        await self._db_wrapper.add_meterings(meterings)

        metering_count: int = len(meterings)
        execution_time: float = round(time() - t0, 3)
        logger.info(f"Gathered {metering_count} meterings in {execution_time} seconds.")
        return metering_count, execution_time
