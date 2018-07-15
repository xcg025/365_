from FireFoxDriverTool.FireFoxDriver import FireFoxDriver, ByType
import userConfig
import time
import datetime


class MatchOperation(object):
    browser = FireFoxDriver(userConfig.URL)
    time_now = datetime.datetime.now()

    # 返回网页源码
    @classmethod
    def pageSource(cls):
        return cls.browser.driver.page_source

    # 关闭弹出来的设置
    @classmethod
    def closeNotNow(cls):
        time.sleep(5)
        notNowBtn = cls.browser.element(ByType.CSS_SELECTOR, '.eba-AdvertWindow_NotNowBtnText')
        if notNowBtn != None:
            cls.browser.click3Element(notNowBtn)

    #关闭保持登录
    @classmethod
    def closeRemain(cls):
        remainBtn = cls.browser.element(ByType.CSS_SELECTOR, '.wl-InactivityAlert_Remain')
        if remainBtn != None:
            cls.browser.click3Element(remainBtn)

    @classmethod
    def closeRemain1(cls):
        remainBtn = cls.browser.element(ByType.CSS_SELECTOR, '.wl-ActivityLimitAlert_Button')
        if remainBtn != None:
            cls.browser.click3Element(remainBtn)

    # 刷新money
    @classmethod
    def refreshMoney(cls):
        cls.browser.clickElement(ByType.CSS_SELECTOR, '.hm-Balance')
        cls.browser.clickElement(ByType.CSS_SELECTOR, '.hm-BalanceDropDown_RefreshBalance')
        time.sleep(5)
        cls.browser.clickElement(ByType.CSS_SELECTOR, '.hm-Balance')

    # 获取金额
    @classmethod
    def getMoney(cls):
        money = cls.browser.textForElement(ByType.CSS_SELECTOR, '.hm-Balance')
        return money.split(' ')[0] if money != None else None

    #判断进球时间是否满足分布时间
    @classmethod
    def isGoalsTimeInDistribution(cls, goals_time, goals_distribution_time):
        goals_distribution_time_list = goals_distribution_time.split(',')
        range_list = []

        for gdt in goals_distribution_time_list:
            t_list = gdt.split('-')
            range_list.append(range(int(t_list[0]), int(t_list[1])))

        qualified_num = 0
        for range_ in range_list:
            for goal_time in goals_time:
                if int(goal_time) in range_:
                    qualified_num += 1
                    break
        return qualified_num == len(goals_distribution_time_list)


    # 处理随时变化的盘口
    @classmethod
    def procUnmatch(cls, goals):
        element = cls.browser.element(ByType.CSS_SELECTOR, '.bs-RemoveColumn_Button')
        handicap = cls.browser.textForElement(ByType.CSS_SELECTOR, '.bs-Selection_Handicap')
        if handicap != None and element != None:
            if (float(handicap) <= goals) or (float(handicap) >= goals + 1):
                cls.browser.click2Element(element)

    # 下注
    @classmethod
    def payForMatch(cls, names, times, goals, money):
        is_pay_success = False
        try:
            cls.switch2BetFrame()
            # 判断比赛有没有错乱的情况
            theNames = cls.browser.textForElement(ByType.XPATH, "//div[@class='bs-Selection']/div[3]")
            odds = cls.browser.textForElement(ByType.CSS_SELECTOR, '.bs-Odds')
            handicap = cls.browser.textForElement(ByType.CSS_SELECTOR, '.bs-Selection_Handicap')

            names_ok = (theNames != None and names == theNames)
            odds_ok = (odds != None and float(odds) >= float(times))
            handicap_ok = (handicap != None and isinstance(handicap,str) and "," not in handicap and ((float(handicap) > goals) and (float(handicap) < goals + 1)))

            if names_ok and odds_ok and handicap_ok:
                cls.browser.setElementText(ByType.XPATH, "//input[@class='stk bs-Stake_TextBox']", money)
                while ((cls.browser.isElementPresent(ByType.CSS_SELECTOR, '.bs-Footer') == True)):
                    # cls.procUnmatch(goals)
                    print('odds_ok--->{}, handicap_ok--->{}'.format(odds_ok, handicap_ok))
                    accept_btn_visible = cls.browser.isElementVisible(ByType.CSS_SELECTOR, '.bs-BtnAccept')
                    bet_btn_visible = cls.browser.isElementVisible(ByType.CSS_SELECTOR, '.bs-BtnHover')
                    print('accept_btn_visible={}, bet_btn_visible={}'.format(accept_btn_visible, bet_btn_visible))
                    if bet_btn_visible:
                        cls.browser.clickElement(ByType.CSS_SELECTOR, '.bs-BtnHover')
                        is_pay_success = True
                    elif accept_btn_visible:
                        cls.browser.clickElement(ByType.CSS_SELECTOR, '.bs-BtnAccept')
                        is_pay_success = False
                    time.sleep(2)
                    print('还没投完注')

                print('投注结束')
        except Exception as e:
            print('doPay has exception-----', e)
        finally:
            cls.switch2Default()
            return is_pay_success

    # 关闭投注窗口
    @classmethod
    def closeBetForMatch(cls):
        try:
            cls.switch2BetFrame()
            remove = cls.browser.element2(ByType.CSS_SELECTOR, '.bs-Header_RemoveAllLink')
            if remove != None:
                cls.browser.click3Element(remove)
                while (cls.browser.isElementPresent(ByType.CSS_SELECTOR, '.bs-Header_RemoveAllLink') == True):
                    pass
        except Exception as e:
            print('closeBetForMatch has exception-----', e)
        finally:
            cls.switch2Default()

    # 点击投注
    @classmethod
    def clickBetForMatch(cls, section, row):
        selector = 'div.ipo-Competition:nth-child(%d) > div:nth-child(3) > ' \
                   'div:nth-child(%d) > div:nth-child(1) > div:nth-child(2) >' \
                   ' div:nth-child(3) > div:nth-child(1)' % (section, row)
        element = cls.browser.element(ByType.CSS_SELECTOR, selector)
        text = cls.browser.text2forElement(element)
        if element != None and len(text) != 0:
            cls.browser.click2Element(element)
            try:
                cls.switch2BetFrame()
                while (cls.browser.isElementPresent(ByType.CSS_SELECTOR, '.bs-Header_RemoveAllLink') == False):
                    # print('clickBetForMatch is running')
                    pass
            except Exception as e:
                print('clickBetForMatch has exception-----', e)
            finally:
                cls.switch2Default()

    # 切换frame
    @classmethod
    def switch2BetFrame(cls):
        frame = cls.browser.element(ByType.CLASS_NAME, 'bw-BetslipWebModule_Frame')
        cls.browser.switch2frame(frame)

    @classmethod
    def switch2Default(cls):
        cls.browser.switch2default()

    # 是否是上半场亚洲盘
    @classmethod
    def isAsiaHalf(cls):
        cls.browser.closePages()
        xPathName = "//div[contains(@class,'ipo-InPlayClassificationMarketSelectorDropDown_Button')]"
        return cls.browser.textForElement(ByType.XPATH, xPathName) == userConfig.AsiaHalfItem

    # 切换到足球比赛
    @classmethod
    def switchToFootball(cls):
        cls.browser.closePages()
        time.sleep(1)
        xPathName = "//div[contains(@class,'ipo-ClassificationBar_ButtonContainer')]/div[2]/div[2]"
        cls.browser.clickElement(ByType.XPATH, xPathName)

    # 切换到上半场亚洲盘
    @classmethod
    def switchToAsiaHalf(cls):
        cls.browser.closePages()
        time.sleep(1)
        xPathName = "//div[contains(@class,'ipo-InPlayClassificationMarketSelectorDropDown_Button')]"
        cls.browser.clickElement(ByType.XPATH, xPathName)
        time.sleep(1)
        xPathName = "//div[contains(@class,'wl-DropDown_Inner ipo-InPlayClassificationMarketSelectorDropDown_Inner')]/div[2]"
        cls.browser.clickElement(ByType.XPATH, xPathName)

    @classmethod
    def switchToMainBk(cls):
        cls.browser.closePages()
        time.sleep(1)
        xPathName = "//div[contains(@class,'ipo-InPlayClassificationMarketSelectorDropDown_Button')]"
        cls.browser.clickElement(ByType.XPATH, xPathName)
        time.sleep(1)
        xPathName = "//div[contains(@class,'wl-DropDown_Inner ipo-InPlayClassificationMarketSelectorDropDown_Inner')]/div[1]"
        cls.browser.clickElement(ByType.XPATH, xPathName)

    # 当前选中的是否是足球
    @classmethod
    def isSelectFootball(cls):
        cls.browser.closePages()
        # time.sleep(1)
        xPathName = "//div[contains(@class,'ipo-ClassificationBarButtonBase_Selected')]/div[2]"
        return cls.browser.textForElement(ByType.XPATH, xPathName) == userConfig.BetSportItem

    #是否存在现场直播
    @classmethod
    def isGamesLiveClosed(cls):
        xPathName = "//div[contains(@class,'lv-ClosableTabView_Closed')]"
        return cls.browser.isElementPresent(ByType.XPATH, xPathName) == True

    #关闭现场直播
    @classmethod
    def closeGamesLive(cls):
        xPathName = "//div[contains(@class,'lv-ClosableTabView_Button ')]"
        cls.browser.clickElement(ByType.XPATH, xPathName)

    # 判断是否是足球项目
    @classmethod
    def hasFootball(cls):
        cls.browser.closePages()
        # time.sleep(1)
        xPathName = "//div[contains(@class,'ipo-ClassificationBar_ButtonContainer')]/div[2]/div[2]"
        return cls.browser.textForElement(ByType.XPATH, xPathName) == userConfig.BetSportItem

    # 禁止的联赛
    @classmethod
    def hasForbiddenLeague(self, aLeague, type):
        forbiddenLeagues = userConfig.ForbiddenLeagues_Half if type == 0 else userConfig.ForbiddenLeagues_Full
        for forbidden in forbiddenLeagues:
            if forbidden in aLeague:
                return True
        return False

    # 禁止的比赛
    @classmethod
    def hasForbiddenMatch(cls, names, type):
        forbiddenMatches = userConfig.ForbiddenMatches_Half if type == 0 else userConfig.ForbiddenMatches_Full
        for forbidden in forbiddenMatches:
            if forbidden in names:
                return True
        return False


    # 禁止的国家
    @classmethod
    def hasForbiddenCountries(cls, names):
        for forbidden in userConfig.ForbiddenCountries:
            if forbidden in names:
                return True
        return False

    # 刷新比赛
    @classmethod
    def refreshMatches(cls):
        time = datetime.datetime.now()
        min = (time - cls.time_now).seconds / 60
        minutes = round(min)
        if minutes >= userConfig.refreshMin:
            cls.browser.refresh()
            return True
        return False

    # 强制登录
    @classmethod
    def login(cls):
        try:
            while ((cls.browser.isElementPresent(ByType.CLASS_NAME, 'hm-Balance ') == False)):
                cls.browser.clickElement(ByType.ID, 'dv1')
                while (cls.browser.isElementPresent(ByType.XPATH,
                                                    "//div[@class='hm-Login_UserNameWrapper ']/input") == False):
                    pass

                time.sleep(2)
                cls.browser.click4Element(ByType.XPATH, "//div[@class='hm-Login_UserNameWrapper ']/input")
                cls.browser.setElementText(ByType.XPATH, "//div[@class='hm-Login_UserNameWrapper ']/input",
                                           "chenggang1986")
                time.sleep(2)
                cls.browser.click4Element(ByType.XPATH, "//div[@class='hm-Login_PasswordWrapper ']/input[1]")
                cls.browser.setElementText(ByType.XPATH, "//div[@class='hm-Login_PasswordWrapper ']/input[2]",
                                           "xuzhou139")
                cls.browser.click4Element(ByType.CSS_SELECTOR, '.hm-Login_LoginBtn ')
                while ((cls.browser.isElementPresent(ByType.CLASS_NAME, 'hm-Balance ') == False)):
                    pass

                elements = cls.browser.elements(ByType.CSS_SELECTOR, '.hm-BigButton ')
                for element in elements:
                    if cls.browser.text2forElement(element) == userConfig.BetSport:
                        cls.browser.click3Element(element)
        except Exception as e:
            print(str(e))
            cls.login()

