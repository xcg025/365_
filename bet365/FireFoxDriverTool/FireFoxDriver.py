from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from enum import Enum, unique
import time
import traceback
import userConfig

class ByType(By):
    pass

class FireFoxDriver(object):
    def __init__(self, url):
        self.driver = webdriver.Chrome() if userConfig.isChromeDriver == True else webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.get(url)
        self.wait = WebDriverWait(self.driver, 1)

    #判断控件是否存在
    def isElementPresent(self, how, what):
        try:
            self.wait.until(EC.presence_of_element_located((how, what)))
            return True
        except Exception as e:
            return False

    def isElementVisible(self, how, what):
        try:
            self.wait.until(EC.visibility_of_element_located((how, what)))
            return True
        except Exception as e:
            return False


    #返回控件对应的文本
    def textForElement(self, how, what):
        isPresent = self.isElementPresent(how, what)
        if isPresent:
            element = self.driver.find_element(how, what)
            return element.text
        else:
            return None

    def text2forElement(self, element):
        if element:
            return element.text

    #返回元素
    def element(self, how, what):
        isPresent = self.isElementPresent(how, what)
        if isPresent:
            element = self.driver.find_element(how, what)
            return element
        else:
            return None

    def element2(self, how, what):
        element = self.driver.find_element(how, what)
        return element

    def elements(self, how, what):
        isPresent = self.isElementPresent(how, what)
        if isPresent:
            elements = self.driver.find_elements(how, what)
            return elements
        else:
            return None

    #设置控件内容
    def setElementText(self, how, what, text):
        element = self.element(how, what)
        if element != None:
            element.clear()
            element.send_keys(text)

    # def setElementText(self, element, text):
    #     if element != None:
    #         element.clear()
    #         element.send_keys(text)


    # 切换窗口
    def switch2frame(self, frame):
        self.driver.switch_to.frame(frame)

    #切出
    def switch2default(self):
        self.driver.switch_to.default_content()

    #点击控件
    def clickElement(self, how, what):
        try:
            isPresent = self.isElementPresent(how, what)
            if isPresent:
                element = self.driver.find_element(how, what)
                self.driver.execute_script("arguments[0].scrollIntoView();", element)
                ActionChains(self.driver).move_to_element(element).perform()
                ActionChains(self.driver).click(element).perform()
        except Exception as e:
            print(e)

    def click2Element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        ActionChains(self.driver).move_to_element(element).perform()
        ActionChains(self.driver).click(element).perform()

    def click3Element(self, element):
        ActionChains(self.driver).move_to_element(element).perform()
        ActionChains(self.driver).click(element).perform()

    def click4Element(self, how, what):
        element = self.driver.find_element(how, what)
        ActionChains(self.driver).move_to_element(element).perform()
        ActionChains(self.driver).click(element).perform()

    #关闭页面
    def closePages(self):
        currentHandle = self.driver.current_window_handle
        handles = self.driver.window_handles;
        for handle in handles:
            if handle != currentHandle:
                self.driver.switch_to_window(handle)
                time.sleep(1)
                self.driver.close()
        self.driver.switch_to_window(currentHandle)

    def refresh(self):
        self.driver.execute_script("location.reload()")
        # self.driver.refresh()


