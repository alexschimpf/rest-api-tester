# Python REST API Tester

## Installation
`pip install rest-api-tester`
- This is available for Python3.7+

## About
`rest-api-tester` makes it easy to create REST API tests for your APIs.
Though this tool is written in Python, your APIs need not be. This library provides a consistent way to write API tests 
and perform the necessary validation. It is primarily built to handle traditional, JSON-based APIs, although it has
the ability to handle other API formats. Also... `rest-api-tester` can auto-update your expectation files for you when 
tests fail!

## Tutorial

1. Create a test cases file named `__data__/test_something.json`
```json
{
    "create_something": {
        "url": "/something",
        "method": "POST",
        "status": 200,
        "request": {
            "name": "something"
        },
        "response": {
            "id": 1,
            "name": "something"
        }
    }
}
```

2. Create a unit test class
```python
from rest_api_tester.test import TestCase

class TestSomething(TestCase):
    ...
```

3. Set up your test case runner
```python
import os
from rest_api_tester.client import TestClient
from rest_api_tester.test import TestCase
from rest_api_tester.runner import TestCaseRunner

class TestSomething(TestCase):
    
    def setUp(self) -> None:
        test_client = TestClient(base_url='https://myapp.com:5000')
        path_to_data = os.path.join(os.path.dirname(__file__), '__data__')
        self.runner = TestCaseRunner(
            client=test_client,
            path_to_data=path_to_data,
            default_content_type='application/json'
        )
```

4. Create your first API test
```python
class TestSomething(TestCase):
    
    ...

    def test_create_something(self) -> None:
        result = self.runner.run(
            path_to_test_cases='test_something.json',
            test_name='create_something'
        )
        self.verify_test_result(result=result)
```

5. Add a more complicated test
```json
{
    "update_something": {
        "url": "/something/{id}",
        "method": "PUT",
        "status": 200,
        "request": {
            "name": "something",
            "alias": "$$$"
        },
        "response": {
            "id": "$$$",
            "name": "something",
            "alias": "$$$",
            "created_date": "$$$"
        }
    }
}
```
```python
import datetime

class TestSomething(TestCase):
    
    ...

    def test_update_something(self) -> None:
        new_alias = 'something_else'
        something_id = create_something()  # assume this function already exists
        result = self.runner.run(
            path_to_test_cases='test_something.json',
            test_name='update_something',
            # Fill in URL variables at runtime
            url_params={'id': something_id},
            # Modify request data at runtime
            request_json_modifiers={
              'alias': new_alias
            },
            # Modify expected response data at runtime
            response_json_modifiers={
              'id': something_id,
              'alias': new_alias,
              'created_date': str(datetime.datetime.now().date())
            }
        )
        self.verify_test_result(
          result=result,
          # Exclude some response fields from validation
          excluded_response_paths=[
            'some_response_field_i_can_ignore'
          ]
        )
```

## Details
- TODO

## Not Supported
- File uploads
- SOAP
- Websockets

## Examples
- You can find more advanced API test examples [here](https://github.com/alexschimpf/python-rest-api-tester/tree/main/tests/api).
- Note: The examples provided are run against a FastAPI server, and thus need Python3.7+ to run.