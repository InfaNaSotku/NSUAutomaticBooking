from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache
import logging
import sys


class Settings(BaseSettings):
    email: str = Field(validation_alias="EMAIL")
    password: str = Field(validation_alias="PASSWORD")
    page_live_time: int = Field(validation_alias="PAGE_LIVE_TIME", default=600)
    book_wait: int = Field(validation_alias="BOOK_WAIT", default=10)

    devices_href: str = Field(
        validation_alias="DEVICES_HREF",
        default="https://lk.1clc.ru/DeviceCurrent/DevicesCurrent"
    )


@lru_cache
def get_settings() -> Settings:
    '''Returns settings of app.

    Settings will be generate only for first call.
    '''
    try:
        settings = Settings()
        return settings
    except Exception as e:
        logging.critical(f"Settings generated with error: {e}")
        sys.exit()
