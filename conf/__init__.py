#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Team : PRA-BD
# @Author: shasha.mao
# @Date : 12/19/2020 1:10 PM
# @File : __init__.py.py
# @Tool : PyCharm

import os
import sys
from utils.config_utils import Config
from bunch import Bunch

# 项目相关目录配置类(使用绝对路径)
root_folder_path = os.path.dirname(os.path.dirname(__file__))
path_config = Bunch({"root_folder_path": root_folder_path,
                     "config_folder_path": os.path.join(root_folder_path, r"conf"),
                     "resources_folder_path": os.path.join(root_folder_path, r"resources"),
                     "log_folder_path": os.path.join(root_folder_path, r"logs")})
# print(path_config)

# 导入配置文件
config_file_path = os.path.join(path_config.config_folder_path, "conf.json")
config = Config().get_config(config_file_path)

# 生成邮箱配置类
email_config = Bunch(config.email)
# print(email_config.account)

# 生成称呼类
title_config = Bunch(config.title)
# print(title_config.owner)

# 生成GWM生产数据数据库类
mysql_config = Bunch(config.mysql)
# print(title_config.owner)

# 生成日志配置类
log_config = Bunch(config.log)
log_config.log_folder_path = path_config.log_folder_path




