from selenium import webdriver
import os


def get_chrome_driver_options():
    driver_options = webdriver.ChromeOptions()
    driver_options.headless = True

    preset_location = os.environ.get("GOOGLE_CHROME_BIN")
    if preset_location is not None:
        driver_options._binary_location = preset_location

    driver_options.add_argument('--disable-gpu')
    driver_options.add_argument('--no-sandbox')
    return driver_options
