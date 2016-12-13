#!/usr/bin/python
# -*- coding: UTF-8 -*-
import django
import os
import sys
import re
import time
import Login
from mobo360.sina.model.user import sina_user

os.environ['DJANGO_SETTINGS_MODULE'] = 'untitled.settings'
if django.VERSION >= (1,7):
    django.setup()
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


def personal_main(driver, user_list):
    time.sleep(10)
    for user in user_list:
        go_personal_deatil(driver, user.sinaNo)
        time.sleep(10)
        Login.to_bottom(driver)
        get_personal_other_info(driver, user)
        get_personal_base_info(driver, user)
        user.referFlag = '100505'
        sina_user.UserInfo.save(user)


def go_personal_deatil(driver,uid):
    nextHref = 'http://weibo.com/'+uid+'/info'
    print "Go to peronal href:", nextHref
    driver.get(nextHref)
    return driver


def get_personal_base_info(driver,user):
   try:
       # 基本信息
       person = driver.find_element_by_class_name('PCD_text_b')
       person_li = person.find_elements_by_tag_name('li')
       i = 0
       nickname,gender, premise, gender, birthday, intro, registerTime = '', '','', '', '', '', ''
       while (i < len(person_li)):
           li = person_li[i]
           li_title = li.find_element_by_class_name('pt_title')
           title_text = li_title.text
           try:
               li_detail = li.find_element_by_class_name('pt_detail')
               title_text = title_text.encode('utf-8')
               detail_text = li_detail.text
               if ('所在地' in title_text):
                   premise = detail_text
               elif ('性别' in title_text):
                   gender = detail_text
               elif ('生日' in title_text):
                   birthday = detail_text
               elif ('简介' in title_text):
                   intro = detail_text
               elif ('注册时间' in title_text):
                   registerTime = detail_text
           except Exception:
               pass
           i = i + 1

       user.premise = premise
       user.birthday = birthday
       user.intro = intro
       user.registerTime = registerTime
       if( user.gender == '') :
           user.gender = gender;
   except Exception:
       pass


# 等级等信息
def get_personal_other_info(driver,user):
    # 点击展示左侧可能隐藏的部分
    try:
        w_fold = driver.find_element_by_class_name('W_fold')
        w_fold.click()
    except Exception:
        pass
    try:
        # 1、关注数量,粉丝数量、微博数量
        tb_counter = driver.find_element_by_class_name('tb_counter')
        tbs = tb_counter.find_elements_by_tag_name('a')
        # 关注
        placeTag = tbs[0].find_element_by_tag_name('strong')
        place = placeTag.text
        if not place:
            time.sleep(3)
            place = placeTag.text
        # 粉丝
        fansTag = tbs[1].find_element_by_tag_name('strong')
        fans = fansTag.text

        # 微博
        blogTag = tbs[2].find_element_by_tag_name('strong')
        blog = blogTag.text

        # 2、勋章
        bagde_list = driver.find_element_by_class_name('bagde_list')
        bagde_lis = bagde_list.find_elements_by_tag_name('a')
        bagde = ''
        for li in bagde_lis:
            bagde += li.get_attribute('title') + ','

        # 3、等级
        w_icon_level = driver.find_element_by_class_name('W_icon_level')
        level_span = w_icon_level.find_element_by_tag_name('span')
        level = level_span.text

        user.place = place
        user.fans = fans
        user.blog = blog
        user.badge = bagde
        user.level = level
    except Exception:
        pass


if __name__ == '__main__':
    driver = Login.main("771539058@qq.com", "cbyz.0820")
    time.sleep(3)
    user_list = sina_user.UserInfo.objects.filter(crTime__istartswith='2016-11-25',referFlag='')
    personal_main(driver, user_list)
