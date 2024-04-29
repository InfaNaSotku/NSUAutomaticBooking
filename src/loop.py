import asyncio
from driver import get_driver
from settings import get_settings
import logging as log
import sys


def start():
    '''
    Started app loop.
    '''
    asyncio.run(_run())


async def _run():
    log.info("Loop started.")
    driver = get_driver()
    try:
        driver.get(get_settings().devices_href)
    except Exception as e:
        log.critical(f"Can't load page: {e}")
        sys.exit(0)
