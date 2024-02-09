import json

import httpx

from config import CREATE_USER_URL, SEND_CODE_URL


async def _make_request(user_info, url):
    async with httpx.AsyncClient() as client:
        response = await client.post(url, content=json.dumps(user_info))

    return {
        "status_code": response.status_code,
        "detail": response.json().get(
            "detail", "Empty"
        ),  # "Empty" нужен для ответов, в которых нет поля "detail", чтобы бот не падал с ошибкой
    }


async def _send_code(user_info):
    return await _make_request(user_info, SEND_CODE_URL)


async def _create_user(user_info):
    return await _make_request(user_info, CREATE_USER_URL)
