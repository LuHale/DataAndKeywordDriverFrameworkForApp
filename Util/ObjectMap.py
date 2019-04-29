#encoding=utf-8
from selenium.webdriver.support.ui import WebDriverWait

# 获取单个页面元素对象
def getElement(driver, locationType, locatorExpression):
    try:
        element = WebDriverWait(driver, 30).until(
            lambda x: x.find_element(by=locationType, value = locatorExpression))
        return element
    except Exception as e:
        raise e

# 获取多个相同页面元素对象，以list返回
def getElements(driver, locationType, locatorExpression):
    try:
        elements = WebDriverWait(driver, 30).until(
            lambda x:x.find_elements(by=locationType, value = locatorExpression))
        return elements
    except Exception as e:
        raise e
