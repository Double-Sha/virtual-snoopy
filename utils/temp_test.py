#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Team : PRA-BD
# @Author: shasha.mao
# @Date : 12/19/2020 1:35 PM
# @File : temp_test.py
# @Tool : PyCharm


from conf import email_config, title_config
from utils.email_utils import SnoopyMailBox
from jobs.car_numbers_statistic import CarNumberInGwmPrd

print(CarNumberInGwmPrd().to_excel(SnoopyMailBox, email_config))
