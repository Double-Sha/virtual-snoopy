#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/11/25 20:11
# @Team : Private
# @Author : shasha.mao
# @Email : maoshasix@163.com
# @File : my_test.py
# @Project : virtual-snoopy
# @Tool : PyCharm


# 模块导入
import schedule
import time
import threading
import pandas as pd

# 工具类导入
from utils.thread_utils import create_thread_for_task

# 类的生成
def func():
    a = 1+2
    a = 1+2
    a = 166 * 244 * 124 / 2.2
    a = 166 * 244 * 124 / 2.2
    a = 166 * 244 * 124 / 2.2
    print(a)
    temp4 = pd.read_csv(r"E:\06_Dataset\02_EV_data\02_EV_Dataset\02_pcode\租赁乘用车_vin_ASC.csv")
    temp5 = pd.read_csv(r"E:\06_Dataset\02_EV_data\02_EV_Dataset\02_pcode\租赁乘用车_vin_DESC.csv")
    temp6 = pd.read_csv(r"E:\06_Dataset\02_EV_data\02_EV_Dataset\02_pcode\租赁乘用车_vin_DESC.csv")
    pass
    # print("定时任务每5秒一次", datetime.datetime.now(), end="\n")


def func2(str):
    a = 1+2
    a = 166 * 244 * 124 / 2.2
    a = 166 * 244 * 124 / 2.2
    a = 166 * 244 * 124 / 2.2
    start = time.time()
    print(str)
    # temp = pd.read_csv(r"E:\06_Dataset\02_EV_data\02_EV_Dataset\02_pcode\租赁乘用车_vin_DESC.csv")
    # temp2 = pd.read_csv(r"E:\06_Dataset\02_EV_data\02_EV_Dataset\02_pcode\租赁乘用车_vin_DESC.csv")
    # temp3 = pd.read_csv(r"E:\06_Dataset\02_EV_data\02_EV_Dataset\02_pcode\租赁乘用车_vin_DESC.csv")
    print("耗时", time.time() - start)
    print(a)
    pass
    # print("定时任务每13一次", datetime.datetime.now(), end="\n")


# 定义


# schedule.every(7).seconds.do(run_threaded, func, "5second")

# 回调函数run_threaded，回调函数的传参func2，"10second"
schedule.every(2).seconds.do(create_thread_for_task, func2, ("name",), "thread_name")

schedule.run_pending()
count = 0
while True:
    time.sleep(1)
    count += 1
    schedule.run_pending()  # 运行所有可以运行的任务
    print("[第%d秒]" % count, "正在运行%d个线程" % len(threading.enumerate()), threading.enumerate(), "正在活跃%d个线程" % threading.activeCount(), end="\n")



