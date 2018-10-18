import configparser
import os
import pickle

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import requests

class Scenario:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    CHROME_DRIVER_PATH = os.path.join(BASE_DIR, "chromedriver.exe")
    CONFIG_PATH = os.path.join(BASE_DIR, "config.ini")

    def __init__(self, username, password, token):
        self.username = username
        self.password = password
        self.token = token

        config = configparser.ConfigParser()
        config.read(self.CONFIG_PATH)

        self.url = config["base"]["url"]
        self.username_input_xpath = config["xpaths"]["username_input"]
        self.username_button_xpath = config["xpaths"]["username_button"]
        self.continue_button_xpath = config["xpaths"]["continue_button"]
        self.password_buttons_xpath = config["xpaths"]["password_buttons"]
        self.password_submit_button_xpath = config["xpaths"]["password_submit_button"]
        self.token_input_xpath = config["xpaths"]["token_input"]
        self.token_checkbox_xpath = config["xpaths"]["token_checkbox"]
        self.token_submit_button_xpath = config["xpaths"]["token_submit_button"]


        self.driver = self.get_chrome_driver()

    def get_chrome_driver(self):
        options = Options()
        options.add_argument("--window-size=1920x1080")
        options.add_experimental_option("detach", True)

        return webdriver.Chrome(self.CHROME_DRIVER_PATH, options=options)

    def play(self):
        self.driver.get(self.url)

        self.play_username_page()
        self.play_continue_page()
        self.play_password_page()
        self.play_token_page()       

    def play_username_page(self):
        username_input = self.driver.find_element_by_xpath(self.username_input_xpath)
        username_input.send_keys(self.username)

        username_button = self.driver.find_element_by_xpath(self.username_button_xpath)
        username_button.click()

    def play_continue_page(self):
        continue_button = self.driver.find_element_by_xpath(self.continue_button_xpath)
        continue_button.click()

    def play_password_page(self):
        # fmt: off
        password_buttons = self.driver.find_elements_by_xpath(self.password_buttons_xpath)  # NOQA
        password_buttons_mapping = self.get_password_buttons_mapping(password_buttons)
        # fmt: on

        for symbol in self.password:
            button = password_buttons_mapping[int(symbol)]
            button.click()

        # fmt: off
        password_submit_button = self.driver.find_element_by_xpath(self.password_submit_button_xpath)  # NOQA
        password_submit_button.click()
        # fmt: on

    def play_token_page(self):
        self.driver.get(self.url)

        token_input = self.driver.find_element_by_xpath(self.token_input_xpath)
        token_input.send_keys(self.token)

        token_checkbox = self.driver.find_element_by_xpath(self.token_checkbox_xpath)
        token_checkbox.click()

        token_submit_button = self.driver.find_element_by_xpath(self.token_submit_button_xpath)  # NOQA
        token_submit_button.click()

    def get_password_buttons_mapping(self, password_buttons_elements):
        """Converts randomized password buttons into mapping.

        On the page there're five randomly generated buttons with labels
        like '1 or 4'. To fill in password, user should click buttons in
        desired order.

        To simplify element clicking, build a mapping with number as a
        key and an element to click as a value.

        """
        password_buttons_mapping = dict()

        for password_button_element in password_buttons_elements:
            text = password_button_element.text
            nums = [int(s) for s in text.split() if s.isdigit()]

            parent = password_button_element.find_element_by_xpath("..")

            for num in nums:
                password_buttons_mapping[num] = parent

        return password_buttons_mapping
