from functools import lru_cache
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options


@lru_cache
def get_driver() -> Firefox:
    options = Options()
    options.add_argument("--headless")
    driver = Firefox(options=options)
    return driver
