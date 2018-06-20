from FireFoxDriverTool.FireFoxDriver import FireFoxDriver, ByType
from pyquery import PyQuery as pq
import time, json
import userConfig
from MongoBetTool.MongoBet import MongoBet
from Balance.Balance import Balance
from LoggingTool.Logging import Logging
from MatchParseTool.MatchParse import MatchParse
from MatchOperationTool.MatchOperation import MatchOperation
from MailTool.Mail import Mail
from DsFootballTool.DsFootball import DsFootball
from RedisTool.db_redis import RedisFactory


class Bet365(object):
    def __init__(self, type):
        self.type = type
        self.collections = dict()
        self.runnings = dict()
        self.deletes = dict()
        self.section = 0
        self.row = 0
        self.mongo = MongoBet(self.type)
        self.all = 0
        self.league = None
        self.balance = Balance(self.type)
        self.initSth()
        self.ds = DsFootball()
        self.redis = RedisFactory().create_redis('match')

    def initSth(self):
        self.balance.updateBalance()
        self.collections = self.mongo.queryMatches(userConfig.MONGO_TABLE_COLLECTIONS)

    def min_max_condition(self, conditions, condition):
        return condition >= conditions['min'] and condition <= conditions['max']


    def procMatches(self):
        pass

    #下注
    def doPay(self, names, times, goals):
        #刷新金额并获取投注前的金额
        # self.refreshMoney()
        # money_before = MatchOperation.getMoney()
        # 先关闭投注窗口
        MatchOperation.closeBetForMatch()
        #再打开投注窗口
        MatchOperation.clickBetForMatch(self.section, self.row)
        #下注
        money_bet = str(self.balance.get(times))
        is_pay_sucess = MatchOperation.payForMatch(names, times, goals, money_bet)

        # 如果金额发生变化，则认为投注成功
        # MatchOperation.refreshMoney()
        # money_after = MatchOperation.getMoney()
        # if money_after != money_before:
        if is_pay_sucess:
            md5 = MatchParse.md5ForName(names)
            self.collections[md5]['times_betteds'][times] = True
            self.collections[md5]['win_goals'] = (goals + 1)
            save_ok = self.mongo.saveMatch(userConfig.MONGO_TABLE_BETS, self.collections[md5])
            update_ok = self.mongo.updateMatch(userConfig.MONGO_TABLE_COLLECTIONS, self.collections[md5])
            bet_hint = '下之，times={}, rmb={}'.format(times, money_bet)
            if save_ok and update_ok:
                Logging.info('{}---{}'.format(bet_hint, self.collections[md5]))
                # Mail.send(bet_hint, json.dumps(self.collections[md5]['parties_name'], ensure_ascii=False))

            #关闭弹出来的设置
            MatchOperation.closeNotNow()

    #解析所有比赛
    def allMatches(self):
        doc = pq(MatchOperation.pageSource())
        allLeagues = doc('.ipo-Competition-open').items()
        self.section = 0
        self.all = 0
        for aLeague in allLeagues:
            self.section += 1
            everyLeagueName = aLeague.find('.ipo-CompetitionButton_NameLabelHasMarketHeading').text()
            #如果有禁止的比赛，则直接返回
            forbidden_ok = MatchOperation.hasForbiddenLeague(everyLeagueName, self.type)
            if forbidden_ok:
                continue

            self.league = everyLeagueName
            matches = aLeague.find('.ipo-Fixture_MainMarkets').items()
            self.row = 0
            for aMatch in matches:
                self.row += 1
                self.all += 1
                yield aMatch







