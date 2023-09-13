## Issues
1. Make sure your issue hasn't already been submitted.
2. Make sure to fill out the issue template with all necessary details.

## Pull Requests
- All pull requests should be made against the `main` branch
- All necessary checks are run on pull requests
  - EOF newline check
  - Python linting
  - Python type-checking
  - Unit tests
  - API tests
  - Commit message linting
- All checks must pass before merging
- All pull requests will be rebased onto the main branch
- All pull requests with code changes should contain tests or updates to existing tests
  - Exceptions are possible with a sufficient reason
- Commit messages are linted via [commitlint](https://commitlint.js.org/#/)
    - Make sure to run step 3 below under Installation for this to install properly
    - Commit messages automatically populate the changelog and tags, so they should be clear and readable.
    - Allowed prefixes: breaking, deps, chore, ci, docs, feat, fix, perf, refactor, style, test
    - Commit messages should look like:
        ```
        feat: I made a new feature

        This is where the optional body goes.

        This is where the optional footer goes.
        ```

## Local Development

### Installation
1. Install python >=3.7
2. Create a python virtual environment
3. Install python dependencies
```shell
make install-dev
```
4. Install the python linter commit hook
```shell
make install-linter
```

### Running Tests
```shell
make run-unit-tests
make run-api-tests
make run-tests  # run both unit and api tests with coverage check
```

### Type Checking
- Mypy (in strict mode) is used to type-check this project.
- The "Any" type is discouraged, although sometimes necessary.
- "ignore" directives are also discouraged.

```shell
make type-check
```

### Linting
- Flake8 is used to lint this project.
- This is ideally done via a pre-commit hook. Installation details are mentioned above.
- "# flake8: noqa" directives are discouraged.

Thanks for contributing!
