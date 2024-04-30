import asyncio
from driver import get_driver
from settings import get_settings
from enum import Enum
from logger import logger as log
from selenium.webdriver import Firefox
import event
import sys


def _start() -> None:
    '''
    Starts app loop.
    '''
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        log.info("Closed successfully!")
        if sys.excepthook is sys.__excepthook__:
            def _no_traceback_excepthook(exc_type, exc_val, traceback):
                pass
            sys.excepthook = _no_traceback_excepthook
        raise


class _PageState(Enum):
    LOGIN_REQUIRED = 1,
    BOOKING_ACTIVE = 2,
    BOOKING_AVAILABLE = 3
    BOOKING_UNAVAILABLE = 4
    UNKNOWN = 5


async def run() -> None:
    '''
    Runs the loop.

    - Warning!
    If you run method directly you need
    run `configure` by hand.
    '''
    log.info('Loop started.')

    driver = get_driver()
    _load_page(driver, get_settings().devices_href)

    while True:
        await _next(driver)
        await asyncio.sleep(get_settings().page_live_time)
        _update_page(driver)


async def _next(driver):
    '''
    Runs next page iteration.
    '''
    state = _validate_page_state(driver)

    match state:
        case _PageState.LOGIN_REQUIRED:
            await _login(driver)

        case _PageState.BOOKING_ACTIVE:
            await _unbook(driver)

        case _PageState.BOOKING_AVAILABLE:
            _book(driver)

        case _PageState.BOOKING_UNAVAILABLE:
            await _wait_until_available(driver)

        case _PageState.UNKNOWN:
            log.critical('Unknown page state!')
            sys.exit(1)


def _book(driver):
    '''
    Books the device by `event.book`.
    '''
    try:
        event.book(driver)
    except Exception as e:
        log.critical(f'Book failed: {e}')
        sys.exit(1)
    log.info("Booked successfully!")


async def _login(driver):
    '''
    Logins user in booking login page by `event.login`.
    '''
    try:
        event.login(driver)
    except Exception as e:
        log.critical(f'Login failed: {e}')
        sys.exit(1)
    if _validate_page_state(driver) == _PageState.LOGIN_REQUIRED:
        log.critical("Login failed: Incorrect data.")
        exit(1)
    log.info("Logged successfully!")
    await _next(driver)


async def _unbook(driver):
    '''
    Unbooks the device by `event.unbook`.
    '''
    try:
        event.unbook(driver)
    except Exception as e:
        log.critical(f'Unbook failed: {e}')
        sys.exit(1)
    log.info("Unbooked successfully!")
    _update_page(driver)
    await _next(driver)


async def _wait_until_available(driver):
    '''
    Waits until at least one device becomes available.
    '''
    log.info("Waiting for available device.")
    await asyncio.sleep(get_settings().book_wait)
    _update_page(driver)
    await _next(driver)


def _load_page(driver: Firefox, href: str) -> None:
    '''
    Loads page.
    '''
    try:
        driver.get(href)
    except Exception as e:
        log.critical(f"Can't load page: {e}")
        sys.exit(1)
    log.info('Page loaded.')


def _update_page(driver: Firefox) -> None:
    '''
    Updates page.
    '''
    try:
        driver.refresh()
    except Exception as e:
        log.critical(f"Can't update page: {e}")
        sys.exit(1)
    log.info('Page reloaded.')


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
