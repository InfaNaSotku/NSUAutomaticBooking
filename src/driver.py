from functools import lru_cache
from selenium.webdriver import Firefox


@lru_cache
def get_driver() -> Firefox:
    driver = Firefox()
    return driver
