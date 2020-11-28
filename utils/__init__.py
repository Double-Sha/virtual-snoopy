#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/11/24 20:23
# @Team : Private
# @Author : shasha.mao
# @Email : maoshasix@163.com
# @File : __init__.py.py
# @Project : virtual-snoopy
# @Tool : PyCharm


from config_utils import Config

temp = Config()
config = temp.get_config(r"../conf/conf.json")