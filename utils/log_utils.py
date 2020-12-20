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
from conf import log_config


class MyLog:
    """根据配置文件生成log文件"""

    def __init__(self, log_config, log_name_label=None):
        """
        初始化log文件
        :param log_config:
        :param log_name_label:
        """

        self.log_config = log_config
        self.log_name_label = log_name_label
        self.history_log_list = []

        # 指定log file文件名
        if self.log_name_label is not None:
            # %Y%m%d%H%M%S
            # %Y-%m-%d
            log_file_name = self.log_name_label + "_" + time.strftime("%Y%m%d%H%M%S", time.localtime(time.time())) + ".log"
        else:
            log_file_name = log_config.log_name + "_" + time.strftime("%Y%m%d%H%M%S", time.localtime(time.time())) + ".log"

        # 指定log文件的绝对路径
        log_file_path = os.path.join(self.log_config.log_folder_path, log_file_name)

        # 类属性设置
        self.log_file_name = log_file_name
        self.log_file_path = log_file_path
        self.history_log_list.append(log_file_path)

        # 定义文件
        self.file = logging.FileHandler(filename=self.log_file_path,
                                        mode="a",
                                        encoding="utf-8")

        self.fmt = logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s -%(module)s:  %(message)s",
                                     datefmt='%Y-%m-%d %H:%M:%S')
        self.file.setFormatter(fmt=self.fmt)

        # 定义日志
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
        self.logger = logging.Logger(name=self.log_config.label, level=self.level)
        self.logger.addHandler(self.file)

    def reset(self):
        # 指定log file文件名
        if self.log_name_label is not None:
            # %Y%m%d%H%M%S
            # %Y-%m-%d
            log_file_name = self.log_name_label + "_" + time.strftime("%Y%m%d%H%M%S",
                                                                      time.localtime(time.time())) + ".log"
        else:
            log_file_name = log_config.log_name + "_" + time.strftime("%Y%m%d%H%M%S",
                                                                      time.localtime(time.time())) + ".log"

        # 指定log文件的绝对路径
        log_file_path = os.path.join(self.log_config.log_folder_path, log_file_name)

        # 类属性设置
        self.log_file_name = log_file_name
        self.log_file_path = log_file_path
        self.history_log_list.append(log_file_path)

        # 定义文件
        self.file = logging.FileHandler(filename=self.log_file_path,
                                        mode="a",
                                        encoding="utf-8")
        self.file.setFormatter(fmt=self.fmt)  # 沿用初始化时的fmt

        # 定义日志
        self.logger = logging.Logger(name=self.log_config.label, level=self.level)  # 沿用初始化事的level
        self.logger.addHandler(self.file)

    def check_size_log(self):
        """
        检查当前log文件大小，如果当前log文件大小，大于配置文件中的指定值，则删除当前文件，并新建一个log文件；
        检查当前log文件夹中的log文件个数，如果文件个数大于配置文件中的指定值，则删除最早的log文件
        """

        current_log_size = os.path.getsize(self.log_file_path) / (1024.0 * 1024.0)  # 转换成MB
        print(round(current_log_size, 2), log_config.max_size_of_single_log_file)
        if current_log_size >= self.log_config.max_size_of_single_log_file:
            self.reset()
            print("iAM")
        print(len(self.history_log_list), self.log_config.total_number_of_log_files)
        if len(self.history_log_list) > self.log_config.total_number_of_log_files:
            os.remove(self.history_log_list[0])
            self.history_log_list.pop(0)


def main():
    log = MyLog(log_config)

    while True:
        log.logger.info("hsafaasdfasdfasdfasdfahsafaasdfasdfasdfasdfahsafaasdfasdfasdfasdfahsafaasdfasdfasdfasdfahsafaasdfasdfasdfasdfahsafaasdfasdfasdfasdfahsafaasdfasdfasdfasdfaasdfhjkashfdhsafaasdfasdfasdfasdfasdfasdfasdfasdfsdfsasdfhjkashfdhsafaasdfasdfasdfasdfasdfasdfasdfasdfsdfsafdasdfjasdfjksajdfajsfdjlasdjflasjdfafdasdfjasdfjksajdfajsfdjlasdjflasjdfjasdlfjlaskdjfklasjdflksajdfljasldfjlasdfjlasdjfasdfhjkashfdhsafaasdfasdfasdfasdfasdfhjkashfdhsafaasdfasdfasdfasdfasdfasdfasdfasdfsdfsafdasdfjasdfjksajdfajsfdjlasdjflasjdfasdfasdfasdfasdfsdfsafdasdfjasdfjksajdfajsfdjlasdjflasjdf")
        log.check_size_log()
        time.sleep(0.5)


if __name__ == "__main__":
    main()
