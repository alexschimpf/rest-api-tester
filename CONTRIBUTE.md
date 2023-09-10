## Issues
1. Make sure your issue hasn't already been submitted.
2. Make sure to fill out the issue template with all necessary details.

## Pull Requests
- All necessary checks are run on pull requests
  - PR title format check
  - EOF newline check
  - Linting
  - Python type-checking
  - Unit tests
  - API tests
- All checks must pass before merging
- All pull requests will be squashed and merged
- All pull requests with code changes should contain tests or updates to existing tests
  - Exceptions are possible with a sufficient reason
- Pull request titles must have one of the following prefixes:
  - "breaking: "
    - Indicates the introduction of a breaking change
    - Results in a major version increment
  - "feat: "
    - Indicates a new feature
    - Results in a minor version increment
  - "fix: "
    - Indicates a bug fix
    - Results in a patch version increment
  - "perf: "
    - Indicates a performance improvement
    - Results in a patch version increment
  - "refactor: "
    - Indicates that refactoring has been
    - Results in a patch version increment
  - "no-release: "
    - Indicates changes that require no release
    - This will not result in a new release / version increment
    - Examples include (but are not limited to):
      - README updates
      - Changes related to dev environment (e.g. new Make commands, dev tooling, etc.)

## Local Development

### Installation
1. Install python >=3.7
2. Create a python virtual environment
3. Install python dependencies
```shell
make install-dev
```
4. Install linter commit hook
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
