# Example Tests

Below are example test cases demonstrating BDD-style usage with this framework:

## Swagger API add pet test

Uses a dataprovider with 4 random pets.

Requires live Swagger API at <https://petstore.swagger.io/v2/>
```python
--8<-- "swagger_petstore_tests.py:func"
```

## Mocked Swagger API add pet test

Defines expected requests and then same test flow as above.
```python
--8<-- "swagger_petstore_mocked_tests.py:func"
```

## TerminalX (UI) search test (Selenium/Playwright)

Requires live <https://www.terminalx.com>

The code is similar for Selenium and Playwright.
```python
--8<-- "terminalx_tests.py:func"
```

The only difference is in the test class declaration.
```python
--8<-- "terminalx_tests.py:class_header"
```
versus
```python
--8<-- "pw_terminalx_tests.py:class_header"
```

### Example of overriding the default `setup_method`

For Selenium:
```python
--8<-- "terminalx_tests.py:setup_method"
```
In this case, it checks if `browser_type` is firefox. This can be set
temporarily via command line, like:
```bash
pytest --config selenium:browser_type=firefox qa-pytest-examples/tests/terminalx_tests.py::TerminalXTests
```

For Playwright:
```python
--8<-- "pw_terminalx_tests.py:setup_method"
```

More details in [Architecture TerminalX Configuration](architecture.md#the-configuration) section.

---
