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
from WeekDayTool.WeekDay import WeekDay

class Bet365Full(Bet365):
    def __init__(self):
        super(Bet365Full, self).__init__(type=1)

    def procMatches(self):
        # print('满足条件的比赛顺序：','next_half-->next_half_combined_goals-->next_half_all_goals-->goals_distribution_time-->latest_goal_time-->handicap-->any_bet_succeed-->bet_times')
        print('目前进行的比赛数目：', self.all)
        print('目前关注的比赛数目：', len(self.collections))

        self.runnings.clear()
        self.runnings = {key: False for key in self.collections.keys()}

        for aMatch in self.allMatches():
            names = MatchParse.nameForMatch(aMatch)
            if MatchOperation.hasForbiddenMatch(names, 1) == True:
                continue

            md5 = MatchParse.md5ForNameOfMatch(aMatch)
            time_now = float(MatchParse.timeForMatch(aMatch))
            if md5 in self.collections:
                self.runnings[md5] = True

            # 如果进行中的比赛不在收藏中，则不解析其他的比赛信息 或者已经加入的赛前比赛
            if (time_now != 0 and md5 not in self.collections) or (time_now == 0 and md5 in self.collections):
                continue

            score = MatchParse.scoreForMatch(aMatch)
            handicap = MatchParse.fullHandicapForMatch(aMatch)
            odds = float(MatchParse.fullOddsForMatch(aMatch))
            ratios = MatchParse.fullRatioForMatch(aMatch)
            all_goals = int(score.split(':')[0]) + int(score.split(':')[1]) if score != None else 0

            # 筛选比赛
            time_ok = (time_now >= userConfig.RULE_FULL['initial_minutes']['min'] and \
                       time_now <= userConfig.RULE_FULL['initial_minutes']['max'])
            odds_ok = False
            if handicap in userConfig.RULE_FULL['initial_handicaps']:
                odds_ok = (odds >= userConfig.RULE_FULL['initial_handicaps'][handicap]['min'] and \
                           odds <= userConfig.RULE_FULL['initial_handicaps'][handicap]['max'])

            # sorted_ratio = sorted(ratios)
            # ratios_ok = (sorted_ratio[0] >= userConfig.RULE_FULL['initial_ratios']['weak']['min'] and
            #              sorted_ratio[0] <= userConfig.RULE_FULL['initial_ratios']['weak']['max']) and \
            #             (sorted_ratio[1] >= userConfig.RULE_FULL['initial_ratios']['strong']['min'] and \
            #              sorted_ratio[1] <= userConfig.RULE_FULL['initial_ratios']['strong']['max'])

            if time_ok and odds_ok:
                matchDict = {
                    'parties_name': names,
                    'score': score,
                    'last_half_score':None,
                    'goals_time': [],
                    'interval_goals_time':[],
                    'times_betteds': {'3':False, '2':False,},
                    'full_handicap': handicap,
                    'full_handicap_odds': odds,
                    'play_time': 0.0,
                    'start_time': None,
                    '_id': md5,
                    'ratios': ratios,
                    'league': self.league,
                    'all_goals': 0,
                    'win_goals': 0,
                    'half_rest': False,
                    'next_half': False,
                    'goal_cancel': False,
                    'any_bet_succeed': False,
                    'all_quick_goal_num':0,
                    'last_half_quick_goal_num':0,
                    'next_half_quick_goal_num':0,
                    'last_half_all_goals': 0,
                    'next_half_all_goals': 0,
                    'last_half_combined_goals':0,
                    'next_half_combined_goals':0,
                }

                #判断当前未收藏的比赛是否在ds中
                # if md5 not in self.collections and md5 in self.ds.fetch_all():
                if md5 not in self.collections:
                    self.collections[md5] = matchDict

            # 如果比赛正在进行且在收藏中
            if md5 in self.collections.keys() and time_now != 0:
                # 更新比赛开始的时间且加入数据库
                if self.collections[md5]['start_time'] == None:
                    if handicap in userConfig.RULE_FULL['initial_handicaps']:
                        odds_ok = (odds >= userConfig.RULE_FULL['initial_handicaps'][handicap]['min'] and \
                                   odds <= userConfig.RULE_FULL['initial_handicaps'][handicap]['max'])

                        ratios_ok = True
                        initial_ratios_consider = userConfig.RULE_FULL.get('initial_ratios_consider', False)
                        if initial_ratios_consider:
                            sorted_ratio = sorted(ratios)
                            ratios_ok = (sorted_ratio[0] >= userConfig.RULE_FULL['initial_ratios']['weak']['min'] and
                                         sorted_ratio[0] <= userConfig.RULE_FULL['initial_ratios']['weak']['max']) and \
                                        (sorted_ratio[1] >= userConfig.RULE_FULL['initial_ratios']['strong']['min'] and \
                                         sorted_ratio[1] <= userConfig.RULE_FULL['initial_ratios']['strong']['max'])

                        if odds_ok and ratios_ok:
                            pass
                            # self.mongo.saveMatch(userConfig.MONGO_TABLE_COLLECTIONS, self.collections[md5])
                        else:
                            self.collections.pop(md5)
                            continue
                    else:
                        self.collections.pop(md5)
                        continue

                    self.collections[md5]['start_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    if (self.mongo.saveMatch(userConfig.MONGO_TABLE_COLLECTIONS, self.collections[md5])):
                       pass

                # 是否是半场休息时间且删除不满足条件的比赛（包括删除数据库的比赛）
                if self.collections[md5]['play_time'] >= time_now and time_now == userConfig.RULE_FULL['half_time']:
                    #更新上半场休息判断和上半场所有的进球
                    self.collections[md5]['half_rest'] = True
                    self.mongo.saveMatch(userConfig.MONGO_TABLE_COLLECTIONS, self.collections[md5])
                    # if self.collections[md5]['last_half_all_goals'] not in userConfig.RULE_FULL['all_bets_info']['last_half_all_goals']:
                    #     self.mongo.deleteMatch(userConfig.MONGO_TABLE_COLLECTIONS, self.collections[md5])
                    #     self.collections.pop(md5)
                    #     continue

                #是否是进入下半场且保存下半场状态到数据库中
                if time_now != userConfig.RULE_FULL['half_time'] and self.collections[md5]['half_rest'] == True:
                    self.collections[md5]['half_rest'] = False
                    self.collections[md5]['next_half'] = True
                    self.mongo.saveMatch(userConfig.MONGO_TABLE_COLLECTIONS, self.collections[md5])

                # 更新当前的比赛时间
                self.collections[md5]['play_time'] = time_now

                #比赛进球或者进球取消
                if self.collections[md5]['score'] != score:  # 有进球的情况
                    self.collections[md5]['score'] = score

                    # 如果进球取消的情况
                    if self.collections[md5]['all_goals'] > all_goals:
                        self.collections[md5]['goal_cancel'] = True
                        self.collections[md5]['goals_time'].pop()
                        self.collections[md5]['interval_goals_time'].pop()
                    else:
                        goals_time = self.collections[md5]['goals_time']
                        quick_goal_interval = userConfig.RULE_FULL['quick_goal_interval']

                        #更新上半场合并进球的次数
                        if len(goals_time) != 0 and (time_now-goals_time[-1] <= quick_goal_interval) and self.collections[md5]['next_half'] == False:
                            self.collections[md5]['last_half_quick_goal_num'] += 1
                            self.collections[md5]['all_quick_goal_num'] += 1

                        #更新下半场合并进球的次数
                        if len(goals_time) != 0 and (time_now-goals_time[-1] <= quick_goal_interval) and self.collections[md5]['next_half'] == True:
                            self.collections[md5]['next_half_quick_goal_num'] += 1
                            self.collections[md5]['all_quick_goal_num'] += 1

                        if len(goals_time) != 0: #添加进球间隔时间
                            self.collections[md5]['interval_goals_time'].append(time_now-goals_time[-1])
                        self.collections[md5]['goals_time'].append(time_now)


                    # 更新上半场所有进球和合并进球
                    if self.collections[md5]['next_half'] == False:
                        self.collections[md5]['last_half_score'] = score
                        self.collections[md5]['last_half_all_goals'] = all_goals
                        self.collections[md5]['last_half_combined_goals'] = all_goals - self.collections[md5]['last_half_quick_goal_num']

                    #更新下半场所有进球和合并进球
                    if self.collections[md5]['next_half'] == True:
                        self.collections[md5]['next_half_all_goals'] = all_goals - self.collections[md5]['last_half_all_goals']
                        self.collections[md5]['next_half_combined_goals'] = all_goals - self.collections[md5]['last_half_all_goals'] - self.collections[md5]['next_half_quick_goal_num']

                    #更新所有进球
                    self.collections[md5]['all_goals'] = all_goals
                    self.mongo.updateMatch(userConfig.MONGO_TABLE_COLLECTIONS, self.collections[md5])

                    win_goals = self.collections[md5]['win_goals']
                    # 如果进球取消且已经下注了，则删除sucesses表的记录，同时投注金额也要回滚
                    if self.collections[md5]['goal_cancel'] == True and all_goals == win_goals - 1:
                        self.collections[md5]['any_bet_succeed'] = False
                        # betted_cancel = False
                        # # cancel_hint = '恼之， '
                        # for (times, betted) in self.collections[md5]['times_betteds'].items():  # 投注回滚
                        #     if betted == True:  # 已经下注的则要回滚
                        #         # self.balance.rollback(times)
                        #         betted_cancel = True
                        #         # cancel_hint = cancel_hint + times + 'times '
                        # if betted_cancel:
                        #     delete_ok = self.mongo.deleteMatch(userConfig.MONGO_TABLE_SUCCESSES, self.collections[md5])
                        #     save_ok = self.mongo.saveMatch(userConfig.MONGO_TABLE_COLLECTIONS, self.collections[md5])
                        #     # if delete_ok and save_ok:
                        #     #     Logging.info('{}---{}'.format(cancel_hint, self.collections[md5]))
                        #     #     Mail.send(cancel_hint, json.dumps(self.collections[md5]['parties_name'], ensure_ascii=False))
                    elif self.collections[md5]['goal_cancel'] == False and all_goals == win_goals:
                        self.collections[md5]['any_bet_succeed'] = True
                        continue
                        # # betted_success = False
                        # # win_hint = '得之， '
                        # for (times, betted) in self.collections[md5]['times_betteds'].items():  # 判断进球是否下注，且列出下注的倍数
                        #     if betted == True:
                        #         # self.balance.win(times)
                        #         betted_success = True
                        #         # win_hint = win_hint + times + '倍 '
                        # if betted_success:  # 进球且已经下注，则增加记录
                        #     # save_ok = self.mongo.saveMatch(userConfig.MONGO_TABLE_SUCCESSES, self.collections[md5])
                        #     # delete_ok = self.mongo.deleteMatch(userConfig.MONGO_TABLE_COLLECTIONS,
                        #     #                                    self.collections[md5])
                        #
                        #     # Mail.send(win_hint,json.dumps(self.collections[md5]['parties_name'], ensure_ascii=False))
                        #
                        #     # if delete_ok and save_ok:
                        #     #     Logging.info('{}---{}'.format(win_hint, self.collections[md5]))
                        #     continue

                print_need = True

                #是否是下半场
                if self.collections[md5]['next_half'] == False:
                    continue

                #进球数是否满足条件
                arleady_goals_dict = userConfig.RULE_FULL['all_bets_info']['already_goals']
                infos_all = arleady_goals_dict.get(all_goals, None)
                if infos_all == None:
                    #self.collections.pop(md5)
                    continue

                goals_time = self.collections[md5]['goals_time']
                last_half_all_goals = self.collections[md5]['last_half_all_goals']
                last_half_score = self.collections[md5]['last_half_score']

                # 上半场进球是否满足条件
                last_half_goals_all = infos_all.get('last_half_goals', None)
                if last_half_goals_all != None:
                    if (isinstance(last_half_goals_all, dict) and self.min_max_condition(last_half_goals_all, last_half_all_goals) == False) or \
                       (isinstance(last_half_goals_all, list) and last_half_all_goals not in last_half_goals_all):
                        self.collections.pop(md5)
                        continue

                #是否考虑周末的比赛
                # weekend_consider = infos_all.get('weekend_consider', False)
                # if weekend_consider and WeekDay.isWeekend():
                #     print('{}, weekend_consider_ok=no'.format(names))
                #     continue

                # 是否有球取消
                goal_cancel_forbidden = infos_all.get('goal_cancel_forbidden', False)
                if goal_cancel_forbidden and self.collections[md5]['goal_cancel']:
                    # print('{}, goal_cancel_ok=no'.format(names))
                    self.collections.pop(md5)
                    continue

                # 是否存在 X:0或0:X的情况
                one_party_zero_allow = infos_all.get('one_party_zero_allow', True)
                goal_a, goal_b = int(score.split(':')[0]), int(score.split(':')[1])
                if one_party_zero_allow == False and (goal_a * goal_b == 0):
                    self.collections.pop(md5)
                    continue

                # 最近进球时间是否满足条件
                latest_goal_times_dict = infos_all.get('latest_goal_times', None)
                if latest_goal_times_dict and self.min_max_condition(latest_goal_times_dict, float(goals_time[-1])) == False:
                    print('{}, latest_goal_time_ok=no'.format(names))
                    continue

                # 第一个进球时间是否满足条件
                first_goal_times_dict = infos_all.get('first_goal_times', None)
                if first_goal_times_dict and self.min_max_condition(first_goal_times_dict, float(goals_time[0])) == False:
                    print('{}, first_goal_time_ok=no'.format(names))
                    continue

                #判断两队进球比分相差是否小于x
                parties_goals_minus_dict = infos_all.get('all_parties_goals_minus', None)
                all_parties_goals_minus = abs(int(score.split(':')[0])-int(score.split(':')[1]))
                if parties_goals_minus_dict != None and self.min_max_condition(parties_goals_minus_dict, all_parties_goals_minus) == False:
                    print('{}, all_parties_goals_minus_ok=no'.format(names))
                    continue

                #判断最快进球数
                two_goals_interval_min = infos_all.get('two_goals_interval_min', -1)
                quick_goal_num = 0
                if two_goals_interval_min != -1:
                    for time_index in range(0, len(goals_time)):
                        if (time_index != len(goals_time)-1) and (goals_time[time_index+1]-goals_time[time_index]) < two_goals_interval_min:
                            quick_goal_num += 1

                allow_quick_goal_num = infos_all.get('allow_quick_goal_num', -1)
                if allow_quick_goal_num != -1 and quick_goal_num > allow_quick_goal_num:
                    print('{}, allow_quick_goal_num_ok=no'.format(names))
                    continue


                #附加条件
                when_last_half_goals_dict = infos_all.get('when_last_half_goals', None)
                if when_last_half_goals_dict and last_half_all_goals in when_last_half_goals_dict:
                    when_last_half_goals_info = when_last_half_goals_dict[last_half_all_goals]

                    # 各个进球时间是否满足条件
                    all_goal_times_dict = when_last_half_goals_info.get('all_goal_times', None)
                    all_goal_times_ok = True
                    if all_goal_times_dict:
                        for goal_num, times in all_goal_times_dict.items():
                            if self.min_max_condition(times, float(goals_time[goal_num - 1])) == False:
                                all_goal_times_ok = False
                                print('{}, {}_goal_time_ok=no'.format(names, goal_num))
                                break
                    if all_goal_times_ok == False:
                        continue

                    #上半场两队进球比分相差是否小于x
                    last_half_parties_goals_minus_dict = when_last_half_goals_info.get('last_half_parties_goals_minus', None)
                    last_half_parties_goals_minus = abs(int(last_half_score.split(':')[0]) - int(last_half_score.split(':')[1]))
                    if last_half_parties_goals_minus_dict != None and self.min_max_condition(last_half_parties_goals_minus_dict, last_half_parties_goals_minus) == False:
                        print('{}, last_half_parties_goals_minus_ok=no'.format(names))
                        continue

                    # 当前两队进球比分相差是否小于x
                    now_parties_goals_minus_dict = when_last_half_goals_info.get('now_parties_goals_minus', None)
                    now_parties_goals_minus = abs(int(score.split(':')[0]) - int(score.split(':')[1]))
                    if now_parties_goals_minus_dict != None and self.min_max_condition(now_parties_goals_minus_dict, now_parties_goals_minus) == False:
                        print('{}, now_parties_goals_minus_ok=no'.format(names))
                        continue


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

                #赔率是否满足条件
                if times_betted == None:
                    print('{}, bet_times={}->no'.format(names,odds))
                    continue

                # 是否遵守投注过就不再投注的原则
                obey_any_success = userConfig.RULE_FULL['all_bets_info']['ready_bets'][times_betted]['obey_any_success']
                if obey_any_success == True and self.collections[md5]['any_bet_succeed'] == True:
                    print('{}, any_bet_succeed->no'.format(names))
                    continue

                target_achieved_ok = (self.balance.isTargetAchieved(times_betted) == False)
                if target_achieved_ok:
                    self.doPay(names, times_betted, all_goals)
                else:
                    print('{}, target_achieved->no'.format(names))

        # 删除已经比赛完的
        for (md5_key, running) in self.runnings.items():
            if running == False and md5_key in self.collections:
                betted_lose = False
                lose_hint = '失之, '
                win_hint = '得之, '
                is_betted = False
                already_goals = self.collections[md5_key]['all_goals']
                win_goals = self.collections[md5_key]['win_goals']
                for (times, betted) in self.collections[md5_key]['times_betteds'].items():
                    if betted == True:
                        is_betted = True
                        if already_goals < win_goals:
                            self.balance.lose(times)
                            betted_lose = True
                            lose_hint = lose_hint + times + ' '
                        else:
                            self.balance.win(times)
                            betted_lose = False
                            win_hint = win_hint + times + ' '

                delete_ok = self.mongo.deleteMatch(userConfig.MONGO_TABLE_COLLECTIONS, self.collections[md5_key])
                if delete_ok and is_betted == True:
                    if betted_lose == True:
                        Mail.send(lose_hint, json.dumps(self.collections[md5_key]['parties_name'], ensure_ascii=False))
                    else:
                        self.mongo.saveMatch(userConfig.MONGO_TABLE_SUCCESSES, self.collections[md5_key])
                        Mail.send(win_hint, json.dumps(self.collections[md5_key]['parties_name'], ensure_ascii=False))
                self.collections.pop(md5_key)