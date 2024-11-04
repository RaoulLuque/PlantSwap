# Writing tests

One benefit of using FastAPI as the framework for designing our api is the easy testing. Basic test setup is explained on [this page](https://fastapi.tiangolo.com/tutorial/testing/) of the FastAPI documentation. Basically a `TestClient` instance can be created which can then send test requests to your API handling all the dependencies that might be necessary. The responses can then be checked. This is shown in the following code snippet taken from [test_main.py](../../app/tests/api/test_main.py)

```python
from fastapi.testclient import TestClient

def test_read_main(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World!"}
```
As can be seen, the TestClient itself is again inserted into the test with the dependency injection system handled by FastAPI.

## Pytest fixtures

To test more involved api endpoints pytest [fixtures](https://docs.pytest.org/en/stable/explanation/fixtures.html) which basically also inject dependencies. In the code snippet below (taken from [test_users.py](../../app/tests/api/routers/test_users.py), the `superuser_token_headers` was defined as a fixture in [conftest.py](../../app/tests/conftest.py)

```python
def test_read_users_me_superuser(
        client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.get("/users/me", headers=superuser_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"]
    assert current_user["email"] == settings.FIRST_SUPERUSER
```

## Async testing and mocking

Sometimes one might not only test api endpoints but instead test functions directly. This is of course also possible. In our case, a lot of the functions our api endpoints depend on are asynchronous though. Therefore we used the [pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio) pytest plugin which allows testing of async functions.

The following is an example test taken from [test_dependencies.py](../../app/tests/api/test_dependencies.py).

```python
@pytest.mark.asyncio
async def test_get_current_user():
    mocked_jwt_payload = {
        "sub": None
    }

    with patch("jwt.decode", return_value=mocked_jwt_payload):
        with pytest.raises(HTTPException) as exception_info:
            await get_current_user(None, None)  # Call asynchronous function
        response = exception_info.value
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.detail == "Could not validate credentials"
        assert response.headers == {"WWW-Authenticate": "Bearer"}
```

The `@pytest.mark.asyncio` decorator above the function indicates that the test tests and asynchronous function. The call of the asynchronous function is highlighted with a comment.

There is however more to be explained in the above code snippet. We are also mocking the `jwt.decode` function, which is a dependency imported and used by the `get_current_user` function. Mocking in this case describes the process of recreating an object that occurs in production with the goal of being able to control the specific behaviour of the object while still maintaining the properties that the object has at runtime. In this case we are mocking the `decode` function from the `jwt` package and telling it to instead of what it would usually do, return `mocked_jwt_payload`. This saves us some time trying to create situations where edge cases might happen and instead allows us to enforce these edge cases and test them directly.

## Current state of testing
As of writing this documentation, the test coverage of the entire codebase is 99% which is sufficient by most standards. The rest 1% can be achieved by writing elaborate tests that test edge cases such as inactive users trying to log in which with the current API logic is technically impossible to happen since all users are created as active users and there is no way to change this attribute. Of course, code coverage should not be the only metric that one measures the test quality by.

