from Bet.Bet365 import Bet365
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
from WeekDay.WeekDay import WeekDay
from datetime import datetime

class Bet365Half(Bet365):
    def __init__(self):
        super(Bet365Half, self).__init__(type=0)


    def procMatches(self):
        print('目前进行的比赛数目为：', self.all)
        print('目前收藏的比赛数目为：', len(self.collections))

        self.runnings.clear()
        self.runnings = {key: False for key in self.collections.keys()}

        for aMatch in self.allMatches():
            names = MatchParse.nameForMatch(aMatch)
            if MatchOperation.hasForbiddenMatch(names, 0) == True:
                continue


            md5 = MatchParse.md5ForNameOfMatch(aMatch)
            time_now = float(MatchParse.timeForMatch(aMatch))
            if md5 in self.collections:
                self.runnings[md5] = True

            # 如果进行中的比赛不在收藏中，则不解析其他的比赛信息 或者已经加入的赛前比赛
            if (time_now != 0 and md5 not in self.collections) or (time_now == 0 and md5 in self.collections):
                continue

            score = MatchParse.scoreForMatch(aMatch)
            handicap = MatchParse.halfHandicapForMatch(aMatch)
            odds = float(MatchParse.halfOddsForMatch(aMatch))
            ratios = MatchParse.halfRatioForMatch(aMatch)
            all_goals = int(score.split(':')[0]) + int(score.split(':')[1]) if score != None else 0

            # 初步筛选比赛
            time_ok = (time_now >= userConfig.RULE_HALF['initial_minutes']['min'] and \
                       time_now <= userConfig.RULE_HALF['initial_minutes']['max'])
            handicap_ok = handicap in userConfig.RULE_HALF['initial_handicaps']


            if time_ok and handicap_ok:  # 满足时间和赔率要求
            # if time_ok:
                matchDict = {
                    'parties_name': names,
                    'score': score,
                    'goals_time': [],
                    'times_betteds': { '2':False,'3':False,'4':False},
                    'half_handicap': handicap,
                    'half_handicap_odds': odds,
                    'play_time': 0.0,
                    'start_time': None,
                    '_id': md5,
                    'ratios': ratios,
                    'league': self.league,
                    'all_goals': 0,
                    'win_goals': 0,
                    'half_rest': False,
                    'next_half': False,
                    'goal_cancel':False,
                    'any_bet_succeed':False,
                    'all_quick_goal_num': 0,
                    'last_half_quick_goal_num': 0,
                }

                # 判断当前未收藏的比赛是否在ds中
                if md5 not in self.collections:
                    self.collections[md5] = matchDict

            # 如果比赛正在进行且在收藏中
            if md5 in self.collections.keys() and time_now != 0:
                # 更新比赛开始的时间且加入数据库
                if self.collections[md5]['start_time'] == None:
                    if handicap in userConfig.RULE_HALF['initial_handicaps'] and ratios != None:
                        odds_ok = (odds >= userConfig.RULE_HALF['initial_handicaps'][handicap]['min'] and \
                                   odds <= userConfig.RULE_HALF['initial_handicaps'][handicap]['max'])

                        # sorted_ratio = sorted(ratios)
                        # ratios_ok = (sorted_ratio[0] >= userConfig.RULE_HALF['initial_ratios']['weak']['min'] and
                        #              sorted_ratio[0] <= userConfig.RULE_HALF['initial_ratios']['weak']['max']) and \
                        #             (sorted_ratio[1] >= userConfig.RULE_HALF['initial_ratios']['strong']['min'] and \
                        #              sorted_ratio[1] <= userConfig.RULE_HALF['initial_ratios']['strong']['max'])

                        # if odds_ok and ratios_ok:
                        if odds_ok:
                            self.mongo.saveMatch(userConfig.MONGO_TABLE_COLLECTIONS, self.collections[md5])
                        else:
                            self.collections.pop(md5)
                            continue
                    else:
                        self.collections.pop(md5)
                        continue

                    self.collections[md5]['start_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    if (self.mongo.updateMatch(userConfig.MONGO_TABLE_COLLECTIONS, self.collections[md5])):
                        pass

                # 是否是半场休息时间
                if self.collections[md5]['play_time'] >= time_now and time_now == userConfig.RULE_HALF['half_time']:
                    self.collections[md5]['half_rest'] = True
                    self.mongo.saveMatch(userConfig.MONGO_TABLE_COLLECTIONS, self.collections[md5])

                # # 是否是进入下半场
                # if time_now != userConfig.RULE_HALF['half_time'] and self.collections[md5]['half_rest'] == True:
                #     self.collections[md5]['half_rest'] = False
                #     self.collections[md5]['next_half'] = True
                #     self.mongo.saveMatch(userConfig.MONGO_TABLE_SUCCESSES, self.collections[md5])

                # 更新当前的比赛时间
                self.collections[md5]['play_time'] = time_now
                if self.collections[md5]['score'] != score:  # 有进球的情况
                    self.collections[md5]['score'] = score
                    # 如果进球取消的情况
                    if self.collections[md5]['all_goals'] > all_goals:
                        self.collections[md5]['goal_cancel'] = True
                        self.collections[md5]['goals_time'].pop()
                    else:
                        goals_time = self.collections[md5]['goals_time']
                        quick_goal_interval = userConfig.RULE_HALF['quick_goal_interval']


                        # 更新上半场合并进球的次数
                        if len(goals_time) != 0 and (time_now - goals_time[-1] <= quick_goal_interval):
                            self.collections[md5]['last_half_quick_goal_num'] += 1
                            self.collections[md5]['all_quick_goal_num'] += 1

                        self.collections[md5]['goals_time'].append(time_now)

                    self.collections[md5]['all_goals'] = all_goals
                    self.mongo.updateMatch(userConfig.MONGO_TABLE_COLLECTIONS, self.collections[md5])

                    win_goals = self.collections[md5]['win_goals']
                    # 如果进球取消且已经下注了，则删除sucesses表的记录，同时投注金额也要回滚
                    if self.collections[md5]['goal_cancel'] == True and all_goals == win_goals - 1:
                        self.collections[md5]['any_bet_succeed'] = False
                        betted_cancel = False
                        cancel_hint = '恼之， '
                        for (times, betted) in self.collections[md5]['times_betteds'].items():  # 投注回滚
                            if betted == True:  # 已经下注的则要回滚
                                self.balance.rollback(times)
                                betted_cancel = True
                                cancel_hint = cancel_hint + times + 'times '
                        if betted_cancel:
                            delete_ok = self.mongo.deleteMatch(userConfig.MONGO_TABLE_SUCCESSES,
                                                               self.collections[md5])
                            save_ok = self.mongo.saveMatch(userConfig.MONGO_TABLE_COLLECTIONS,
                                                           self.collections[md5])
                            if delete_ok and save_ok:
                                Logging.info('{}---{}'.format(cancel_hint, self.collections[md5]))
                                Mail.send(cancel_hint, json.dumps(self.collections[md5]['parties_name'], ensure_ascii=False))
                    elif self.collections[md5]['goal_cancel'] == False and all_goals == win_goals:
                        self.collections[md5]['any_bet_succeed'] = True
                        betted_success = False
                        win_hint = '得之， '
                        for (times, betted) in self.collections[md5]['times_betteds'].items():  # 判断进球是否下注，且列出下注的倍数
                            if betted == True:
                                self.balance.win(times)
                                betted_success = True
                                win_hint = win_hint + times + 'times '
                        if betted_success:  # 进球且已经下注，则增加记录
                            save_ok = self.mongo.saveMatch(userConfig.MONGO_TABLE_SUCCESSES, self.collections[md5])
                            delete_ok = self.mongo.deleteMatch(userConfig.MONGO_TABLE_COLLECTIONS,
                                                               self.collections[md5])
                            if delete_ok and save_ok:
                                Logging.info('{}---{}'.format(win_hint, self.collections[md5]))
                                Mail.send(win_hint, json.dumps(self.collections[md5]['parties_name'], ensure_ascii=False))
                            continue

                # 是否在规定的时间内满足进球数
                if all_goals not in userConfig.RULE_HALF['all_bets_info']['arleady_goals']:
                    continue

                infos_all = userConfig.RULE_HALF['all_bets_info']['arleady_goals'][all_goals]
                goals_time = self.collections[md5]['goals_time']

                # 是否存在 X:0或0:X的情况
                one_party_zero = infos_all.get('one_party_zero', False)
                goal_a, goal_b = int(score.split(':')[0]), int(score.split(':')[1])
                if one_party_zero and (goal_a * goal_b != 0):
                    self.collections.pop(md5)
                    continue

                # 最快进球数
                two_goals_interval_min = infos_all.get('two_goals_interval_min', -1)
                quick_goal_num = 0
                if two_goals_interval_min != -1:
                    for time_index in range(0, len(goals_time)):
                        if (time_index != len(goals_time) - 1) and (goals_time[time_index + 1] - goals_time[time_index]) < two_goals_interval_min:
                            quick_goal_num += 1

                allow_quick_goal_num = infos_all.get('allow_quick_goal_num', -1)
                if allow_quick_goal_num != -1 and quick_goal_num > allow_quick_goal_num:
                    print('{}, allow_quick_goal_num_ok=no'.format(names))
                    continue

                # 是否有球取消
                goal_cancel_forbidden = infos_all.get('goal_cancel_forbidden', False)
                if goal_cancel_forbidden and self.collections[md5]['goal_cancel']:
                    print('{}, goal_cancel_ok=no'.format(names))
                    continue

                #各个进球时间是否满足条件
                all_goal_times_dict = infos_all.get('all_goal_times', None)
                all_goal_times_ok = True
                if all_goal_times_dict:
                    for goal_num, times in all_goal_times_dict.items():
                        if self.min_max_condition(times, float(goals_time[goal_num-1])) == False:
                            all_goal_times_ok = False
                            print('{}, {}_goal_time_ok=no'.format(names, goal_num))
                            break
                if all_goal_times_ok == False:
                    continue

                #---------------------以下代码可以不动------------------------
                # 投注的进球数是否满足条件
                handicap_now_ok = (handicap != None and isinstance(handicap, str) and "," not in handicap and ((float(handicap) > all_goals) and (float(handicap) < all_goals + 1)))
                if handicap_now_ok == False:
                    print('{}, handicap={}->no'.format(names, handicap))
                    continue

                times_betted = None
                for (key, val) in self.collections[md5]['times_betteds'].items():
                    if odds >= float(key) and val == False:
                        times_betted = key
                        break

                # 赔率是否满足条件
                if times_betted == None:
                    print('names={}, bet_times={}->no'.format(names, odds))
                    continue

                #是否遵守投注过就不再投注的原则
                obey_any_success = userConfig.RULE_HALF['all_bets_info']['ready_bets'][times_betted]['obey_any_success']
                if obey_any_success == True and self.collections[md5]['any_bet_succeed'] == True:
                    # print('names={},all_goals->yes,handicap->yes,latest_goal_time->yes,bet_times->no, any_bet_succeed->no'.format(names))
                    continue

                # #是否是弱队先进球
                # strong_team_first_goal = False
                # original_ratios = self.collections[md5]['ratios']
                # if original_ratios != None and ratios != None:
                #     if (original_ratios[0]-original_ratios[1]) * (ratios[0]-ratios[1]) > 0:
                #         strong_team_first_goal = True

                # if strong_team_first_goal == False:
                #     print('names={},all_goals->yes,handicap->yes,latest_goal_time->yes,bet_times=->yes,bet_minute->yes,strong_team_first_goal->no'.format(names))
                #     continue

                target_achieved_ok = (self.balance.isTargetAchieved(times_betted) == False)
                if target_achieved_ok:
                    self.doPay(names, times_betted, all_goals)
                else:
                    print('names={},target_achieved->no'.format(names))


        # 删除已经比赛完的
        for (md5_key, running) in self.runnings.items():
            if md5_key in self.collections and (self.collections[md5_key]['half_rest'] == True or running == False):
                betted_lose = False
                lose_hint = '失之， '
                already_goals = self.collections[md5_key]['all_goals']
                win_goals = self.collections[md5_key]['win_goals']
                for (times, betted) in self.collections[md5_key]['times_betteds'].items():
                    if betted == True and already_goals < win_goals:
                        self.balance.lose(times)
                        betted_lose = True
                        lose_hint = lose_hint + times + 'times '
                #
                delete_ok = self.mongo.deleteMatch(userConfig.MONGO_TABLE_COLLECTIONS, self.collections[md5_key])
                if delete_ok:
                    if betted_lose == True:
                        Logging.info('{}---{}'.format(lose_hint, self.collections[md5_key]))
                        Mail.send(lose_hint, json.dumps(self.collections[md5_key]['parties_name'], ensure_ascii=False))
                    else:
                        pass
                        # Logging.info('比赛结束,删除比赛---{}'.format(self.collections[md5_key]))
                self.collections.pop(md5_key)
