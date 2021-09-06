import typing as tp
from datetime import datetime

from mastodon_meter.Account import Account
from mastodon_meter.Metering import Metering
from mastodon_meter.Types import GraphData
from mastodon_meter.database import MongoDbWrapper
from mastodon_meter.models import GraphRequest


def filter_metering_by_time(
    meterings: tp.List[Metering], since: tp.Optional[str], to: tp.Optional[str]
) -> tp.List[Metering]:
    """filter meterings to only leave ones that are within the time boundaries"""
    date_format: str = "%Y-%m-%d %H:%M"
    since_: tp.Optional[datetime] = datetime.strptime(since, date_format) if since else None
    to_: tp.Optional[datetime] = datetime.strptime(to, date_format) if to else None
    return list(filter(lambda m: m.is_within_range(since_, to_), meterings))


async def get_plot_data(account_internal_id: str, time_boundaries: GraphRequest) -> GraphData:
    """gather data for drawing the plot"""
    account: Account = await MongoDbWrapper().get_account_by_internal_id(account_internal_id)
    meterings: tp.List[Metering] = await MongoDbWrapper().get_all_meterings(account_internal_id)
    meterings = filter_metering_by_time(meterings, time_boundaries.since, time_boundaries.to)
    return meterings, account
