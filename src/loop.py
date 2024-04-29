import asyncio
from driver import get_driver
from settings import get_settings
from enum import Enum
import logging as log
from selenium.webdriver.common.by import By
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import event
import sys


def start() -> None:
    '''
    Started app loop.
    '''
    asyncio.run(_run())


class _PageState(Enum):
    LOGIN_REQUIRED = 1,
    BOOKING_ACTIVE = 2,
    BOOKING_INACTIVE = 3
    UNKNOWN = 4


async def _run() -> None:
    log.info('Loop started.')

    driver = get_driver()
    state = _load_page(driver, get_settings().devices_href)

    while True:
        await _next(driver, state)
        await asyncio.sleep(get_settings().page_live_time)
        state = _update_page(driver)


async def _next(driver, state):
    '''
    Runs next page iteration.
    '''
    match state:
        case _PageState.LOGIN_REQUIRED:
            try:
                event.login(driver)
            except Exception as e:
                log.critical(f'Login failed: {e}')
            await _next(driver, _validate_page_state(driver))
        case _PageState.BOOKING_ACTIVE:
            pass
        case _PageState.BOOKING_INACTIVE:
            pass
        case _PageState.UNKNOWN:
            log.critical('Unknown page state!')
            sys.exit(1)


def _load_page(driver: Firefox, href: str) -> None:
    '''
    Loads page.

    - Returns page state.
    '''
    try:
        driver.get(href)
    except Exception as e:
        log.critical(f"Can't load page: {e}")
        sys.exit(1)
    log.info('Page loaded')
    return _validate_page_state(driver)


def _update_page(driver: Firefox) -> _PageState:
    '''
    Updates page.

    - Returns page state.
    '''
    try:
        driver.refresh()
    except Exception as e:
        log.critical(f"Can't update page: {e}")
        sys.exit(1)
    log.info('Page reloaded.')
    return _validate_page_state(driver)


def _validate_page_state(driver: Firefox) -> _PageState:
    '''
    Validates current page state.

    - Returns current `_PageState`.
    '''
    if driver.title == 'Вход':
        return _PageState.LOGIN_REQUIRED
    elif driver.title == 'Бронирование':
        devices = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'device'))
        )
        for device in devices:
            panel = device.find_element(By.CLASS_NAME, 'panel-body-inside')
            button = panel.find_element(By.TAG_NAME, 'button')
            if button.text == 'Отменить бронь':
                return _PageState.BOOKING_ACTIVE
        return _PageState.BOOKING_INACTIVE

    return _PageState.UNKNOWN
