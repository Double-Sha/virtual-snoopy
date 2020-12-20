#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Team : PRA-BD
# @Author: shasha.mao
# @Date : 12/18/2020 4:51 PM
# @File : car_numbers_statistic.py
# @Tool : PyCharm

import pandas as pd
import pymysql
import datetime
import os
import sys
from utils.email_utils import SnoopyMailBox
from conf import email_config, mysql_config


class CarNumberInGwmPrd:
    """
    获取GWM生产环境最近7天的车辆数,包括车辆注册数,车辆实际接入数,车辆每日增长数，并邮件发送到指定账号
    """

    def __init__(self, mysql_config, past_days: int=10):
        """
        初始化类
        :param past_days: 相获取过去几天的注册车辆和接入车辆，默认10天
        :param mysql_config: mysql数据库配置类
        """
        self.past_days = past_days  # 输入为n,则常看过去n-3天的车辆接入情况
        self.today = None  # 今日日期
        self.mysql_config = mysql_config

    def get_date_of_past(self):
        """
        返回过去10天的凌晨时间点，包括今天，共10个时间点，如'2020-12-03 23:59:59'
        :return: past_days_list
        """

        date_list = [datetime.datetime.now() - datetime.timedelta(days=i) for i in range(0, self.past_days, 1)]
        past_days_list = ["'" + str(i)[0:10] + str(" 23:59:59") + "'" for i in date_list][::-1]
        self.today = past_days_list[-1][1:11]

        # 单引号也是时间的一部分
        return past_days_list

    def get_past_days_register_car_number(self):
        """
        连接mysql，获取GWM生产环境最近7天的车辆注册数,车辆每日增长数

        :return: DataFrame
        """

        # 连接mysql
        connect = pymysql.connect(host=self.mysql_config.host,
                                  user=self.mysql_config.user,
                                  password=self.mysql_config.passwd,
                                  database=self.mysql_config.database,
                                  charset=self.mysql_config.charset)

        cursor = connect.cursor(cursor=pymysql.cursors.DictCursor)

        # 参数定义
        start_date = "'2020-01-01 00:00:00'"
        past_days_list = self.get_date_of_past()  # 获取天数日期

        # 获取每日数据
        for i in range(1, len(past_days_list), 1):
            # sql语句编写
            column_name = "'截止%s(包含)的注册车辆总数'" % past_days_list[i][1:11]
            where_sql = "WHERE creation_date BETWEEN %s AND %s GROUP BY car_type;" % (start_date, past_days_list[i])
            sql = "SELECT car_type,COUNT(*) AS %s FROM t_car_info " % column_name + where_sql
            cursor.execute(sql)
            if i == 1:
                past_days_register_car_df = pd.DataFrame.from_dict(cursor.fetchall())
            else:
                past_days_register_car_df = pd.merge(past_days_register_car_df, pd.DataFrame.from_dict(cursor.fetchall()))

        # 车辆总数求和
        past_days_register_car_df.set_index("car_type", inplace=True)
        past_days_register_car_df.loc["五个车型总注册数据"] = past_days_register_car_df.apply(lambda x: x.sum(), axis="rows")
        past_days_register_car_df = past_days_register_car_df.T  # columns_name is cartype

        # 车辆每日增长数据数
        past_days_register_car_df["单日注册车辆增长数"] = past_days_register_car_df["五个车型总注册数据"] - past_days_register_car_df[
            "五个车型总注册数据"].shift(1)

        # 关闭数据库连接
        connect.close()

        return past_days_register_car_df.iloc[1:-1, :]

    def get_past_days_actual_car_number(self):
        """
        连接mysql，获取GWM生产环境最近7天的车辆接入数,车辆每日接入的增长数

        :return: DataFrame
        """

        # 连接mysql
        connect = pymysql.connect(host=self.mysql_config.host,
                                  user=self.mysql_config.user,
                                  password=self.mysql_config.passwd,
                                  database=self.mysql_config.database,
                                  charset=self.mysql_config.charset)
        cursor = connect.cursor(cursor=pymysql.cursors.DictCursor)

        # 参数定义
        start_date = "'2020-01-01 00:00:00'"
        past_days_list = self.get_date_of_past()  # 获取天数日期

        # 获取每日数据
        for i in range(1, len(past_days_list), 1):
            # sql语句编写
            column_name = "'截止%s(包含)的注册车辆总数'" % past_days_list[i][1:11]
            where_sql = "WHERE create_datetime BETWEEN %s AND %s GROUP BY car_type;" % (start_date, past_days_list[i])
            sql = "SELECT car_type,COUNT(*) AS %s FROM dw_common_carlocation_realtime " % column_name + where_sql
            cursor.execute(sql)
            if i == 1:
                past_days_actual_car_df = pd.DataFrame.from_dict(cursor.fetchall())
            else:
                past_days_actual_car_df = pd.merge(past_days_actual_car_df, pd.DataFrame.from_dict(cursor.fetchall()))

        past_days_actual_car_df = past_days_actual_car_df

        # 车辆总数求和
        past_days_actual_car_df.set_index("car_type", inplace=True)
        past_days_actual_car_df.loc["五个车型总接入数据"] = past_days_actual_car_df.apply(lambda x: x.sum(), axis="rows")
        past_days_actual_car_df = past_days_actual_car_df.T  # columns_name is cartype

        # 车辆每日增长数据数
        past_days_actual_car_df["单日接入车辆增长数"] = past_days_actual_car_df["五个车型总接入数据"] - past_days_actual_car_df[
            "五个车型总接入数据"].shift(1)

        # 关闭数据库连接
        connect.close()

        return past_days_actual_car_df.iloc[1:-1, :]

    def send_excel_to_mailbox(self, SnoopyMailBox, email_config):
        """
        获取GWM生产环境最近7天的车辆数,包括车辆注册数,车辆实际接入数,车辆每日增长数，并邮件发送到指定账号
        :param SnoopyMailBox: 邮箱类
        :param email_config: 邮箱配置信息，作为邮箱类对象生成的输入

        :return:
        """

        # 得出车辆注册数和接入数
        register_df = self.get_past_days_register_car_number()
        actual_df = self.get_past_days_actual_car_number()
        # register_df = util.TEMP_DF
        # actual_df = util.TEMP_DF

        # 写入文件
        sys.path[0] = os.path.dirname(__file__)
        excel_file_path = r"../resources/car_nunbers/GWM车辆注册数_车辆接入数_%s.xlsx" % self.today
        with pd.ExcelWriter(excel_file_path) as writer:
            register_df.to_excel(writer, sheet_name="注册总数")
            actual_df.to_excel(writer, sheet_name="接入总数")

        # 编辑邮件并发送
        subject = "近7天GWM生产环境车辆注册数和实际接入数"
        contents = "%s为%d，近七天，平均每日车辆注册数为%d\n%s为%d，近七天，平均每日车辆接入数为%d" % \
                   (register_df.index[-1], register_df.iloc[-1, -2], register_df.iloc[:, -1].mean(),
                    actual_df.index[-1], actual_df.iloc[-1, -2], actual_df.iloc[:, -1].mean())

        SnoopyMailBox(email_config).email_instance.send(to=email_config.car_numbers_info_to_list,
                                                        subject=subject,
                                                        contents=contents,
                                                        attachments=excel_file_path)


def main():
    CarNumberInGwmPrd(mysql_config, 10).send_excel_to_mailbox(SnoopyMailBox, email_config)


if __name__ == "__main__":
    main()

