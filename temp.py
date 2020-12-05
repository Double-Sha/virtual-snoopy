#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/5 20:20
# @Team : Private
# @Author : shasha.mao
# @Email : maoshasix@163.com
# @File : temp.py.py
# @Project : virtual-snoopy
# @Tool : PyCharm

# !/usr/bin/env python

import threading
from time import sleep, ctime

loops = [4, 2]


class ThreadFunc():
    def __init__(self, name):
        self.name = name

    def __call__(self):
        print("我得到了执行", self.name)


def main():
    print('程序开始于：', ctime())
    threads = []
    nloops = range(len(loops))

    for i in nloops:
        t = threading.Thread(target=ThreadFunc("tempname"), )# 传递一个可调用类的实例
        t.start()  # 开始所有的线程


    print('任务完成于：', ctime())


if __name__ == '__main__':
    main()