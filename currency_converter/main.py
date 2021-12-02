from aiohttp.web_request import Request
from aiohttp.web_response import Response
from aiohttp.web import Application, run_app, json_response
from app.helpers.help import is_float
from app.redis_database.redis_data import upload, convert
from typing import Dict
from app.exceptions.exceptions import ValueErrorRequest


async def converted(request: Request) -> Response:
    try:
        if 'from' not in request.query:
            raise ValueErrorRequest('from', 'not found')
        if not request.query['from'].isalpha():
            raise ValueErrorRequest(request.query['from'], "must be a string consisting of letters")
        from_: str = request.query['from']
        if 'to' not in request.query:
            raise ValueErrorRequest('to', 'not found')
        if not request.query['to'].isalpha():
            raise ValueErrorRequest(request.query['to'], "must be a string consisting of letters")
        to: str = request.query['to']
        if 'amount' not in request.query:
            raise ValueErrorRequest('amount', 'not found')
        amount = float(request.query['amount'])
        value: float = await convert(from_, to, amount)
        response_obj: Dict[str, str] = {'amount': str(value)}
        return json_response(response_obj, status=200)
    except ValueErrorRequest as e:
        response_obj: Dict[str, str] = {'message': str(e)}
        print(str(e))
        return json_response(response_obj, status=400)
    except ValueError as e:
        response_obj: Dict[str, str] = {'message': str(e)}
        return json_response(response_obj, status=400)
    except ConnectionRefusedError as e:
        response_obj: Dict[str, str] = {'message': str(e)}
        return json_response(response_obj, status=500)
    except Exception as e:
        response_obj: Dict[str, str] = {'message': str(e)}
        print(type(e))
        return json_response(response_obj, status=500)


async def database(request: Request) -> Response:
    try:
        data: Dict[str, str] = dict(await request.post())
        for key, value in data.items():
            if not key.isalpha():
                raise ValueErrorRequest(key, "must be a string consisting of letters")
            if not is_float(value):
                raise ValueErrorRequest(value, "must be a float")
        await upload(data, request.query['merge'] == '1')
        return json_response({'status': 'ok'}, status=201)
    except ConnectionRefusedError as e:
        response_obj: Dict[str, str] = {'message': str(e)}
        return json_response(response_obj, status=500)
    except Exception as e:
        response_obj: Dict[str, str] = {'status': 'fail', 'message': str(e)}
        print(type(e))
        return json_response(response_obj, status=500)


if __name__ == '__main__':
    app = Application()
    app.router.add_get('/convert', converted)
    app.router.add_post('/database', database)
    run_app(app)
