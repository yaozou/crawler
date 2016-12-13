#!/usr/bin/python
# -*- coding: UTF-8 -*-
import django
import os
import re
import time
from selenium.webdriver.chrome.webdriver import WebDriver

from mobo360.sina.model.user import sina_user
from mobo360.core.utils import DateUtils
from mobo360.sina.controller import Login

os.environ['DJANGO_SETTINGS_MODULE'] = 'untitled.settings'
if django.VERSION >= (1,7):
    django.setup()


def fans_main( driver, user_list):
    # 获得用户信息
    time.sleep(10)
    for user in user_list:
        try :
            uid = user.sinaNo
            print uid
            get_fans_from_person_info(user.sinaNo, driver)
            time.sleep(2)
            analysis_fans(driver)
            page_fans(driver)
            print user.sinaNo
        except Exception:
            continue


# 通过个人首页跳转粉丝页面
def get_fans_from_person_info(uid,driver):
    nextHref = 'http://weibo.com/'+uid+'/fans?rightmod=1&wvr=6'
    print "Go to fans' page:", nextHref
    driver.get(nextHref)
    return driver


# 获得个人粉丝页面的所有分页地址
def page_fans(driver):
    try:
        w_pages = driver.find_element_by_class_name('W_pages')
        page_a = w_pages.find_elements_by_tag_name('a')
        href_list = list()
        for a in page_a:
            href = a.get_attribute("href")
            href_list.append(href)
        for href in href_list:
            if isinstance(href, basestring):
                print 'fans_page url :', href
                next_url = href;
                driver.get(next_url)
                time.sleep(3)
                try:
                    time.sleep(2)
                    analysis_fans(driver)
                except Exception:
                    break
    except Exception:
        raise Exception


# 解析每页粉丝信息
def analysis_fans(driver):
    if isinstance(driver,WebDriver):
        Login.to_bottom(driver)
    try:
        follow_list = driver.find_element_by_class_name('follow_list')
        li_list = follow_list.find_elements_by_tag_name('li')
        for li in li_list:
            try :
                # uid=6011451430&amp;fnick=喜欢姓王的&amp;sex=f
                user_info = li.get_attribute('action-data')
                mod_pic = li.find_element_by_tag_name('img')
                user = get_li_info(user_info)
                if user:
                    img = mod_pic.get_attribute('src')
                    user.headerPath = img
                    user.save()
            except Exception:
                continue
    except Exception:
        print Exception.message
        raise Exception


# 分解粉丝信息
def get_li_info(user_info):
    if isinstance(user_info, basestring): # uid=5234670682&fnick=菠萝包胖次&sex=m
        info = user_info.split('&',user_info.count("&"))
        #uid
        uidArray = info[0].split("=", user_info.count("="))
        uid = uidArray[1]
        # fnick
        fnickArray = info[1].split("=",user_info.count("="))
        fnick = fnickArray[1]
        # sex
        sexArray = info[2].split("=",user_info.count("="))
        sex = sexArray[1]
        a = sina_user.UserInfo.objects.filter(sinaNo=uid)
        if len(a) <= 0:
            user = sina_user.UserInfo()
        else:
            user = a[0]
        user.sinaNo = uid
        user.nickName = fnick
        user.gender = sex

        user.crTime = DateUtils.now_time()
    else :
        user = sina_user.UserInfo()
    return user

if __name__ == '__main__':
    driver = Login.main("771539058@qq.com", "cbyz.0820")
    time.sleep(3)
    user_list = sina_user.UserInfo.objects.filter(crTime__istartswith='2016-11-25', referFlag='')
    fans_main(driver, user_list)
