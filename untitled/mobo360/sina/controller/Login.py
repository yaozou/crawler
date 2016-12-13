#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  # 键盘
from selenium.common.exceptions import *

# come to the bottom of ther page
def to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print "To bottom......"


# login with your own account
def login(driver, account, password):
    try:
        print "点击登录。。。。。。"
        label = driver.find_element_by_link_text('登录')
        label.click()
        time.sleep(1)

        box_login = driver.find_element_by_class_name('form_login_register')

        print "输入用户名。。。。。。"
        login_name = box_login.find_element_by_name('username')
        login_name.send_keys(account)
        time.sleep(1)

        print "输入密码。。。。。。"
        login_pw = box_login.find_element_by_name('password')
        login_pw.send_keys(password)
        time.sleep(1)

        print "回车登录。。。。。。"
        login_pw.send_keys(Keys.RETURN)
    except NoSuchElementException:
        print 'NoSuchElementException'

def main(account, password):
    # type: (object, object) -> object
    driver = webdriver.Chrome()
    driver.get('http://weibo.com')
    # login
    time.sleep(6)
    login(driver, account, password)
    return driver