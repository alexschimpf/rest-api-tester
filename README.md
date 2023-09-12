# Python REST API Tester

## Installation
`pip install rest-api-tester`
- This is available for Python3.7+

## About
`rest-api-tester` makes it easy to create REST API tests for your APIs.
Though this tool is written in Python, your APIs need not be. This library provides a consistent way to write API tests
and perform the necessary validation. It is primarily built to handle traditional, JSON-based APIs, although it has
the ability to handle other API formats. Also... `rest-api-tester` can auto-update your scenario files for you when
tests fail!

## Tutorial

1. Create a test cases file named `__scenarios__/test_something.json`
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
        path_to_scenarios_dir = os.path.join(os.path.dirname(__file__), '__scenarios__')
        self.runner = TestCaseRunner(
            client=test_client,
            path_to_scenarios_dir=path_to_scenarios_dir,
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
            url_params={
                'id': something_id
            },
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

## Summary
`rest-api-tester` makes API testing easier for APIs based on JSON and plain-text formats.

### Scenario Files
Test scenarios are written in external files.
A scenario specifies the request to be made and expected response details (i.e. content, headers, and status).

### API Client
You must implement your own client as a subclass of `rest_api_tester.client.base_client.BaseClient` to make the API requests.
See [here](https://github.com/alexschimpf/python-rest-api-tester/tree/main/tests/api/fastapi/fastapi_test_client.py) for an example.

### Test Case Runner
To run your test cases, you must use `rest_api_tester.runner.TestCaseRunner`.
This class parses your test scenario files and uses your client implementation to make the necessary API requests.
A JSON parser is provided as a default to parse your test scenario files.
A scenario files can contain one or more test scenarios, each with a specific key that can be referenced in code.
Custom parsers can be created and passed to `TestCaseRunner`.

### Test Case
All test cases are built upon python's `unittest`. Your test case classes should inherit from `rest_api_tester.test.TestCase`.
This base class provides the functionality to verify test results from `rest_api_tester.runner.TestCaseRunner`.
To do this, you will pass the test results from `TestCaseRunner` to `TestCase.verify_test_result`.
The default response content verifier should work for most cases, but a custom verifier function can be used via the `verifier` param.

### Modifying Scenarios at Runtime
In many instances, URLs, request data, and expected response data need to be modified at runtime.
For example, you may create an entity, but its ID or creation date are not known until runtime.
Another use case is authentication. For example, you may generate a login cookie at runtime, which can be used to augment your request.
Thus, your test scenarios need to be augmented. `rest-api-tester` offers various ways to handle such cases.

1. You can modify scenario URLs at runtime by using `url_params` from `TestCaseRunner.run`.
    - If your URL is `/something/{id}`, you can use `url_params={'id': 123}` to substitute `123` in for `{id}`.
2. You can modify your scenario request JSON data at runtime by using `request_json_modifiers` from `TestCaseRunner.run`.
    - You can provide a dict of JSON paths and, for each, a value.
    - The JSON path format supported is a simple one that can be easily understood via the test cases [here](https://github.com/alexschimpf/python-rest-api-tester/tree/main/tests/unit/test_utils.py).
    - Note that this is similar but not quite the same as JsonPath expressions (e.g. https://github.com/json-path/JsonPath)
    - For example, `{'a.[1].b.*c': 3}` will modify set `item['c'] = 3` for all items of `request_json['a'][1]['b']`.
3. Similarly, you can modify your scenario expected response JSON data at runtime by using `response_json_modifiers` from `TestCaseRunner.run`.
4. If you want to exclude some response fields from verification, you can use `excluded_response_paths` from `TestCase.verify_test_result`
   - This will be a list of the same kind of JSON paths from `request_json_modifiers` and `response_json_modifiers`.
   - This can be useful if certain fields from the response can't be easily known at runtime.
5. If you'd like more fine-grained, programmatic control over test scenario data before a test is actually run, you can use `test_data_modifier` from `TestCaseRunner.run`.
    - This requires passing a function which accepts a `TestData` parameter and returns the modified `TestData`.
    - The `TestData` object contains all the parsed test scenario data before the test has been executed (i.e. the client has made an API call).
    - This can be used to add authentication headers/cookies that may not be known until runtime.

### Auto-updating Scenario Files on Fail
`rest-api-tester` can also auto-update your scenario files for you when tests fail.
For example, if you run your tests, but your response data does not match, `rest-api-tester` can automatically update the scenario's expected response details based on what the actual API response was.
This can be done in one of the following ways:
- Setting `rest_api_tester.config.Config.UPDATE_SCENARIOS_ON_FAIL = true`.
- Setting `self.update_scenarios_on_fail = True` in `TestCase.setup`.
- Passing `update_scenarios_on_fail = True` in `TestCase.verify_test_result`

<b>Please note that scenario files can become corrupted if tests run in parallel and update the same file.
Corruption can also happen if the tests are force-killed in the middle of writing to scenario files.</b>

## Not Supported
- APIs based on data formats other than JSON and plain text
  - It's possible other formats could be used, but it would likely require more workaround and effort
- File uploads
- SOAP
- Websockets
- RPC

## Examples
- You can find more advanced API test examples [here](https://github.com/alexschimpf/python-rest-api-tester/tree/main/tests/api).
- Note: The examples provided are run against a FastAPI server, and thus need Python3.7+ to run.
