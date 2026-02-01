# Switching from Selenium to Playwright

Thanks to the backend-agnostic design, switching tests from Selenium to Playwright requires minimal changes:

## 1. Update Base Classes

**From Selenium:**
```python
from qa_pytest_webdriver import SeleniumTests, SeleniumConfiguration

class MyTests(SeleniumTests[MySteps[MyConfiguration], MyConfiguration]):
    pass

class MyConfiguration(SeleniumConfiguration):
    pass
```

**To Playwright:**
```python
from qa_pytest_playwright import PlaywrightTests, PlaywrightConfiguration

class MyTests(PlaywrightTests[MySteps[MyConfiguration], MyConfiguration]):
    pass

class MyConfiguration(PlaywrightConfiguration):
    pass
```

## 2. Update Configuration Files

The configuration file structure remains the same:
- Section name: `[ui]`
- Entry point: `entry_point = <your-url>`

Both Selenium and Playwright use the same configuration section names and settings.
Browser-specific settings (if any) are handled by the respective base classes.

## 3. Test Steps Remain the Same

Because steps use the backend-agnostic `UiContext` and `UiElement` protocols from `qa-pytest-commons`, **your test logic doesn't need to change**:

```python
(self.steps
    .given.ui_context(page)
    ._and.at("https://example.com")
    .when.clicking(By.id("login"))
    .then.the_element(By.css_selector("welcome"), ...))
```

## 4. Install Playwright Browsers

Don't forget to install browsers:
```bash
pdm run playwright-install
```

## Examples

See [qa-pytest-examples](https://github.com/QA-Automation-Starter/qa-automation-python/tree/main/qa-pytest-examples) for complete examples comparing:
- Selenium: [terminalx_tests.py](https://github.com/QA-Automation-Starter/qa-automation-python/blob/main/qa-pytest-examples/tests/terminalx_tests.py)
- Playwright: [pw_terminalx_tests.py](https://github.com/QA-Automation-Starter/qa-automation-python/blob/main/qa-pytest-examples/tests/pw_terminalx_tests.py)

Both implementations demonstrate the same test flow using different backends.

---
