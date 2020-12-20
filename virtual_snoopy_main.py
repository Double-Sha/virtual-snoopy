#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/11/24 20:13
# @Team : Private
# @Author : shasha.mao
# @Email : maoshasix@163.com
# @File : virtual_snoopy_main.py
# @Project : virtual-snoopy
# @Tool : PyCharm


# 模块导入
import schedule
import time
import threading
import pandas as pd

# 配置文件类导入
from conf import email_config
# 工具类导入
from utils.thread_utils import create_thread_for_task
from utils.email_utils import SnoopyMailBox
from jobs.meal_reminder import MealReminder
from jobs.car_numbers_statistic import CarNumberInGwmPrd

# TODO log工具类，进一步细化，格式调整
# TODO jobs引用log，记录每个类的输出情况
# TODO 异常抛出与捕获
# TODO 日志检查加入schedule类中
# TODO 主函数的任务调度
# TODO 日志类中的文件名格式strftime，配置文件更新


# 主函数
def main():
    """程序入口"""

    # 邮箱类生成
    snoopy_mail_box = SnoopyMailBox(email_config)

    # 任务调度

    # 【一】1.1提醒孟宝宝按时就餐-早餐
    schedule.every().monday.at("08:30").\
        do(create_thread_for_task, MealReminder().send_meal_reminder, (snoopy_mail_box, "breakfast"), "MealReminder")
    # 【一】1.3提醒孟宝宝按时就餐-午餐
    schedule.every().wednesday.at("11:30").\
        do(create_thread_for_task, MealReminder().send_meal_reminder, (snoopy_mail_box, "lunch"), "MealReminder")
    # 【一】1.2提醒孟宝宝按时就餐-晚餐
    schedule.every().friday.at("17:00").\
        do(create_thread_for_task, MealReminder().send_meal_reminder, (snoopy_mail_box, "dinner"), "MealReminder")

    # 【二】2.1 GWM生产环境车辆接入数检查
    schedule.every().monday.at("13:00").\
        do(create_thread_for_task, MealReminder().send_meal_reminder, (snoopy_mail_box, "dinner"), "MealReminder")

    count = 0
    while True:
        time.sleep(20)


if __name__ == "__main__":
    main()
