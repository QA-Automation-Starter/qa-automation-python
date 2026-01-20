def should_open_browser():
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://www.terminalx.com")
        assert "TerminalX" in driver.title or "terminalx" in driver.title.lower()
    finally:
        driver.quit()
