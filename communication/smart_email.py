#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/11/25 18:43
# @Team : Private
# @Author : shasha.mao
# @Email : maoshasix@163.com
# @File : smart_email.py
# @Project : virtual-snoopy
# @Tool : PyCharm


import yagmail
from datetime import datetime


class MyMailBox():
    """邮箱类"""

    def __init__(self, config):
        """初始化邮箱对象"""
        self.account = config.email["account"]
        self.password = config.email["password"]
        self.host = config.email["host"]
        self.master = config.email["master"]
        self.to_list = config.email["to_list"]
        self.cc_list = config.email["cc_list"]
        self.email_instance = yagmail.SMTP(user=self.account,
                                           password=self.password,
                                           host=self.host)

    def send_qr_code(self,attachments_path):
        """to_list中的邮箱master用户发送二维码"""

        subject = "【二维码】微信登录"
        contents = "微信登录二维码来自云端" + "\n" +\
                    "【登录时间】 " + str(datetime.datetime.now())

        self.email_instance.send(to=self.master,
                                 subject=subject,
                                 contents=contents,
                                 attachments=attachments_path)