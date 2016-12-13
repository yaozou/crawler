# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.db import models
import os
os.environ.update({"DJANGO_SETTINGS_MODULE": "untitled.settings"})

# Create your models here.


class UserInfo(models.Model):
    nickName = models.CharField('昵称',max_length=200,db_column='nick_name')
    premise = models.CharField('所在地',max_length=100,db_column='premise')
    gender  = models.CharField('性别',max_length=10,db_column='gender')
    birthday = models.CharField('生日',max_length=60,db_column='birthday')
    intro = models.TextField('简介',db_column='intro')
    registerTime = models.CharField('注册时间',max_length=100,db_column='register_time')
    headerPath = models.CharField('头像',max_length=500,db_column='header_path')

    level = models.CharField('等级', max_length=50, db_column='level')
    badge = models.CharField('勋章', max_length=600, db_column='badge')

    place = models.CharField('关注数量', max_length=50, db_column='place')
    fans = models.CharField('粉丝数量', max_length=50, db_column='fans')
    blog = models.CharField('微博数量', max_length=50, db_column='blog')

    sinaNo = models.CharField('微博用户编号', max_length=100, db_column='sina_no')
    referFlag = models.CharField('标识', max_length=50, db_column='refer_flag')
    crTime = models.CharField('获取时间', max_length=100, db_column='cr_time')

    class Meta:
        verbose_name = ('新浪微博用户信息')
        db_table = "sina_user_info"