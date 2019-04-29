#coding=utf-8
from configparser import ConfigParser
from Config.VarConfig import desiredcapsFilePath
class ParseConfigFile(object):
    def __init__(self,path):
        self.cf=ConfigParser()
        self.cf.read(path)

    def getItemsSection(self,sectionName):
        optionsDict=dict(self.cf.items(sectionName))
        return optionsDict

    def getOptionVaule(self,sectionName,optionName):
        optionValue=self.cf.get(sectionName,optionName)
        return optionValue

if __name__ == '__main__':
    print(desiredcapsFilePath)
    pc=ParseConfigFile(desiredcapsFilePath)
    print(pc.getItemsSection("Desired_caps"))
    print(pc.getOptionVaule("Desired_caps","platformVersion"))