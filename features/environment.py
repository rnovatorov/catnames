import os
import logging
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
# Custom modules
from config import VK_TEST_USER_PHONE, VK_TEST_USER_PASSWORD


def before_all(context):
    # Setting up logging
    context.logger = logging.getLogger(__name__)
    context.logger.setLevel(logging.INFO)

    # Setting up Selenium
    context.driver = webdriver.Firefox(log_path="tmp/geckodriver.log")
    context.wait = WebDriverWait(context.driver, 5)
    context.screenshot_dir = os.path.abspath("tmp/screenshots")

    # Index page
    context.index_page = "http://127.0.0.1:5000/"

    # Credentials
    context.vk_test_user_credentials = {"phone": VK_TEST_USER_PHONE,
                                        "password": VK_TEST_USER_PASSWORD}


def after_all(context):
    context.driver.quit()
