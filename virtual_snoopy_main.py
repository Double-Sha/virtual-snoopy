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

# 工具类导入
from utils.thread_utils import create_thread_for_task
from utils.email_utils import SnoopyMailBox

# 主函数
def main():
    # 回调函数run_threaded，回调函数的传参func2，"10second"
    schedule.every(2).seconds.do(create_thread_for_task, func2, ("name",), "thread_name")

    count = 0
    while True:
        time.sleep(1)
        count += 1
        schedule.run_pending()  # 运行所有可以运行的任务
        print("[第%d秒]" % count, "正在运行%d个线程" % len(threading.enumerate()), threading.enumerate(),
              "正在活跃%d个线程" % threading.activeCount(), end="\n")


if __name__ == "__main__":
    main()
