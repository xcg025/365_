from __future__ import division
import datetime
import userConfig
from MongoBetTool.MongoBet import MongoBet
import time
from LoggingTool.Logging import Logging


class Balance(object):
    def __init__(self, type):
        self.mongo = MongoBet(type)
        self.balance = self.mongo.queryBalance(userConfig.MONGO_TABLE_BALANCE)

    #更新目标值
    def updateBalance(self):
        start_date = datetime.datetime.strptime(self.balance['start_date'], '%Y-%m-%d %H:%M:%S')
        now_date = datetime.datetime.now()
        day_num = (now_date - start_date).days
        week_num = ((now_date - start_date).days) // 7 + 1
        self.balance['day_in_week'] = day_num % 7

        if week_num != self.balance['week_num']:
            self.balance['week_num'] = week_num
            for (times, data) in self.balance['cash'].items():
                if isinstance(data, dict):
                    data['original'] = data['now']
                    days_target = []
                    for day in range(7):
                       day_target = data['original'] * (1 + data['day_growth']*(day+1))
                       days_target.append(day_target)
                    data['days_target'] = days_target
        self.mongo.updateBalance(userConfig.MONGO_TABLE_BALANCE, self.balance)
        # Logging.info(u'设置days_target---{}'.format(self.balance))

    #赢
    def win(self, times):
        data = self.balance['cash'][times]
        data['now'] += (data['original']*data['ratio']*(float(times)-1))
        self.mongo.updateBalance(userConfig.MONGO_TABLE_BALANCE, self.balance)
        Logging.info(u'更新{}倍数据库---{}'.format(times, self.balance))

    #输
    def lose(self, times):
        data = self.balance['cash'][times]
        data['now'] -= (data['original'] * data['ratio'])
        self.mongo.updateBalance(userConfig.MONGO_TABLE_BALANCE, self.balance)
        Logging.info(u'更新{}倍数据库---{}'.format(times, self.balance))

    #回滚
    def rollback(self, times):
        data = self.balance['cash'][times]
        data['now'] -= (data['original'] * data['ratio'] * (float(times) - 1))
        self.mongo.updateBalance(userConfig.MONGO_TABLE_BALANCE, self.balance)
        # Logging.info(u'回滚数据库, {}'.format(self.balance))

    #获取下注金
    def get(self, times):
        data = self.balance['cash'][times]
        return data['original'] * data['ratio']

    #判断赔率所对应的目标值是否达到
    def isTargetAchieved(self, times):
        data = self.balance['cash'][times]
        day_in_week = self.balance['day_in_week']
        return data['now'] >= data['days_target'][day_in_week]


if __name__ == '__main__':

    # d1 = datetime.datetime(2017, 11, 29, 16, 0,0)
    d1 = datetime.datetime.strptime('2018-01-01 12:00:00', '%Y-%m-%d %H:%M:%S')
    # d2 = datetime.datetime.now()
    d2 = datetime.datetime.strptime('2018-01-08 12:00:00', '%Y-%m-%d %H:%M:%S')
    print(d2)
    day_num = (d2 - d1).days
    # week_num = ((now_date - start_date).days) // 7 + 1
    # self.balance['day_in_week'] = day_num % 7
    print(day_num % 7)

