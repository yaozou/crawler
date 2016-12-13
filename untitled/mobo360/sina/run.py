#!/usr/bin/env python
# -*- coding:utf-8 -*-
import django
import os
import sys
import Queue
import threading
import time

from mobo360.sina.controller import Login
from mobo360.sina.controller import CrawlerFans
from mobo360.sina.controller import CrawlerPersonal
from mobo360.sina.controller import CrawlerTopic
from mobo360.sina.controller import CrawlerFollow
from mobo360.sina.model.user import sina_user

os.environ['DJANGO_SETTINGS_MODULE'] = 'untitled.settings'
if django.VERSION >= (1,7):
    django.setup()

class Worker(threading.Thread):    # 处理工作请求
    def __init__(self, workQueue, resultQueue, **kwds):
        threading.Thread.__init__(self, **kwds)
        self.setDaemon(True)
        self.workQueue = workQueue
        self.resultQueue = resultQueue

    def run(self):
        while 1:
            try:
                callable, args, kwds = self.workQueue.get(False)    # get task
                res = callable(*args, **kwds)
                self.resultQueue.put(res)    # put result
            except Queue.Empty:
                break

class WorkManager:    # 线程池管理,创建
    def __init__(self, num_of_workers=10):
        self.workQueue = Queue.Queue()    # 请求队列
        self.resultQueue = Queue.Queue()    # 输出结果的队列
        self.workers = []
        self._recruitThreads(num_of_workers)

    def _recruitThreads(self, num_of_workers):
        for i in range(num_of_workers):
            worker = Worker(self.workQueue, self.resultQueue)    # 创建工作线程
            self.workers.append(worker)    # 加入到线程队列


    def start(self):
        for w in self.workers:
            w.start()

    def wait_for_complete(self):
        while len(self.workers):
            worker = self.workers.pop()    # 从池中取出一个线程处理请求
            worker.join()
            if worker.isAlive() and not self.workQueue.empty():
                self.workers.append(worker)    # 重新加入线程池中
        print 'All jobs were complete.'


    def add_job(self, callable, *args, **kwds):
        self.workQueue.put((callable, args, kwds))    # 向工作队列中加入请求

    def get_result(self, *args, **kwds):
        return self.resultQueue.get(*args, **kwds)

class Spider():
    def __init__(self,num):
        self.num = num

    @staticmethod
    def run_first_get_topic(self):
        list = ["至上励合小五金恩圣"]
        driver = run_login()
        CrawlerTopic.topic_main(driver, list)

    @staticmethod
    def run_person_get_follow(self):
        driver = run_login()
        list = sina_user.UserInfo.objects.filter(premise='')
        CrawlerFollow.follow_main(driver, list)

    @staticmethod
    def run_person_get_fans(self):
        list = sina_user.UserInfo.objects.filter(premise='')
        if len(list) <= 0:
            self.run_person_get_fans(self)
        driver = run_login()
        CrawlerFans.fans_main(driver, list)
        self.run_person_get_fans(self)

    @staticmethod
    def run_person_get_info(self):
        list = sina_user.UserInfo.objects.filter(premise='')
        if len(list) <= 0:
            self.run_person_get_info(self)
        driver = run_login()
        CrawlerPersonal.personal_main(driver, list)
        self.run_person_get_info(self)

    def worker(self):
        if self.num == 4:
            self.run_first_get_topic(self)
        elif self.num == 3:
            self.run_person_get_follow(self)
        elif self.num == 2:
            self.run_person_get_fans(self)
        elif self.num == 1:
            self.run_person_get_info(self)


def run_login():
    driver = Login.main("771539058@qq.com","cbyz.0820")
    return driver;


def run_spider(num):
    s = Spider(num)
    s.worker()


def main():
    try:
        num_of_threads = int(sys.argv[1])
    except:
        num_of_threads = 4
    _st = time.time()
    wm = WorkManager(num_of_threads)
    nums = {1, 2, 3, 4}
    for num in nums:
        wm.add_job(run_spider, num)
    wm.start()
    wm.wait_for_complete()
    print time.time() - _st

if __name__ == '__main__':
    main()