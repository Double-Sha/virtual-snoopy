#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Team : PRA-BD
# @Author: shasha.mao
# @Date : 12/19/2020 1:35 PM
# @File : temp_test.py
# @Tool : PyCharm

import schedule
import time
import traceback

# 配置文件类导入
from conf import email_config, path_config, title_config, log_config, mysql_config

# 工具类导入
from utils.thread_utils import create_thread_for_task
from utils.email_utils import SnoopyMailBox
from utils.log_utils import MyLog
from utils.test_utils import demo_error

snoopy_logger = MyLog(log_config=log_config)

try:
    demo_error()
except Exception as e:
    print(traceback.format_exc())
