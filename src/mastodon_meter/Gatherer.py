import asyncio
import datetime as dt
import os
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

    @staticmethod
    def _get_delay() -> int:
        """get delay time"""
        delay: int = int(os.getenv("METERING_INTERVAL", default=0))

        if delay:
            logger.info(f"Metering internal is set to {delay} s.")
        else:
            # by default metering will happen daily at 03:00 UTC
            now: dt.datetime = dt.datetime.utcnow()
            next_gathering: dt.datetime = dt.datetime(now.year, now.month, now.day, 3)
            if now > next_gathering:
                next_gathering += dt.timedelta(days=1)

            delay_: dt.timedelta = next_gathering - now
            delay = int(delay_.total_seconds())
            logger.info(f"Next gathering is staged for {next_gathering} UTC.")

        return delay

    async def start_metering_daemon(self) -> None:
        """sets a never ending task for metering"""
        logger.info("Started metering daemon")
        while True:
            delay: int = self._get_delay()
            logger.info(f"Sleeping {delay} s. before next metering.")
            await asyncio.sleep(delay)
            await self.gather_meterings()

    @staticmethod
    async def gather_meterings() -> tp.Tuple[int, float]:
        """do meterings for all the tracked accounts asynchronously"""
        t0: float = time()
        tracked_accounts: tp.List[Account] = await MongoDbWrapper().get_tracked_accounts()
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

        await MongoDbWrapper().add_meterings(meterings)

        metering_count: int = len(meterings)
        execution_time: float = round(time() - t0, 3)
        logger.info(f"Gathered {metering_count} meterings in {execution_time} seconds.")
        return metering_count, execution_time
