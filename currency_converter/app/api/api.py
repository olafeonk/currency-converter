from ..database.redis import upload, convert
from typing import Dict,
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from aiohttp.web import json_response
from ..helpers.handlers_exceptions import correct_data, get_query
from ..exceptions import RequestError


async def converted(request: Request) -> Response:
    try:
        from_, to, amount = get_query(request.query)
        value: float = await convert(from_, to, amount)
        response_obj: Dict[str, str] = {'amount': str(value)}
    except RequestError as e:
        response_obj: Dict[str, str] = {'message': str(e)}
        return json_response(response_obj, status=400)
    except Exception as e:
        response_obj: Dict[str, str] = {'message': str(e)}
        return json_response(response_obj, status=500)
    else:
        return json_response(response_obj, status=200)


async def database(request: Request) -> Response:
    try:
        data: Dict[str, str] = dict(await request.post())
        correct_data(data)
        await upload(data, request.query['merge'] == '1')
    except RequestError as e:
        response_obj: Dict[str, str] = {'message': str(e)}
        return json_response(response_obj, status=400)
    except Exception as e:
        response_obj: Dict[str, str] = {'status': 'fail', 'message': str(e)}
        return json_response(response_obj, status=500)
    else:
        return json_response({'status': 'ok'}, status=201)
