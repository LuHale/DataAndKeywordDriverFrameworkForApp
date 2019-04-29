#coding=utf-8
from Config.VarConfig import desiredcapsFilePath
from Util.ParseConfigFile import ParseConfigFile
def getDesiredcaps():
    #获取desired_caps的配置信息
    pc=ParseConfigFile(desiredcapsFilePath)
    items=pc.getItemsSection("Desired_caps")
    desired_caps={
        'platformName':items['platformname'],
        'platformVersion':items['platformversion'],
        'deviceName': items['devicename'],
        'appPackage' :items['apppackage'],
        'appActivity': items['appactivity'],
        'autoAcceptAlerts':True,
        'unicodeKeyboard':True,
        'resetKeyboard':True,
        'noReset':True,
        'newCommandTimeout' : 6000
    }
    return desired_caps

if __name__ == '__main__':
    print(getDesiredcaps())
