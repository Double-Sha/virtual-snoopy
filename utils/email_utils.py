#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/11/25 18:43
# @Team : Private
# @Author : shasha.mao
# @Email : maoshasix@163.com
# @File : email_utils.py
# @Project : virtual-snoopy
# @Tool : PyCharm


import yagmail
import time
from utils.config_utils import config


class SnoopyMailBox:
    """邮箱类"""

    def __init__(self, config_object=config):
        """
        初始化邮箱对象
        :param config: 配置类
        """
        self.account = config.email["account"]
        self.password = config.email["password"]
        self.host = config.email["host"]
        self.master = config.email["master"]
        self.to_list = config.email["to_list"]
        self.cc_list = config.email["cc_list"]
        self.email_instance = yagmail.SMTP(user=self.account,
                                           password=self.password,
                                           host=self.host)

    def send_to_master(self, subject=None, contents=None, attachments=None):
        """向master用户发送邮件
        subject/contents/attachments三者不能同时为空，否则会报错554
        """

        # 标题
        if subject is not None:
            subject = "【Virtual Snoopy】 " + str(subject)

        # 开头 + 正文 + 结尾
        if contents is not None:
            beginning = "Dear Sha:\n\n" + "Here is some information to share with you.\n"
            ending = "\n\nYours\nVirtual Snoopy\n%s\n" % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            contents = beginning + contents + ending

        self.email_instance.send(to=self.master,
                                 cc=None,
                                 subject=subject,
                                 contents=contents,
                                 attachments=attachments)


def main():
    snoopy_mail_box = SnoopyMailBox(config_object=config)
    snoopy_mail_box.send_to_master()


if __name__ == "__main__":
    main()
else:
    # 实例化邮箱类对象, 供其他模块调用
    snoopy_mail_box = SnoopyMailBox(config_object=config)
