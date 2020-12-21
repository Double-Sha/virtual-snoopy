#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/20 15:21
# @Team : Private
# @Author : shasha.mao
# @Email : maoshasix@163.com
# @File : meal_reminder.py
# @Project : virtual-snoopy
# @Tool : PyCharm


import os
from random import randint
import time
import traceback


class MealReminder:

    def __init__(self, title_config, path_config, email_config, logger):
        """
        对象初始化

        :param title_config: 称谓配置对象实例
        :param path_config: 路径配置对象实例
        :param email_config: 邮箱配置对象实例
        :param logger: 日志对象实例
        """

        self.title_config = title_config
        self.path_config = path_config
        self.email_config = email_config
        self.mylog = logger
        pass

    def select_a_title(self):
        """根据配置文件中的darling_title_list信息，随机返回一个称呼"""

        return self.title_config.darling_title_list[randint(0, len(self.title_config.darling_title_list) - 1)]

    def select_a_picture(self, meal: str = "breakfast"):
        """
        指定用餐类型，从相应的文件夹中随机选择一张图片，并返回其绝对路径

        :param meal: 用餐类型，"breakfast", "lunch", "dinner"

        :return: aim_file_path: 随机选择出来的图片的绝对路径
        """

        # 指定文件夹，将从该文件夹中随机选择图片
        aim_picture_folder = os.path.join(self.path_config.resources_folder_path,
                                          "meal_reminder", meal)

        # 获取该文件夹下的图片名字列表
        file_name_list = os.listdir(aim_picture_folder)

        # 随机选择一张图片，并给出其绝对路径
        aim_file_path = os.path.join(aim_picture_folder,
                                     file_name_list[randint(0, len(file_name_list)-1)])
        return aim_file_path

    @staticmethod
    def generate_contents(meal: str = "breakfast"):
        """
        指定用餐类型，从相应的文件夹中随机选择一张图片，并返回其绝对路径

        :param meal: 用餐类型，"breakfast", "lunch", "dinner"

        :return: aim_file_path: 随机选择出来的图片的绝对路径
        """

        if meal == "breakfast":
            return "\n\n你好 :)\n俗话说：早餐要吃好，午餐要吃饱，晚餐要吃少。本宝宝建议您按时（8:00am - 9:00am）吃早餐呢~\n\n" \
                   "【早餐小贴士】\n早餐（breakfast/the morning meal），又叫早点、过早、早饭，是指在早上享用的餐。" \
                   "一般集中在早上六点至八点。世界各地的早餐食品均有不同，通常都以谷类食物为主，配上牛奶、咖啡、粥等。"
        elif meal == "dinner":
            return "\n\n你好 :)\n俗话说：早餐要吃好，午餐要吃饱，晚餐要吃少。本宝宝建议您按时（5:30pm - 6:30pm）吃晚餐呢~\n\n" \
                   "【晚餐小贴士】\n健康晚餐很重要对我们的身体健康有一定的影响，晚餐早吃少易患结石，所以说晚餐很重要。"
        else:
            return "\n\n你好 :)\n俗话说：早餐要吃好，午餐要吃饱，晚餐要吃少。本宝宝建议您按时（11:30am - 12:30am）吃午餐呢~\n\n" \
                   "【午餐小贴士】\n午餐（又名午饭、中餐、中饭等等），是指大约在中午或者之后一段时间所用的一餐。" \
                   "在中国大陆，人们认为中餐是一天中最重要的一餐，也是食物和能量的主要补充"

    def send_meal_reminder(self, snoopy_mailbox, meal: str = "breakfast", to=None):
        """
        编辑邮件，并发送邮件，邮件包含附件

        :param snoopy_mailbox: 邮箱实例
        :param meal: 用餐类型，"breakfast", "lunch", "dinner"
        :param to: 邮件发送列表
        """

        # 编辑邮件正文
        ending = "\n\nYours\n上海外滩最靓的仔\n%s\n" % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        contents = self.select_a_title() + self.generate_contents(meal) + ending

        # 确定发件人
        if to is not None:
            pass
        else:
            to = self.email_config.meal_reminder_to_list

        # 发送邮件
        try:
            snoopy_mailbox.email_instance.send(to=to,
                                               cc=self.email_config.meal_reminder_cc_list,
                                               subject="孟艺璇，你老公喊你吃饭啦！",
                                               contents=contents,
                                               attachments=self.select_a_picture(meal))
        except Exception as e:
            self.mylog.logger.error(e)
            self.mylog.logger.error(traceback.format_exc())

        self.mylog.logger.info("%s邮件已发送" % meal)


def main():
    """CarNumberStatistic类调用方法"""

    # 模块导入
    from conf import path_config, title_config, email_config, log_config
    from utils.email_utils import SnoopyMailBox
    from utils.log_utils import MyLog

    # 邮箱对象实例生成，日志对象实例生成
    snoopy_mailbox = SnoopyMailBox(email_config=email_config)
    snoopy_logger = MyLog(log_config=log_config)

    # MealReminder对象实例生成，及方法调用
    meal_reminder = MealReminder(title_config=title_config,
                                 path_config=path_config,
                                 email_config=email_config,
                                 logger=snoopy_logger)

    meal_reminder.send_meal_reminder(snoopy_mailbox=snoopy_mailbox,
                                     meal="breakfast",
                                     to=None)


if __name__ == "__main__":
    main()



