MONGO_URL = 'localhost'
MONGO_DB_FULL = 'bet365_full'
MONGO_DB_HALF = 'bet365_half'
MONGO_DB_DSFOOTBALL = 'dsfootball'


MONGO_TABLE_COLLECTIONS = 'collections'
MONGO_TABLE_BETS = 'bets'
MONGO_TABLE_SUCCESSES = 'successes'
MONGO_TABLE_BALANCE = 'balance'

URL = 'https://www.7788365365.com/#/HO/'
#URL = 'https://www.356884.com/zh-CHS/'
#URL = 'https://www.365-838.com/zh-CHS/'
refreshMin = 0
isChromeDriver = True
SpiderInterval = 3
ItemExchangeInterval = 2*60
BetSportItem = '足球'
BetSport = '滚球盘'
AsiaHalfItem = '上半場亞洲盤'
# ForbiddenLeagues_Half = ['80分钟', '19', '20', '女', '英格兰', '苏格兰', '威尔士', '爱尔兰', '巴西', '以色列', '阿根廷', '葡萄牙', '西班牙', '法国', '意大利', '德国', '伊朗', '哥斯达黎加', '希腊', '阿联酋 - 超级联赛', '香港超级联赛','阿尔及利亚杯', '欧洲友谊赛']
ForbiddenLeagues_Half = ['80分钟',]
ForbiddenMatches_Half = ['80分钟',]

ForbiddenLeagues_Full = ['80分钟', ]
ForbiddenMatches_Full = ['80分钟', ]

# full_lgt_min = 45
# full_lgt_max = 75
# full_lgt_max_1 = 80


RULE_FULL = {
    # 'initial_handicaps':{'1.5':{'min':1.0, 'max':2.5}, '2.5':{'min':1.61, 'max':2.5}} ,  #1---->2.75
    # 'initial_handicaps': {'2.5': {'min': 1.0, 'max': 1.57}, '3.5': {'min': 1.75 , 'max': 2.5}},   #3.0---->3.75
    'initial_handicaps': { '3.5': {'min': 1.825 , 'max': 2.15}},   #3.25---->3.5
    # 'initial_handicaps': {'2.5': {'min': 1.0, 'max': 1.57}, '3.5': {'min': 1.825 , 'max': 2.5}},   #3.0---->3.5
    # 'initial_ratios':{'weak':{'min':1.0, 'max':1.55}, 'strong':{'min':5, 'max':9.5}},  #1.25---->1 .75
    'initial_ratios':{'weak':{'min':1.0, 'max':1.55}, 'strong':{'min':4.2, 'max':50}},  #1.0---->xxx
    'initial_ratios_consider': True,
    'initial_minutes': {'min': 0, 'max': 0},
    'half_time': 45,
    'full_time': 90,
    'quick_goal_interval': 4.30,
    'all_bets_info': {
        'already_goals': {
            3: {'goal_cancel_forbidden': False, 'one_party_zero_allow': False, 'last_half_goals': [1, 2, 3],
                 'latest_goal_times': {'min': 0, 'max': 75}, 'two_goals_interval_min':4.30, 'allow_quick_goal_num':0,
                'when_last_half_goals': {
                    1:{
                        'all_goal_times':{
                            1:{'min': 0, 'max': 30}
                        }
                    },
                    2:{
                        'all_goal_times':{
                            1:{'min': 0, 'max': 30}
                        }
                    },
                    3:{
                        'all_goal_times':{
                            1:{'min': 0, 'max': 20}
                        }
                    }
                }
            },
            4: {'goal_cancel_forbidden': False, 'one_party_zero_allow':False, 'last_half_goals':[2, 3],
                 'latest_goal_times': {'min': 45, 'max': 75}, 'two_goals_interval_min':4.30, 'allow_quick_goal_num':1,
                'when_last_half_goals': {
                    2:{
                        'all_goal_times':{
                            1:{'min': 0, 'max': 30}
                        }
                    },
                    3:{
                        'all_goal_times':{
                            1:{'min': 0, 'max': 20}
                        }
                    }
                }
            },
            6: {'goal_cancel_forbidden': False, 'one_party_zero_allow': False, 'last_half_goals': [3, 4], 'first_goal_times':{'min': 0, 'max': 15},
                'latest_goal_times': {'min': 45, 'max': 75},
            },
            # 5: {'goal_cancel_forbidden': True, 'one_party_zero_allow': True, 'last_half_goals': [4],
            #     'latest_goal_times': {'min': 45, 'max': 80},
            #     # 'when_last_half_goals': {
            #     #     7: {
            #     #         'all_goal_times': {
            #     #             8: {'min': 45, 'max': 81},
            #     #         },
            #     #     },
            #     # }
            # },
        },
        'ready_bets':{
            '2':{'obey_any_success': True },
            '3':{'obey_any_success': True},
            '4':{'obey_any_success': True},
            '5':{'obey_any_success': True},
            '6':{'obey_any_success': True},
        }
    },
}


RULE_HALF = {
    # 'initial_handicaps':{'0.5':{'min':1.0, 'max':2.5}, '0.5,1.0':{'min':1.0, 'max':2.5},
                            #  '1':{'min':1.0, 'max':2.5}, '1.0':{'min':1.0, 'max':2.5},
                            #  '1.0,1.5': {'min': 2.05, 'max': 2.5}} ,
    # 'initial_handicaps':{'1.0,1.5': {'min': 1.5, 'max': 1.85}, '1.5':{'min':1.75, 'max':2.5}},   # 3.25--->3.75
    'initial_handicaps':{'1.0,1.5': {'min': 1.5, 'max': 1.85}, '1.5':{'min':1.90, 'max':2.5}},   # 3.25--->3.5
    # 'initial_ratios':{'weak':{'min':1.0, 'max':1.55}, 'strong':{'min':5, 'max':12}},
    'initial_minutes':{'min':0, 'max':0},
    'half_time':45,
    'quick_goal_interval':3.30,
    'all_bets_info':{
        'arleady_goals':{
                1:{ 'goal_cancel_forbidden':True,
                    'all_goal_times': {
                        1: {'min': 0, 'max': 6},
                    }
                },
        },
        'ready_bets':{
            '2':{'obey_any_success': True},
            '3':{'obey_any_success': True},
            '4':{'obey_any_success': True},
            '5':{'obey_any_success': True}
        }
    },
}




