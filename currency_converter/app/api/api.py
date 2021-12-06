from ..database.redis import upload, convert
from typing import Dict, Tuple
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from aiohttp.web import json_response
from ..helpers.handlers_exceptions import key_in_query, value_is_letter, value_is_float, correct_data
from ..exceptions import RequestError


def get_query(query) -> Tuple[str, str, float]:
    try:
        key_in_query('from', query)
        key_in_query('to', query)
        key_in_query('amount', query)
        value_is_letter(query['from'])
        value_is_letter(query['to'])
        value_is_float(query['amount'])
    except RequestError:
        raise
    else:
        return query['from'], query['to'], float(query['amount'])


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
