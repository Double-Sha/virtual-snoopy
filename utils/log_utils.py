#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/20 18:22
# @Team : Private
# @Author : shasha.mao
# @Email : maoshasix@163.com
# @File : log_utils.py
# @Project : virtual-snoopy
# @Tool : PyCharm

import os
import logging
import time
import traceback


class MyLog:
    """根据配置文件生成log文件"""

    def __init__(self, log_config, log_name_label=None):
        """
        初始化log文件

        :param log_config: log配置类
        :param log_name_label: log文件名标识
        """

        self.log_config = log_config  # log配置文件
        self.log_name_label = log_name_label  # log文件命名：命名标识
        self.history_log_file_path_list = []  # log文件路径历史记录
        self.time_fmt = "%Y-%m-%d_%H-%M-%S"  # log文件命名：时间字符串格式
        self.fmt = logging.Formatter(fmt="【[%(asctime)s] - [%(name)s] - [%(levelname)s] - [%(module)s]】:  %(message)s",
                                     datefmt='%Y-%m-%d %H:%M:%S')  # 日志记录格式

        # 指定log file文件名
        if self.log_name_label is not None:
            # %Y%m%d%H%M%S
            # %Y-%m-%d
            log_file_name = self.log_name_label + "_" + time.strftime(self.time_fmt, time.localtime(time.time())) + ".log"
        else:
            log_file_name = log_config.log_name + "_" + time.strftime(self.time_fmt, time.localtime(time.time())) + ".log"

        # 指定log文件的绝对路径
        log_file_path = os.path.join(self.log_config.log_folder_path, log_file_name)

        # 类属性设置
        self.log_file_name = log_file_name  # 当前log文件
        self.log_file_path = log_file_path  # 当前log文件的绝对路径
        self.history_log_file_path_list.append(log_file_path)  # 当前log文件夹下的log文件列表（绝对路径）

        # 定义文件
        self.file = logging.FileHandler(filename=self.log_file_path,
                                        mode="a",
                                        encoding="utf-8")
        self.file.setFormatter(fmt=self.fmt)

        # 设定日志级别
        if log_config.level == "debug":
            level = logging.DEBUG
        elif log_config.level == "info":
            level = logging.INFO
        elif log_config.level == "warning":
            level = logging.WARNING
        elif log_config.level == "error":
            level = logging.ERROR
        else:
            level = logging.CRITICAL
        self.level = level

        # 生成logger对象
        self.logger = logging.Logger(name=self.log_config.label, level=self.level)
        self.logger.addHandler(self.file)

    def send_backup_log_to_mailbox(self, snoopy_mailbox, backup_file_path):
        """
        将某个日志文件发送到邮件（备份用）

        :param snoopy_mailbox: 邮箱对象
        :param backup_file_path: 日志文件的绝对路径
        """

        # 发送备份邮件
        body = "您好，附件为云端服务virtual_snoopy的log日志，现在对附件log日志进行备份，同时云端将删除该log文件"
        try:
            snoopy_mailbox.email_instance.send(to=self.log_config.backup_email_account,
                                               subject="日志备份",
                                               contents=body,
                                               attachments=backup_file_path)
        except Exception as e:
            self.logger.error(e)
            self.logger.error(traceback.format_exc())

        self.logger.info("备份邮件已发送")
        self.logger.info("备份文件=%s" % self.history_log_file_path_list[0])

    def reset(self):
        """重新生成log文件"""

        # 指定log file文件名
        if self.log_name_label is not None:
            # %Y%m%d%H%M%S
            # %Y-%m-%d
            log_file_name = self.log_name_label + "_" + time.strftime(self.time_fmt,
                                                                      time.localtime(time.time())) + ".log"
        else:
            log_file_name = self.log_config.log_name + "_" + time.strftime(self.time_fmt,
                                                                      time.localtime(time.time())) + ".log"

        # 指定log文件的绝对路径
        log_file_path = os.path.join(self.log_config.log_folder_path, log_file_name)

        # 类属性设置
        self.log_file_name = log_file_name
        self.log_file_path = log_file_path
        self.history_log_file_path_list.append(log_file_path)

        # 定义文件
        self.file = logging.FileHandler(filename=self.log_file_path,
                                        mode="a",
                                        encoding="utf-8")
        self.file.setFormatter(fmt=self.fmt)  # 沿用初始化时的fmt

        # 定义日志
        self.logger = logging.Logger(name=self.log_config.label, level=self.level)  # 沿用初始化事的level
        self.logger.addHandler(self.file)

    def check_size_log(self,snoopy_mailbox):
        """
        【检查事项1】：
        检查当前log文件大小，如果当前log文件大小，大于配置文件中的指定值，则删除当前文件，并新建一个log文件；
        【检查事项2】：
        检查当前log文件夹中的log文件个数，如果文件个数大于配置文件中的指定值，则通过邮箱备份后并删除最早的log文件
        """

        current_log_size = os.path.getsize(self.log_file_path) / (1024.0 * 1024.0)  # 转换成MB

        if current_log_size >= self.log_config.max_size_of_single_log_file:
            self.reset()
            print("iAM")

        if len(self.history_log_file_path_list) > self.log_config.total_number_of_log_files:
            # 先备份
            self.send_backup_log_to_mailbox(snoopy_mailbox=snoopy_mailbox,
                                            backup_file_path=self.history_log_file_path_list[0])
            # 删除文件
            os.remove(self.history_log_file_path_list[0])

            # 从历史列表中删除
            self.history_log_file_path_list.pop(0)


def main():
    """MyLog对象调用方法"""

    from conf import log_config, email_config
    from utils.email_utils import SnoopyMailBox

    snoopy_mailbox = SnoopyMailBox(email_config)
    log = MyLog(log_config=log_config)
    # while True:
    #     log.logger.info("hsafaasdfasdfasdfasdfahsafaasdfasdfasdfasdfahsafaasdfasdfasdfasdfahsafaasdfasdfasdfasdfahsafaasdfasdfasdfasdfahsafaasdfasdfasdfasdfahsafaasdfasdfasdfasdfaasdfhjkashfdhsafaasdfasdfasdfasdfasdfasdfasdfasdfsdfsasdfhjkashfdhsafaasdfasdfasdfasdfasdfasdfasdfasdfsdfsafdasdfjasdfjksajdfajsfdjlasdjflasjdfafdasdfjasdfjksajdfajsfdjlasdjflasjdfjasdlfjlaskdjfklasjdflksajdfljasldfjlasdfjlasdjfasdfhjkashfdhsafaasdfasdfasdfasdfasdfhjkashfdhsafaasdfasdfasdfasdfasdfasdfasdfasdfsdfsafdasdfjasdfjksajdfajsfdjlasdjflasjdfasdfasdfasdfasdfsdfsafdasdfjasdfjksajdfajsfdjlasdjflasjdf")
    #     log.check_size_log(snoopy_mailbox=snoopy_mailbox)
    #     time.sleep(0.5)

    # log.backup_by_email(snoopy_mailbox, r"D:\python_code\11_projects\virtual-snoopy\logs\virtual_snoopy.txt")

if __name__ == "__main__":
    main()
