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
import traceback

# 配置文件类导入
from conf import email_config, path_config, title_config, log_config, mysql_config

# 工具类导入
from utils.thread_utils import create_thread_for_task
from utils.email_utils import SnoopyMailBox
from utils.log_utils import MyLog

# job类导入
from jobs.meal_reminder import MealReminder
from jobs.car_number_statistic import CarNumberStatistic


# TODO log工具类，进一步细化，格式调整
# TODO jobs引用log，记录每个类的输出情况
# TODO 异常抛出与捕获
# TODO 日志检查加入schedule类中
# TODO 主函数的任务调度
# TODO 日志类中的文件名格式strftime，配置文件更新

# 主函数
def main():
    """程序入口"""

    # 邮箱对象生成，日志对象生成
    snoopy_mailbox = SnoopyMailBox(email_config=email_config)
    snoopy_logger = MyLog(log_config=log_config)
    snoopy_logger.logger.info("【successful】邮箱对象实例生成，日志对象生成")

    # MealReminder对象生成
    meal_reminder = MealReminder(title_config=title_config,
                                 path_config=path_config,
                                 email_config=email_config,
                                 logger=snoopy_logger)

    # CarNumberStatistic对象生成
    car_number_statistic = CarNumberStatistic(mysql_config=mysql_config,
                                              logger=snoopy_logger,
                                              past_days=10)
    snoopy_logger.logger.info("【successful】MealReminder对象生成，CarNumberStatistic对象生成")

    # 任务安排
    # 【一】1.1提醒孟宝宝按时就餐-早餐
    schedule.every().monday.at("08:30").\
        do(create_thread_for_task, snoopy_logger, meal_reminder.send_meal_reminder_to_mailbox, (snoopy_mailbox, "breakfast"), "MealReminder")
    # 【一】1.3提醒孟宝宝按时就餐-午餐
    schedule.every().wednesday.at("11:30").\
        do(create_thread_for_task, snoopy_logger, meal_reminder.send_meal_reminder_to_mailbox, (snoopy_mailbox, "lunch"), "MealReminder")
    # 【一】1.2提醒孟宝宝按时就餐-晚餐
    schedule.every().friday.at("17:00").\
        do(create_thread_for_task, snoopy_logger, meal_reminder.send_meal_reminder_to_mailbox, (snoopy_mailbox, "dinner"), "MealReminder")

    # 【二】2.1 GWM生产环境车辆接入数检查
    schedule.every().monday.at("14:20").\
        do(create_thread_for_task, snoopy_logger, car_number_statistic.send_car_number_excel_to_mailbox, (snoopy_mailbox, email_config, path_config), "CarNumberStatistic")

    snoopy_logger.logger.info("【successful】jobs已添加")

    # 任务执行
    count = 0
    while True:
        try:
            schedule.run_pending()  # 运行所有可以运行的任务
            if count == 60:
                snoopy_logger.check_size_log()
                count = 0  # 每过60次 × 40s＝40min检查一下日志大小
        except Exception as e:
            print(e)
            snoopy_logger.logger.error(e)
            traceback.print_exc(snoopy_logger.log_file_path)
        finally:
            time.sleep(40)
            count += 1


if __name__ == "__main__":
    main()
