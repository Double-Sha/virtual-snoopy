#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/5 21:21
# @Team : Private
# @Author : shasha.mao
# @Email : maoshasix@163.com
# @File : thread_utils.py
# @Project : virtual-snoopy
# @Tool : PyCharm

import threading


def create_thread_for_task(job_func, job_func_args=None, thread_name=None):
    """
    为任务job_func创建一个线程，实现一个任务一个线程的功能

    :param job_func: 可调用对象或函数，指定的任务
    :param job_func_args: 可调用对象或函数对象的传参,例如("name", age),或者（"name",）
    :param thread_name: 该任务的线程名
    :type job_func object
    :type job_func_args tuple
    :type thread_name str
    """

    if job_func_args is not None:
        """
        Thread类的用法
        target是线程执行函数的名字，函数的名字后面不要带有小括号。
        args：执行函数所需要的参数，这个参数要以元组的形式去传，如果只有一个元素，后面不要忘了逗号。
        """
        job_thread = threading.Thread(target=job_func, args=job_func_args)
    else:
        job_thread = threading.Thread(target=job_func)
    if thread_name is not None:
        job_thread.setName(thread_name)
    job_thread.start()
