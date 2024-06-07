# webdriver_setup.py

from selenium import webdriver

def get_webdriver():
    options = webdriver.ChromeOptions()
    driver = webdriver.Remote(
        command_executor='http://172.23.0.3:4444/wd/hub',
        options=options
    )
    driver.maximize_window()
    return driver
