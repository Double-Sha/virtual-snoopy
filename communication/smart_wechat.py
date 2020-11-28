#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/11/25 18:44
# @Team : Private
# @Author : shasha.mao
# @Email : maoshasix@163.com
# @File : smart_wechat.py
# @Project : virtual-snoopy
# @Tool : PyCharm

import itchat

class MyWeChat:

    def __init__(self):
        pass

    def login(self, by="QR"):
        """登录微信，并将登录所需的QR code发送至master邮箱"""

        if by== "QR":
            itchat.get_QR("login_QR_CODE.png")
            print("123456")
            print(itchat.check_login())


def main():

    temp = MyWeChat()
    temp.login()


main()


if __name__ == "__main__":

    main()
    print("123")




