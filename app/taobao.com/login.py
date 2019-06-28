# coding = utf-8
import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import datetime
import time

USERNAME = 'xxx'
PASSWORD = 'xxx'


class taobao_spyder:
    def __init__(self, url):
        self.url = url
        options = webdriver.ChromeOptions()
        # 此步骤很重要，设置为开发者模式，防止被网站识别出来使用了Selenium
        options.add_experimental_option(
            'excludeSwitches', ['enable-automation'])
        self.browser = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.browser, 10)

    def login(self):
        print('准备登陆')
        time.sleep(1)
        self.browser.get(self.url)
        # 点击密码登录
        self.browser.find_element_by_css_selector('.J_Quick2Static').click()
        input = self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#TPL_username_1')))
        time.sleep(2)

        input2 = self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#TPL_password_1')))
        submit = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#J_SubmitStatic')))
        submit.click()  # J_SelectAll1
        input.send_keys(USERNAME)  # J_SelectAll1 > div > label
        input2.send_keys(PASSWORD)
        submit.click()
        time.sleep(1)
        input2 = self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#TPL_password_1')))
        input2.send_keys(PASSWORD)


if __name__ == '__main__':
    url = 'https://login.taobao.com/member/login.jhtml'
    a = taobao_spyder(url)
    a.login()