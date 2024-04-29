from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache
import logging
import sys


class Settings(BaseSettings):
    email: str = Field(validation_alias="EMAIL")
    password: str = Field(validation_alias="PASSWORD")


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
