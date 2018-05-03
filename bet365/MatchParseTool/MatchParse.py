import hashlib
import re

class MatchParse(object):

    @classmethod
    # 获取当前比赛的时间
    def timeForMatch(cls, aMatch):
        timer = aMatch.find('.ipo-InPlayTimer').text()
        return timer.replace(':', '.') if timer else 0

    @classmethod
    # 获取当前比赛双方的名称
    def nameForMatch(cls, aMatch):
        items = aMatch.find('.ipo-TeamStack_TeamWrapper').items()
        names = [item.text() for item in items]
        return ('{} v {}'.format(names[0], names[1]))

    @classmethod
    # 获取当前比赛的Md5
    def md5ForNameOfMatch(cls, aMatch):
        name = cls.nameForMatch(aMatch)
        return cls.md5ForName(name)

    @classmethod
    # 获取比赛名的Md5
    def md5ForName(cls, name):
        m = hashlib.md5()
        m.update(name.encode('utf8'))
        return m.hexdigest()

    @classmethod
    # 比赛全场进球
    def fullHandicapForMatch(cls, aMatch):
        goals = aMatch.find('.gl-ParticipantCentered_Handicap').text()
        if goals:
            patt = re.compile(r"(\d+\.\d+)")
            return patt.search(goals).group()
        else:
            return 0

    # 上半场初盘
    @classmethod
    def halfHandicapForMatch(cls, aMatch):
        index = 0
        for item in aMatch.find('.ipo-MainMarketRenderer ').items():
            if index == 2:
                handicap = item.find('.gl-ParticipantCentered_Handicap').text()
                if handicap:
                    patt = re.compile(r"高于(.*)低于")
                    return patt.search(handicap).group(1).strip()
            index += 1
        return None

    #获取上半场赔率
    @classmethod
    def halfOddsForMatch(cls, aMatch):
        index = 0
        for item in aMatch.find('.ipo-MainMarketRenderer ').items():
            if index == 2:
                odds = item.find('.gl-ParticipantCentered_Odds').text()
                if odds:
                    patt = re.compile(r"(\d+\.\d+)")
                    return patt.search(odds).group()
            index += 1
        return 0

    @classmethod
    def halfRatioForMatch(cls, aMatch):
        index = 0
        for item in aMatch.find('.ipo-MainMarketRenderer ').items():
            if index == 0:
                odds = item.find('.gl-ParticipantCentered_Odds').text()
                if odds:
                    ratios = odds.split(' ')
                    return [float(ratios[0]), float(ratios[1])]
                    # return sorted([float(ratios[0]), float(ratios[1])])
            index += 1
        return None


    @classmethod
    # 比赛全场赔率
    def fullRatioForMatch(cls, aMatch):
        index = 0
        for item in aMatch.find('.ipo-MainMarketRenderer ').items():
            if index == 0:
                ratio = item.find('.gl-ParticipantCentered_Odds').text()
                if ratio:
                    if 'SP' in ratio:
                        return None
                    else:
                        ratios = ratio.split(' ')
                        return [float(ratios[0]), float(ratios[1])]
                        # return sorted([float(ratios[0]), float(ratios[1])])
        return None

    @classmethod
    # 获取赔率
    def fullOddsForMatch(cls, aMatch):
        for item in aMatch.find('.ipo-MainMarketRenderer').items():
            if item.find('.gl-ParticipantCentered_Handicap'):
                odds = item.find('.gl-ParticipantCentered_Odds').text()
                if odds:
                    return odds.split(' ')[0]
        return 0

    @classmethod
    # 当前比分
    def scoreForMatch(cls, aMatch):
        score = aMatch.find('.ipo-TeamPoints_TeamScore').text()
        return score.replace(' ', ':') if score else None