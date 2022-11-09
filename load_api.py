# ------- #
# Created by: valeriodeblasio with ❤
# Date: Tue 08/11/2022
# Time: 11:25
# ------- #
import json
from typing import Dict, List

from fastapi import Request
from starlette.responses import JSONResponse

from model import ApiMockModel
from deepdiff import DeepDiff


def load_api(api_json: List[ApiMockModel]) -> Dict[str, List[ApiMockModel]]:
    '''
    Given the list of endpoints, it returns a Dict of normalized endpoints grouped by method.
    It will apply standardization such as removing trailing slashes, replace path params, etc.
    :param api_json: List of endpoint
    :return: Dict with method as key and list of normalized endpoints
    '''
    api_mapping: Dict = {}
    for mock in api_json:
        method = mock.method
        endpoints = api_mapping.setdefault(method, [])

        endpoint = mock.endpoint
        if mock.path_params:
            # if path_params are present, it will replace the param with the actual value
            res = []
            for elem in mock.endpoint.split("/"):
                if not elem.startswith('{'):
                    res.append(elem)
                else:
                    res.append(mock.path_params.get(elem[1:-1]))
            endpoint = '/'.join(res)

        ## remove trailing and starting slashes
        if endpoint.startswith('/'):
            endpoint = endpoint[1:]
        if endpoint.endswith('/'):
            endpoint = endpoint[:-1]
        mock.endpoint = endpoint

        endpoints.append(mock)

    return api_mapping


async def extract_response(api_mapping: List[ApiMockModel], request: Request):
    '''
    Given the list of endpoints and the input request, check if the request matches an endpoint.
    If true, it returns the declared response, otherwise it returns a 404
    :param api_mapping:
    :param request:
    :return:
    '''
    if not api_mapping:
        return JSONResponse({}, status_code=404)

    for mock in api_mapping:
        if mock.endpoint != request.path_params['full_path']:
            continue

        ## check on query params
        if mock.query_params:
            valid = True
            for query_param_key, query_param_value in mock.query_params.items():
                ## check if list
                if type(query_param_value) is list:
                    if query_param_key not in request.query_params or \
                            sorted(query_param_value) != sorted(request.query_params.getlist(query_param_key)):
                        valid = False
                        break

                else:
                    if query_param_key not in request.query_params or query_param_value != request.query_params.get(
                            query_param_key):
                        valid = False
                        break
            if not valid:
                continue

        ## check on body
        if mock.body:
            body = json.loads(await request.body())
            if DeepDiff(mock.body, body, ignore_string_case=True):
                continue

        return JSONResponse(mock.response, status_code=mock.response_code or 200)

    return JSONResponse({}, status_code=404)
