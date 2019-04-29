#encoding=utf-8
import time, os
from datetime import datetime
from Config.VarConfig import screenPicturesDir

# 获取当前的日期
def getCurrentDate():
    currentDate =time.strftime('%Y-%m-%d')
    return currentDate

# 获取当前的时间
def getCurrentTime():
    nowTime = time.strftime('%H-%M-%S')
    return nowTime

# 创建截图存放的目录
def createCurrentDateDir():
    dirName = os.path.join(screenPicturesDir, getCurrentDate())
    if not os.path.exists(dirName):
        os.makedirs(dirName)
    return dirName