# Example Tests

Below are example test cases demonstrating BDD-style usage with this framework:

## Swagger API add pet test

Uses a dataprovider with 4 random pets.

Requires live Swagger API at https://petstore.swagger.io/v2/
```python
--8<-- "swagger_petstore_tests.py:func"
```

## Mocked Swagger API add pet test

Defines expected requests and then same test flow as above.
```python
--8<-- "swagger_petstore_mocked_tests.py:func"
```

## TerminalX (UI) search test

Requires live https://www.terminalx.com
```python
--8<-- "terminalx_tests.py:func"
```
---
