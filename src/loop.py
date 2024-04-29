import asyncio
from driver import get_driver
from settings import get_settings
from enum import Enum
import logging as log
from selenium.webdriver import Firefox
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
    BOOKING_AVAILABLE = 3
    BOOKING_UNAVAILABLE = 4
    UNKNOWN = 5


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
                sys.exit(1)
            await _next(driver, _validate_page_state(driver))

        case _PageState.BOOKING_ACTIVE:
            pass

        case _PageState.BOOKING_AVAILABLE:
            try:
                event.book(driver)
            except Exception as e:
                log.critical(f'Book failed: {e}')
                sys.exit(1)

        case _PageState.BOOKING_UNAVAILABLE:
            await asyncio.sleep(get_settings().book_wait)
            await _next(driver, _update_page(driver))

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
        buttons = event.get_devices_buttons(driver)

        for button in buttons:
            if button.text == 'Отменить бронь':
                return _PageState.BOOKING_ACTIVE
            elif button.text == 'Забронировать':
                return _PageState.BOOKING_AVAILABLE
        return _PageState.BOOKING_UNAVAILABLE

    return _PageState.UNKNOWN
