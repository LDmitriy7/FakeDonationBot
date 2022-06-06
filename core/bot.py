import logging
from dataclasses import dataclass
from typing import Callable, Any

import requests

from . import c as c
from . import utils, errors
from .filters import Filter

Func = Callable[[], Any]

API_ENDPOINT = 'https://api.telegram.org/bot{token}/{method}'


@dataclass
class Handler:
    func: Func
    filters: list[Filter]


@dataclass
class Task:
    func: Func


class Bot:
    def __init__(self):
        self.handlers: list[Handler] = []
        self.tasks: list[Task] = []
        self.session = requests.Session()

    def add_handler(self, func: Func, filters: list[Filter] = None):
        handler = Handler(func, filters or [])
        self.handlers.append(handler)

    def request(self, method: str, params: dict) -> dict | list | bool | str | int:
        from .loader import ctx

        params = utils.clear_params(params)
        url = API_ENDPOINT.format(token=ctx.token, method=method)

        logging.debug(f'Request {method} with params: {params}')
        resp = self.session.post(url, json=params)
        result: dict = resp.json()

        if result[c.OK]:
            return result[c.RESULT]
        else:
            raise errors.Error(result[c.ERROR_CODE], result[c.DESCRIPTION])
