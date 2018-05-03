class Match(object):

    #比赛球队名
    @property
    def parties_name(self):
        return self._parties_name

    @parties_name.setter
    def parties_name(self, names):
        self._parties_name = names

    #比分
    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, score):
        self._score = score

    #最近进球时间
    @property
    def latest_goal_time(self):
        return self._latest_goal_time

    @latest_goal_time.setter
    def latest_goal_time(self, time):
        self._latest_goal_time = time

    #所有进球的时间，数组
    @property
    def goals_time(self):
        return self._goals_time

    @goals_time.setter
    def goals_time(self, times):
        if isinstance(times, list):
            self._goals_time = times
        else:
            raise ValueError('times is not a list')

    #赔率
    @property
    def odds_betted(self):
        return self._odds_betted

    @odds_betted.setter
    def odds_betted(self, odds):
        if isinstance(odds, dict):
            self._odds_betted = odds
        else:
            raise ValueError('odds is not a dict')

    #是否还可以下注
    @property
    def abandoned(self):
        return self._abandoned

    @abandoned.setter
    def abandoned(self, abandoned):
        self._abandoned = abandoned

    #盘口大小
    @property
    def handicap(self):
        return self._handicap

    @handicap.setter
    def handicap(self, handicap):
        self._handicap = handicap

    #比赛进行的时间
    @property
    def play_time(self):
        return self._play_time

    @play_time.setter
    def play_time(self, play_time):
        self._play_time = play_time

    #比赛开始时间
    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, time):
        self._start_time = time

    #比赛是否要删除
    @property
    def delete(self):
        return self._delete

    @delete.setter
    def delete(self, delete):
        self._delete = delete

    #id
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    #合并几分钟内的进球后数目
    @property
    def actual_goals(self):
        return self._actual_goals

    @actual_goals.setter
    def actual_goals(self, value):
        self._actual_goals = value

    # def __init__(self, cfg={}):
    #     self.cfg = cfg
    # def __setitem__(self, key, value):
    #     self.cfg[key] = value
    # def __getitem__(self, key):
    #     return self.cfg[key]
