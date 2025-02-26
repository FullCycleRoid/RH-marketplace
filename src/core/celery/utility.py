import asyncio

import httpx


def get_request(url) -> str:
    response = httpx.get(url, verify=False)
    if not response.is_success:
        raise ConnectionError
    return response.text


def post_request(url: str, data: dict):
    response = httpx.post(url, data=data)
    if not response.is_success:
        raise ConnectionError


def run_async_subtask(func, **kwargs):
    loop = asyncio.get_event_loop()
    res = loop.run_until_complete(asyncio.gather(func(**kwargs)))
    return res[0]
