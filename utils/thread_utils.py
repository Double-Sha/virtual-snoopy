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
    为任务job_func创建线程，传参job_func_args为job_func函数的传参
    :param job_func: 可调用对象或函数，指定的任务
    :param job_func_args: 对象的传参
    :param thread_name: 该任务的线程名
    :type job_func object
    :type job_func_args tuple
    :type thread_name str
    :return:
    """
    if job_func_args is not None:
        job_thread = threading.Thread(target=job_func, args=job_func_args)
    else:
        job_thread = threading.Thread(target=job_func)
    if thread_name is not None:
        job_thread.setName(thread_name)

    job_thread.start()