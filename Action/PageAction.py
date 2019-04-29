#coding=utf-8
from Util.GetDesiredcaps import getDesiredcaps
from Util.ObjectMap import *
from Util.DirAndTime import *
import time
from appium import webdriver

driver = ""
def open_app():
    global driver
    try:
        desired_caps = getDesiredcaps()
        driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    except Exception as e:
        raise e

def open_start_activity(appName, starActivityName):
    global driver
    try:
        driver.start_activity(appName, starActivityName)
    except Exception as e:
        raise

def quit_server():
    global  driver
    try:
        driver.quit()
    except Exception as e:
        raise e

def input_string(locationType, locatorExpression, inputContent):
    # 在页面输入框中输入数据
    global driver
    try:
        getElement(driver, locationType,locatorExpression).send_keys(inputContent)
    except Exception as e:
        raise e

def clear(locationType, locatorExpression, *arg):
    # 清除输入框默认内容
    global driver
    try:
        getElement(driver, locationType, locatorExpression).clear()
    except Exception as e:
        raise e

def click(locationType, locatorExpression, *arg):
    # 点击页面元素
    global driver
    try:
        getElement(driver, locationType, locatorExpression).click()
    except Exception as e:
        raise e

def assert_string_in_pagesource(assertString, *arg):
    # 断言界面源码是否存在某关键字或关键字符串
    global driver
    try:
        assert assertString in driver.page_source,"%s not found in page source!" %assertString
    except AssertionError as e:
        raise AssertionError(e)
    except Exception as e:
        raise e

def sleep(sleepSeconds, *arg):
    # 强制等待
    try:
        time.sleep(int(sleepSeconds))
    except Exception as e:
        raise e

def capture_screen(*args):
    # 截取屏幕图片
    global driver
    # 获取当期时间，精确到毫秒
    currTime = getCurrentTime()
    # 拼接异常图片保存的绝对路径及名称
    picNameAndPath =createCurrentDateDir() + "\\"+currTime+".png"
    try:
        # 截取屏幕图片，并保存为本地文件
        driver.get_screenshot_as_file(picNameAndPath)
    except Exception as e:
        raise e
    else:
        return picNameAndPath

def assertAPPList(locationType, locatorExpression,assertString):
    global driver
    try:
        assertStringList=assertString.split(",")
        elements=getElements(driver,locationType, locatorExpression)
        for element in elements[:3]:
            assert element.text in assertStringList
    except AssertionError as e:
        raise AssertionError(e)
    except Exception as e:
        raise e

def Enter():
    global driver
    try:
        driver.keyevent(66)
    except Exception as e:
        raise e