import datetime
import json

import httpretty
import httpx
import respx

from common.constants import DEBUG_MODE, INTERNAL_SERVER_ERROR_MESSAGE

MOCK_URLS = {
    'https://cheap-payment-gateway/api/v1/availability/': {'data': 'ok', 'status_code': 200},
    'https://cheap-payment-gateway/api/v1/transaction/': {'data': 'ok', 'status_code': 200},
    'https://expensive-payment-gateway/api/v1/availability/': {'data': 'ok', 'status_code': 200},
    'https://expensive-payment-gateway/api/v1/transaction/': {'data': 'ok', 'status_code': 200},
    'https://premium-payment-gateway/api/v1/availability/': {'data': 'ok', 'status_code': 200},
    'https://premium-payment-gateway/api/v1/transaction/': {'data': 'ok', 'status_code': 200},
}


def date_time_json_serialize(date):
    """
    Serialize datetime object to string
    :param date: datetime object
    :return:
    """
    if isinstance(date, datetime.datetime):
        return "{}-{}-{}".format(date.year, date.month, date.day)


async def log_request(request):
    """
    Print the details of request
    :param request:
    :return:
    """
    print(f"Request event hook: {request.method} {request.url} - Waiting for response")
    print(request.headers)
    print(request.read())


async def log_response(response):
    """
    Print the details of response
    :param response:
    :return:
    """
    request = response.request
    print(f"Response event hook: {request.method} {request.url} - Status {response.status_code}")
    print(response.json())


@respx.mock
async def make_request(method='get', api_url='', api_key='', data={}, retries=0):
    """
    Make call to external urls using python request
    :param method: get|post (str)
    :param api_url:
    :param api_key:
    :param data: data to send in the request (dict)
    :param retries:
    :return:
    """
    headers = {'content-type': 'application/json'}
    if api_key and isinstance(data, dict):
        data['api_key'] = api_key
    method = method.upper()
    respx.route(method=method, path=api_url).mock(
        return_value=httpx.Response(
            status_code=MOCK_URLS[api_url]['status_code'],
            json=MOCK_URLS[api_url]['data']
        )
    )
    event_hooks = {}
    if DEBUG_MODE:
        event_hooks = {'request': [log_request], 'response': [log_response]}
    async with httpx.AsyncClient(event_hooks=event_hooks) as client:
        try:
            if method == httpretty.GET:
                response = await client.get(api_url, params=data, headers=headers)
            elif method == httpretty.POST:
                response = await client.post(
                    api_url,
                    data=json.dumps(data, default=date_time_json_serialize),
                    headers=headers
                )
            return {'status_code': response.status_code, 'data': response.json()}
        except Exception as exception_occurred:
            if DEBUG_MODE:
                print(exception_occurred)
            return {'status_code': 500, 'data': INTERNAL_SERVER_ERROR_MESSAGE}
