from Bet.Bet365Full import Bet365Full
from Bet.Bet365Half import Bet365Half
import time
from datetime import datetime
import userConfig
from LoggingTool.Logging import Logging
from MatchOperationTool.MatchOperation import MatchOperation
import traceback


class BetSpider(object):
    def __init__(self, type):
        self.type = type
        self.login_time = datetime.now()
        self.bet = Bet365Half() if type == 0 else Bet365Full()
        self.exchange_num = 1
        MatchOperation.login()
        Logging.info(u'登陆成功')

    def process(self):
        try:
            while True:
                print('matchesProcess is running..., and time is %s' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
                if MatchOperation.isGamesLiveClosed() == False:
                    MatchOperation.closeGamesLive()
                MatchOperation.closeRemain()
                MatchOperation.closeRemain1()

                if MatchOperation.hasFootball() == False:
                    print('matchesProcess has no football games')
                else:
                    if MatchOperation.isSelectFootball():
                        if self.type == 1: #全场比赛
                            self.bet.procMatches()
                        else:    #半场比赛                            
                            if MatchOperation.isAsiaHalf():
                                self.bet.procMatches()
                            else:
                                MatchOperation.switchToAsiaHalf()
                    else:
                        MatchOperation.switchToFootball()
                time.sleep(userConfig.SpiderInterval)
        except Exception as e:
            # print('有异常抛出了哦！',e)
            traceback.print_exc()
            time.sleep(userConfig.SpiderInterval)
            self.process()



    def start(self):
        self.process()

