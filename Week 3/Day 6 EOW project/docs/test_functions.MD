# Testing functions

## Concepts/keywords/Functions
- How to run tests
- pytest.fixture
- patch()
- MagicMock(), Mock()
- create_autospec()
- capsys, capsys.readouterr()
- assert_called, assert_called_once, assert_called_once_with
- pytest.raises()
- mock_function.call_args

## Learn
1. Running tests:   
    ```bash
    pytest <test_file_name> # to run tests from a single file 
    pytest # runs tests that starts with test_ name or the files defined in pytest.ini file 
    pytest <test_file_name> -v # to run tests from a single file with verbos(more printed stuff) 
    pytest <test_file_name> -s # to run tests from a single file along with the printed outputs on console 
    ```

2. pytest.fixture:
    A reusable function that provides setup data or objects for tests.
    [fixture example](../test/conftest.py)

3. [MagicMock(), Mock()](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock)

4. create_autospec(): used to create a mock object for a fucntion. [example -> Line: 75](../test/test_main.py)

5. capsys, capsys.readouterr(): 
    - capsys is parameter to use in a test function
    - capsys.readouterr() is the funtion that gets all the printed outputs within a test funtion.
    [example -> Line: 95](../test/test_main.py)

6. assert_called, assert_called_once, assert_called_once_with:
    funtions to test(assert) calling of other funtions

7. pytest.raises(): used to assert exceptions
    [example -> Line: 63](../test/test_model.py)

8. mock_funtion.call_args:
    - Contains the arguments passed to a mock function (mock_funtion)
    [example -> Line: 29](../test/test_main.py)

## Best Practices
1. Running Tests
- Keep tests small and focused so they run quickly.
- Use `-v` for better visibility when diagnosing failures.
- Use `-k` to run specific tests during development.
- Avoid depending on print statements; prefer assertions.
- Configure `pytest.ini` to control test discovery and markers.

---

2. pytest.fixture
- Use fixtures for repeated setup to avoid duplication.
- Keep fixtures simple; avoid complex logic inside them.
- Scope fixtures appropriately (`function`, `module`, `session`) to speed up test execution.
- Place shared fixtures in `conftest.py` for automatic availability.
- Name fixtures descriptively based on what they provide.

---
 3. MagicMock() and Mock()
- Mock only external dependencies, not your own logic.
- Use `Mock()` for simple mocks; use `MagicMock()` when magic methods are needed.
- Always assert expected behavior on mocks (`assert_called_once`, etc.).
- Avoid over-mocking; too many mocks hide real issues.
- Set explicit return values to avoid unexpected behavior.

---
 4. create_autospec()
- Use `create_autospec()` to enforce function signatures.
- Prefer `autospec=True` when mocking large modules or classes.
- Helps catch bugs where the system under test calls a function with wrong arguments.
- Use it when mocking your own application code to ensure correctness.

---
5. capsys and capsys.readouterr()
- Use `capsys` for capturing print output instead of modifying the code.
- Call `capsys.readouterr()` only after the print-producing action.
- Avoid mixing `capsys` with logging capture unless necessary.
- Do not capture output in tests unless the output is part of the behavior being tested.

---
6. assert_called, assert_called_once, assert_called_once_with
- Always assert calls when testing function interactions.
- Use `assert_called_once_with()` to validate exact parameters.
- Use `assert_not_called()` to ensure a function was not triggered.
- Avoid asserting internal implementation details unless necessary.

---
7. pytest.raises()
- Use `pytest.raises()` to test predictable exceptions.
- Always assert the exact exception type.
- Prefer the context manager form for clarity.
- Optionally inspect the exception message using `match=` to avoid false positives.

---
8. mock_function.call_args
- Use `call_args` to introspect arguments passed to mocks.
- Prefer `call_args_list` when multiple calls are expected.
- Validate both positional (`args`) and keyword (`kwargs`) arguments.
- Use this when you cannot or do not want to use `assert_called_with()` directly.


### Resources
[pytest documentation](https://docs.python.org/3/contents.html)
