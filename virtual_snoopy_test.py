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


# 主函数
def main():
    """程序入口"""

    # 邮箱类生成
    snoopy_mail_box = SnoopyMailBox(email_config)

    # 【job】
    # job = create_thread_for_task

    # 【传参】
    # job传参1 = MealReminder().send_meal_reminder, (snoopy_mail_box, "dinner")
    #        其中snoopy_mail_box, "dinner"是MealReminder().send_meal_reminder的传参
    # job传参2 = "MealReminder"

    schedule.every(2).minutes.\
        do(create_thread_for_task, MealReminder().send_meal_reminder, (snoopy_mail_box, "dinner"), "MealReminder")

    count = 0
    while True:
        time.sleep(20)
        count += 1
        schedule.run_pending()  # 运行所有可以运行的任务
        print("[第%d秒]" % count, "正在运行%d个线程" % len(threading.enumerate()), threading.enumerate(),
              "正在活跃%d个线程" % threading.activeCount(), end="\n")


if __name__ == "__main__":
    main()
