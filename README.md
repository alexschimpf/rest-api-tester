# Python REST API Tester

## Installation
`pip install rest-api-tester`

## About
`rest-api-tester` makes it easy to create REST API tests for your APIs.
Though this tool is written in Python, your APIs need not be!

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

## Other Details
- There is a JSON file parser provided out of the box that can be used to parse JSON test case files
  - If needed, you can write your own parser for another format... this is quite trivial
  - Your custom parser function should be provided as an argument to `TestCaseRunner.run`
- Requests and responses can be referenced as an external file as shown [here](https://github.com/alexschimpf/python-rest-api-tester/blob/main/tests/api/json/__data__/test_json.json#L88)
  - The file path is relative to `TestCaseRunner.path_to_data`
- Test case data can be augmented dynamically before tests are run and also before test results are verified
  - `TestCaseRunner.run` returns a `TestResult` object. You can then use `TestCase.verify_test_result` to verify the result is as expected
  - Before `TestCase.verify_test_result` is called, you can modify the `TestResult` object, if needed
  - If you need to modify the test case data before the test is run, you can use the `test_data_modifier` argument of `TestCaseRunner.run`
    - This is a convenient place to programmatically add authentication data to your test case requests
- `TestCaseRunner` needs a `client` provided so that it can make requests to your API
  - There is a `TestClient` class provided out of the box, which makes simple HTTP requests to your API using the `requests` library
  - If you need something more custom, you can create your own class that extends from `BaseTestClient`
- `TestCase.verify_test_result` uses a [simple verifier](https://github.com/alexschimpf/python-rest-api-tester/blob/main/rest_api_tester/test.py#L77) by default
  - If you need something more custom, the verifier can be overridden by using the `verifier` argument

## Not Supported
- File uploads
- SOAP
- Websockets

## Examples
You can find more advanced API test examples [here](https://github.com/alexschimpf/python-rest-api-tester/tree/main/tests/api).


