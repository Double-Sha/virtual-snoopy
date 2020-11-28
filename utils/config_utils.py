#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/11/24 20:24
# @Team : Private
# @Author : shasha.mao
# @Email : maoshasix@163.com
# @File : config_utils.py
# @Project : virtual-snoopy
# @Tool : PyCharm


from json import load
from bunch import Bunch


class Config():
    """配置对象类，将json格式的配置文件转化为python对象，可以通过属性的形式访问配置文件"""

    def __init__(self):
        pass

    @staticmethod
    def get_config(config_path):

        with open(config_path) as fp:
            config = Bunch(load(fp))

        return config


def main():
    temp = Config()
    config = temp.get_config(r"../conf/conf.json")
    print(config.email["account"])


if __name__ == "__main__":
    main()
