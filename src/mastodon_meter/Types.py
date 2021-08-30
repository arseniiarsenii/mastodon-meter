import typing as tp

import pymongo

Document = tp.Dict[str, tp.Any]
Collection = pymongo.collection
ResponsePayload = tp.Dict[str, tp.Any]
