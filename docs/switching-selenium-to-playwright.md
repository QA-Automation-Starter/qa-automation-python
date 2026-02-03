# Switching from Selenium to Playwright

Thanks to the backend-agnostic design, switching tests from Selenium to Playwright is straightforward. Both backends use the same `UiConfiguration` and test logic remains identical.

## What Changes

### 1. Test Base Class

Simply change the base class import and inheritance:

**From:**
```python
from qa_pytest_webdriver import SeleniumTests

class MyTests(SeleniumTests[MySteps[MyConfiguration], MyConfiguration]):
    ...
```

**To:**
```python
from qa_pytest_playwright import PlaywrightTests

class MyTests(PlaywrightTests[MySteps[MyConfiguration], MyConfiguration]):
    ...
```

### 2. Browser Setup (If Customized)

If you overrode `setup_method()` for custom browser configuration, update the backend-specific code:

**Selenium Example:**
```python
class MyTests(SeleniumTests[...]):
    @override
    def setup_method(self):
        from selenium.webdriver import Firefox
        from selenium.webdriver.firefox.options import Options
        from selenium.webdriver.firefox.service import Service
        from webdriver_manager.firefox import GeckoDriverManager
        
        super().setup_method()
        options = Options()
        options.add_argument("--start-maximized")
        service = Service(GeckoDriverManager().install())
        self._web_driver = Firefox(options=options, service=service)
```

**Playwright Equivalent:**
```python
class MyTests(PlaywrightTests[...]):
    @override
    def setup_method(self):
        from playwright.sync_api import sync_playwright
        
        super().setup_method()
        self._playwright = sync_playwright().start()
        self._browser = self._playwright.firefox.launch(headless=False)
        self._page = self._browser.new_page(viewport={"width": 1920, "height": 1080})
```

### 3. Install Playwright Browsers

Don't forget to install browsers:
```bash
pdm run playwright-install
```

## What Doesn't Change

- **Configuration files** - Same `[ui]` section, same `entry_point`
- **Test logic** - All step definitions work identically
- **Configuration class** - Both use `UiConfiguration`

## Examples

See [qa-pytest-examples](https://github.com/QA-Automation-Starter/qa-automation-python/tree/main/qa-pytest-examples) comparing:
- Selenium: [terminalx_tests.py](https://github.com/QA-Automation-Starter/qa-automation-python/blob/main/qa-pytest-examples/tests/terminalx_tests.py)
- Playwright: [pw_terminalx_tests.py](https://github.com/QA-Automation-Starter/qa-automation-python/blob/main/qa-pytest-examples/tests/pw_terminalx_tests.py)

Both demonstrate identical test flows using different backends.

---
