#!/usr/bin/python
# -*- coding: UTF-8 -*-
# desc:从微博用户主题爬取用户信息
import django
import os
import re
import time

from mobo360.sina.model.user import sina_user
from mobo360.core.utils import DateUtils
from mobo360.sina.controller import Login

os.environ['DJANGO_SETTINGS_MODULE'] = 'untitled.settings'
if django.VERSION >= (1,7):
    django.setup()


def topic_main(driver, list):
    for topic in list:
        try:
            get_fans_from_topic(topic, driver)
            get_data(driver)
        except Exception:
            continue
    driver.close()


# 使用搜索名称操作跳转粉丝页面
def get_fans_from_topic(topic,driver):
    time.sleep(20)
    driver.get('http://s.weibo.com/weibo/{}?topnav=1&wvr=6&b=1'.format(topic))
    time.sleep(10)
    Login.to_bottom(driver)
    e = driver.find_elements_by_tag_name("a")
    nextHref = ''
    for x in e:
        href = x.get_attribute("href")
        # print href
        if isinstance(href, basestring):
            searchFlag = re.search('/fans', href, re.M | re.I)
            if (searchFlag):
                nextHref = href;
                break
    if nextHref.strip() != '':
        print "Go to next href:", nextHref
        driver.get(nextHref)
    return driver


# 初始化数据
def get_data(driver):
    try:
        time.sleep(2)
        print '解析个人信息。。。。。。。。。'
        try :
            pf_opt = driver.find_element_by_class_name('pf_opt')
            btn_bed = pf_opt.find_element_by_class_name('btn_bed')
            action_data = btn_bed.get_attribute('action-data')
            uidArray = action_data.split('&', action_data.count("&"))
            uid = uidArray[0].split("=", action_data.count("="))[1]

            pf_photo = driver.find_element_by_class_name('pf_photo')
            img = pf_photo.find_elements_by_tag_name('img')
            headerPath = img[0].get_attribute('src')

            pf_username = driver.find_element_by_class_name('pf_username')
            h1_username = pf_username.find_elements_by_tag_name('h1')
            username = h1_username[0].text

            user = sina_user.UserInfo()
            user.sinaNo = uid
            user.headerPath = headerPath
            user.nickName = username
            user.crTime = DateUtils.now_time()
            sina_user.UserInfo.save(user)

        except Exception:
            pass
    except Exception:
        raise Exception

if __name__ == '__main__':
    list = ["至上励合", "至上励合张远", "至上励合_马雪阳MARS", "至上励合小五金恩圣"]
    driver = Login.main("771539058@qq.com", "cbyz.0820")
    time.sleep(3)
    topic_main(driver, list)