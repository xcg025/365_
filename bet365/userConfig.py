﻿MONGO_URL = 'localhost'
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
ForbiddenLeagues_Half = ['80分钟']
ForbiddenMatches_Half = ['80分钟']

ForbiddenLeagues_Full = ['80分钟', '女', '19']
ForbiddenMatches_Full = ['80分钟', '女', '19']

# full_lgt_min = 45
# full_lgt_max = 75
# full_lgt_max_1 = 80


RULE_FULL = {
    'initial_handicaps': {'2.5': {'min': 1.0, 'max': 1.57}, '3.5': {'min': 1.7, 'max': 2.5}},
    # 'initial_ratios':{'weak':{'min':1.0, 'max':1.55}, 'strong':{'min':5, 'max':12}},
    # 'initial_handicaps':{'1.5':{'min':1.0, 'max':2.5}, '2.5':{'min':1.61, 'max':2.5}} ,
    'initial_minutes': {'min': 0, 'max': 0},
    'half_time': 45,
    'full_time': 90,
    'quick_goal_interval': 4.30,
    'all_bets_info': {
        'arleady_goals': {
        5: {'allow_quick_goal_num': 1,'parties_goals_minus_min':1, 'goal_cancel_forbidden':True,  'latest_goal_times': {'min': 70, 'max': 80}, 'last_half_goals': {'min': 1, 'max': 3},
            'when_last_half_goals':{
                1: {'half_first_goal_time_max': 40 },  
                2: {'half_first_goal_time_max': 30, 'half_last_goal_time_min': 30, },   #上半场2个进球，则第2个进球时间必须大于30分钟
                3: {'half_first_goal_time_max': 15, 'half_last_goal_time_min': 30, 'next_last_two_interval_min': 10}, #上半场3个进球，则第3个进球时间必须大于30分钟且下半场两个进球间隔必须大于10分钟
                
            },
            },
        6: {'allow_quick_goal_num': 1, 'parties_goals_minus_min':1, 'goal_cancel_forbidden':True, 'latest_goal_times': {'min': 70, 'max': 80}, 'last_half_goals': {'min': 2, 'max': 4},
            'when_last_half_goals': {
                2: {'half_first_goal_time_max': 30, 'half_last_goal_time_min': 30, },  # 上半场2个进球，则第2个进球时间必须大于30分钟
                3: {'half_first_goal_time_max': 15, 'half_last_goal_time_min': 30,}, # 上半场3个进球，则第3个进球时间必须大于30分钟
                4: {'half_first_goal_time_max': 15, 'half_last_goal_time_min': 30, 'next_last_two_interval_min': 10, },  # 上半场4个进球，则第3个进球时间必须大于30分钟且下半场两个进球间隔必须大于10分钟
               
            },
            },
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


half_lgt_min = 29
half_lgt_max = 38

half_fgt_min = 0
half_fgt_max = 38

RULE_HALF = {
    # 'initial_handicaps':{'0.5':{'min':1.0, 'max':2.5}, '0.5,1.0':{'min':1.0, 'max':2.5},
                            #  '1':{'min':1.0, 'max':2.5}, '1.0':{'min':1.0, 'max':2.5},
                            #  '1.0,1.5': {'min': 2.05, 'max': 2.5}} ,
    'initial_handicaps':{'1.0,1.5': {'min': 1.5, 'max': 1.85}, '1.5':{'min':1.0, 'max':2.155},'2.0':{'min':1.0, 'max':2.5},'2':{'min':1.0, 'max':2.5}},
    # 'initial_ratios':{'weak':{'min':1.0, 'max':1.55}, 'strong':{'min':5, 'max':12}},
    'initial_minutes':{'min':0, 'max':0},
    'half_time':45,
    'quick_goal_interval':4,
    'all_bets_info':{
        'arleady_goals':{
                4:{'latest_goal_times':{'min':half_lgt_min, 'max':half_lgt_max}, 'first_goal_times':{'min':half_fgt_min, 'max':half_fgt_max}, 'allow_quick_goal_num':10},
                5:{'latest_goal_times':{'min':half_lgt_min, 'max':half_lgt_max}, 'first_goal_times':{'min':half_fgt_min, 'max':half_fgt_max}, 'allow_quick_goal_num':10},
                6:{'latest_goal_times':{'min':half_lgt_min, 'max':half_lgt_max}, 'first_goal_times':{'min':half_fgt_min, 'max':half_fgt_max}, 'allow_quick_goal_num':10},
                7:{'latest_goal_times':{'min':half_lgt_min, 'max':half_lgt_max}, 'first_goal_times':{'min':half_fgt_min, 'max':half_fgt_max}, 'allow_quick_goal_num':10},
        },
        'ready_bets':{
            '2':{'obey_any_success': True},
            '3':{'obey_any_success': True},
            '4':{'obey_any_success': True},
            '5':{'obey_any_success': True}
        }
    },
}




