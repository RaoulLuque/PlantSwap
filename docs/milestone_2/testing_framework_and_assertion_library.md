# Testing framework

As testing framework I chose [pytest](https://docs.pytest.org/en/stable/). One of the reasons being the [recommendation](https://fastapi.tiangolo.com/tutorial/testing/) of FastAPI to use pytest as testing framework. It seamlessly works with FastAPI and its dependency injection system to easily handle sessions and headers when testing APIs. This is further supported by the [fixtures](https://docs.pytest.org/en/stable/explanation/fixtures.html) feature of pytest.

In comparison to the standard library unit testing option unittest, pytest has a way more concise and human-readable syntax whereas writing unittests with unittest is notoriously tedious due to verbosity and large amounts of boilerplate code. Additionally, pytest natively runs the tests multithreaded while unittest does not support this out-of-the-box.

With similar reasoning I chose to go for TDD (test-driven-development) instead of BDD (behaviour-driven-development) for now. Test-driven-development and therefore unittests offer a fine-grained approach at testing functions by themselves and at the same time integration tests by testing entire API endpoints. This, and the small learning curve as well as conciseness of tests and ease of writing (of unittests) led me to the decision of not using BDD tests for now. Fortunately, behaviour driven tests can still be added in the future to possibly achieve a more user-oriented testing experience.

To come to the above conclusion, I looked at the python framework [behave](https://github.com/behave/behave) with similarities to [cucumber](https://cucumber.io/), the most prominent BDD framework (cucumber itself does not support python).

## Assertion library
Pytest conveniently uses the assert statements from the python standard library so no further setup was necessary since the assert statement is automatically imported into every python file.

## Setup of testing framework

Setting up pytest is as easy as installing it via pip or in this case uv:
```commandline
uv add pytest
```
Pytest will then automatically discover test functions that are named `test_*` in the project directory.

In order to create test reports and have an overview of the test coverage, [pytest-cov](https://github.com/pytest-dev/pytest-cov) was also added as a dev dependency and several pytest flags were set in the [pyproject.toml](../../pyproject.toml) file:

```toml
[tool.pytest.ini_options]
minversion = "6.0"
addopts = """
--doctest-modules --junitxml=reports/test-results.xml
--cov=app --cov-report=xml:reports/coverage-summary.xml
--cov-report=html:reports/html_dir
--cov-report=lcov:reports/lcov.info
--cov-report term-missing
"""
testpaths = [
    "app/tests",
]
```
These options automatically create different test and coverage reports in different formats and displays a coverage report in the terminal. We also set the test discovery paths in `testpaths` according to our project structure.

In addition to pytest-cov two other plugins were used, namely [pytest-mock](https://github.com/pytest-dev/pytest-mock) which is a wrapper around the [unittest.mock](https://docs.python.org/3/library/unittest.mock.html) standard library module, that simplifies the usage of mock with pytest, and [pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio) for testing of async functions.
