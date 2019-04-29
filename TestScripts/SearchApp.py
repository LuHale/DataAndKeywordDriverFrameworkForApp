#coding=utf-8
from appium import webdriver
import time,traceback
from Util.ParseExcel import ParseExcel
from Config.VarConfig import *
from Util .Log import logger
from Action.PageAction import *
from TestScripts.WriteResult import writeResult
def searchApp(excelObj,stepSheet,dataSheet):
    try:
        dataIsExecuteCols=excelObj.getColumn(dataSheet,dataSource_isExecute)
        appNameCols=excelObj.getColumn(dataSheet,dataSource_appName)

        requiredDataNum=0
        successfulDataNum=0
        for idx,i in enumerate(dataIsExecuteCols[1:]):
            if i.value=="y":
                requiredDataNum+=1
                successfulStepNum=0
                logger.info("开始搜索APP“%s”"%(appNameCols[idx+1].value))
                stepNum=excelObj.getRowsNumber(stepSheet)
                for j in range(2,stepNum+1):
                    # 用例步骤中的第一行为标题，无须执行
                    stepRow = excelObj.getRow(stepSheet, j)
                    # 获取用例步骤中描述
                    stepDescription = stepRow[caseStep_caseStepDescription - 1].value
                    # 获取函数名
                    keyWord = stepRow[caseStep_keyWord - 1].value
                    # 获取操作元素的定位方式
                    locationType = stepRow[caseStep_locationType - 1].value
                    # 获取操作元素定位方式的表达式
                    locatorExpression = stepRow[caseStep_locatorExpression - 1].value
                    # 获取函数中的参数
                    operatorValue = stepRow[caseStep_operatorValue - 1].value
                    if isinstance(operatorValue, int):
                        # 数值类数据从excel取出后为long型数据，转换为字符串，方便拼接
                        operatorValue = str(operatorValue)
                    if operatorValue and operatorValue.isalpha():
                        # 如果operatorValue为字母时，则根据坐标在数据源工作表中取操作值
                        operatorValue=excelObj.getCellOfValue(dataSheet, coordinate=operatorValue+str(idx+2))
                    if keyWord and locationType and locatorExpression and operatorValue:
                        step = keyWord + "('%s','%s',u'%s')" % (locationType, locatorExpression, operatorValue)
                    elif keyWord and locationType and locatorExpression:
                        step = keyWord + "('%s','%s')" % (locationType, locatorExpression)
                    elif keyWord and operatorValue:
                        step = keyWord + "('%s')" % (operatorValue)
                    else:
                        step = keyWord + "()"
                    try:
                        # 用例步骤执行执行成功，写入执行结果和日志
                        print(step)
                        eval(step)
                        successfulStepNum += 1
                        logger.info(u"执行步骤“%s”成功" % stepDescription)
                    except Exception as e:
                        # 用例步骤执行执行失败
                        logger.error("执行步骤“%s”失败\n异常信息：%s" % (stepDescription, traceback.format_exc().decode("utf-8")))
                if successfulStepNum==stepNum-1:
                    writeResult(excelObj, dataSheet, "Pass", idx+2, "dataSheet")
                    successfulDataNum+=1
                else:
                    writeResult(excelObj, dataSheet, "Faild", idx+2, "dataSheet")
            else:
                #清空不需要执行的数据源中的执行时间和执行结果
                writeResult(excelObj, dataSheet, "", idx + 2, "dataSheet")
                logger.info("APP“%s”被设置为忽略执行" % appNameCols[idx+1].value)
        if requiredDataNum==successfulDataNum:
            return 1
        return 0

    except Exception as e:
        logger.info("数据驱动框架主程序发生异常\n异常信息:%s"%(traceback.format_exc().decode("utf-8")))


