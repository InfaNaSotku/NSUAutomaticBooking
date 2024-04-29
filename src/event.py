from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from settings import get_settings


def login(driver: Firefox):
    '''
    Logins user in booking login page.
    '''
    email_input = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'Email'))
    )
    password_input = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'Password'))
    )
    submit = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'btn'))
    )

    email_input.send_keys(get_settings().email)
    password_input.send_keys(get_settings().password)
    submit.click()
