# RestMock
RestMock is a simple and light service, written in Python with FastAPI, which allows you to create a mock API service via REST interface.
This allows you to test your application without needing to have the actual API server.

### Configuration
The configuration is done through `api.json`, in which all the various endpoints (with their parameters) and the expected responses are defined.

This is an example of an endpoint
```yaml
{
    "method": "POST", // could be also GET, PUT, DELETE
    "endpoint": "/{param_1}/{param_2}/clone", // path_params must be included between {}
    "path_params": {
      "param_1": "1",
      "param_2": "test"
    },
    "query_params": {
      "ids": ["abd", "csf"], // could be string or list
      "org_id": "organization"
    },
    "body": { // body should be a valid json
        "field_1": "field_1",
        "field_2": {
            "subfield": "subfield"
        },
        "field_3": ["field_3_value"]
    },
    "response": {
      "data": "response_example"
    },
    "response_code": 200
  }
```


## Quick start
The service can be run directly through Python

```bash
pip install -r requirements

gunicorn --bind 0.0.0.0:5000 -k uvicorn.workers.UvicornWorker main:app
```

It is possible to run the service via docker image

```bash
docker build -t restmock .

# should pass the api.json file when running the service
docker run -p 5000:5000 --mount type=bind,source="$(pwd)"/api.json,target=/usr/app/api.json,readonly  restmock
```



