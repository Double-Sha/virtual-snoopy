#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Team : PRA-BD
# @Author: shasha.mao
# @Date : 12/19/2020 1:10 PM
# @File : __init__.py.py
# @Tool : PyCharm

import os
from utils.config_utils import Config
from bunch import Bunch

config_file_path = os.path.join(os.path.dirname(__file__), "conf.json")
config = Config().get_config(config_file_path)

# 邮箱配置类
email_config = Bunch(config.email)
# print(email_config.account)

# 称呼类
title_config = Bunch(config.title)
# print(title_config.owner)

# GWM生产数据数据库类
mysql_config = Bunch(config.mysql)
# print(title_config.owner)
