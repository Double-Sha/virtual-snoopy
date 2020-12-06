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
    def get_config(config_path=r"../conf/conf.json"):
        """默认读取/conf/conf.json的文件默认"""

        with open(config_path) as fp:
            config = Bunch(load(fp))

        return config


def main():
    temp = Config()
    config = temp.get_config()
    print(config.email["account"])


if __name__ == "__main__":
    main()

else:
    # 实例化配置类对象,并直接获取配置信息，供其他模块调用
    config = Config().get_config()
