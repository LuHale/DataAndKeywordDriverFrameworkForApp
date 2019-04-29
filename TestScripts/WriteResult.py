#coding=utf-8
from Util.ParseExcel import ParseExcel
from Config.VarConfig import *
from Util.Log import logger
import traceback
import time

def writeResult(excelObj,sheet,testResult,rowNo,colNo,errMsg=None,errPicPath=None):
    #用例执行结束后，向excel中写入执行结果信息
    #通过测试结果信息，判断成功为绿色，失败为红色
    colorDict={"pass":"green","faild":"red","":None}
    #“测试用例”工作表和用例步骤工作表都有执行时间和执行结果，因此根据测试结果列的字典对象，区分是哪个工作表
    colsDict={
        "testCase":[testCase_runTime,testCase_testResult],
        "caseStep":[caseStep_runTime,caseStep_testResult],
        "dataSheet":[dataSource_runTime,dataSource_testResult]}
    try:
        # 在测试用例、测试步骤或数据源工作表，写入测试时间和测试结果
        if testResult=="":
            excelObj.writeCell(sheet,testResult, rowNo=rowNo, colsNo=colsDict[colNo][0],style=colorDict[testResult.lower()])
        else:
            excelObj.writeCellCurrentTime(sheet,rowNo=rowNo,colsNo=colsDict[colNo][0],style=colorDict[testResult.lower()])
        excelObj.writeCell(sheet,testResult,rowNo=rowNo,colsNo=colsDict[colNo][1],style=colorDict[testResult.lower()])
        #如果是测试步骤表，还要写入异常信息和截图
        if colNo=="caseStep":
            if errMsg and errPicPath:
                # 测试步骤执行失败，在测试步骤工作表中写入异常信息和截图
                excelObj.writeCell(sheet, errMsg, rowNo=rowNo, colsNo=caseStep_errMsg, style=colorDict[testResult.lower()])
                excelObj.writeCell(sheet, errPicPath, rowNo=rowNo, colsNo=caseStep_errPicPath, style=colorDict[testResult.lower()])
            else:
                # 测试步骤执行成功，在测试步骤工作表中清空异常信息和截图
                excelObj.writeCell(sheet, "", rowNo=rowNo, colsNo=caseStep_errMsg, style=colorDict[testResult.lower()])
                excelObj.writeCell(sheet, "", rowNo=rowNo, colsNo=caseStep_errPicPath, style=colorDict[testResult.lower()])
    except Exception as e:
        print("写入excel出错\n错误信息:%s："%(traceback.format_exc()))