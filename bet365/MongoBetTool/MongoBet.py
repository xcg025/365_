import pymongo
import userConfig
from LoggingTool.Logging import Logging

class MongoBet(object):
    def __init__(self, type):
        self.client = pymongo.MongoClient(userConfig.MONGO_URL)
        self.db = self.client[userConfig.MONGO_DB_HALF] if type == 0 else self.client[userConfig.MONGO_DB_FULL]

    # 保存到数据库中
    def saveMatch(self, tableName, aMatch):
        try:
            self.db[tableName].save(aMatch)
            return True
        except Exception as e:
            return False

    # 更新比赛信息
    def updateMatch(self, tableName, aMatch):
        try:
            self.db[tableName].save(aMatch)
            return True
        except Exception as e:
            return False

    # 删除比赛
    def deleteMatch(self, tableName, aMatch):
        try:
            self.db[tableName].delete_many({'_id': aMatch['_id']})
            return True
        except Exception as e:
            return False


    # 获取收藏中的比赛
    def queryMatches(self, tableName):
        matches = {}
        for aMatch in self.db[tableName].find():
            md5 = aMatch['_id']
            matches[aMatch['_id']] = aMatch
        return matches

    #更新统计数据
    def updateBalance(self, tableName, balance):
        try:
            self.db[tableName].save(balance)
            return True
        except Exception as e:
            return False

    #获取投注的统计数据
    def queryBalance(self, tableName):
        return self.db[tableName].find_one()



# if __name__ == '__main__':
#     mongo = MongoBet()
#     cash = {userConfig.BET_CASH_TWO_TIMES:200, userConfig.BET_CASH_THREE_TIMES:300, userConfig.BET_CASH_FOUR_TIMES:400, '_id':888888888}
#     mongo.updateCash(userConfig.MONGO_TABLE_CASH, cash)
