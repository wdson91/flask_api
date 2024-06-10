# webdriver_setup.py
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium import webdriver
capabilities = DesiredCapabilities.CHROME.copy()
def get_webdriver():
    options = webdriver.ChromeOptions()
    driver = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        options=options,
        
    )
    driver.maximize_window()
    return driver
