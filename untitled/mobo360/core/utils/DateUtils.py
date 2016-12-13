#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time


def now_date():
    return time.strftime("%Y-%m-%d", time.localtime())


def now_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())