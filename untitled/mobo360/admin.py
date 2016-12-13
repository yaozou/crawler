# -*- coding: UTF-8 -*-
from django.contrib import admin

# Register your models here.
from mobo360 import models
from mobo360.sina.model.user import sina_user

# 新浪微博的用户信息
# admin.site.register(models.UserInfo)
admin.site.register(sina_user.UserInfo)
