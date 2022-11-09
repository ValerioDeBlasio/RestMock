from typing import List

from fastapi import FastAPI, Request
import json
import os

from pydantic import parse_obj_as

from load_api import load_api, extract_response
from logger_config import LOG_CONFIG
from model import ApiMockModel

import logging.config
## init loggin
logging.config.dictConfig(LOG_CONFIG)

## load api json file and convert it into list of pydantic model
api_json_file = os.path.join(os.path.dirname(__file__), "api.json")
api_json = json.load(open(api_json_file))
items = parse_obj_as(List[ApiMockModel], api_json)

## normalize and apply
endpoint_mapping = load_api(items)
app = FastAPI()

## The endpoint will capture all incoming requests
@app.get("/{full_path:path}")
async def get(request: Request):
    return await extract_response(endpoint_mapping.get('GET'), request)


@app.post("/{full_path:path}")
async def post(request: Request):
    return await extract_response(endpoint_mapping.get('POST'), request)


@app.put("/{full_path:path}")
async def put(request: Request):
    return await extract_response(endpoint_mapping.get('PUT'), request)


@app.delete("/{full_path:path}")
async def delete(request: Request):
    return await extract_response(endpoint_mapping.get('DELETE'), request)
