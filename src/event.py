from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from settings import get_settings


def login(driver: Firefox) -> None:
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


def book(driver: Firefox) -> None:
    '''
    Books the device.
    '''
    devices = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'device'))
    )
    for device in devices:
        panel = device.find_element(By.CLASS_NAME, 'panel-body-inside')
        button = panel.find_element(By.TAG_NAME, 'button')
        if button.text == 'Забронировать':
            button.click()
            modals = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'modal'))
            )
            for modal in modals:
                try:
                    footer = modal.find_element(By.CLASS_NAME, 'modal-footer')
                    button = footer.find_element(By.TAG_NAME, 'button')
                except Exception:
                    continue

                if button.text == 'Забронировать':
                    button.click()
                    return
            return

    raise RuntimeError('Unbooked device not found.')


def unbooks(driver: Firefox) -> None:
    '''
    Unbooks the device.
    '''
