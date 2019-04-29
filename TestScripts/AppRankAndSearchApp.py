#coding=utf-8
from Action.PageAction import *
from Util.ParseExcel import ParseExcel
from Config.VarConfig import *
from Util.Log import logger
import traceback
from TestScripts.WriteResult import writeResult
from TestScripts.SearchApp import searchApp
def appRankAndSearchApp():
    try:
        excelObj = ParseExcel()
        excelObj.loadWorkBook(dataFilePath)
        caseSheet = excelObj.getSheetByName("测试用例")
        caseNum = excelObj.getRowsNumber(caseSheet)
        isExecuteCaseCols = excelObj.getColumn(caseSheet,testCase_isExecute)
        #记录需要执行的用例个数
        requiredCaseNum = 0
        #记录执行成功的用例个数
        successfulCaseNum = 0

        for idx,i in enumerate(isExecuteCaseCols[1:]):
            caseName = excelObj.getCellOfValue(caseSheet, rowNo = idx + 2, colsNo = testCase_testCaseName)
            logger.info("----------" + caseName)
            #测试用例sheet中第一行为标题，无须执行
            if i.value == "y":
                requiredCaseNum+=1
                caseRow = excelObj.getRow(caseSheet, idx + 2)
                frameworkName = caseRow[testCase_frameworkName - 1].value
                stepSheetName = caseRow[testCase_testStepSheetName - 1].value

                if frameworkName == "关键字":
                    logger.info("**********调用关键字驱动**********")
                    #根据用例的sheet名获取用例的sheet对象
                    stepSheet = excelObj.getSheetByName(stepSheetName)
                    #记录用例步骤的个数
                    stepNum = excelObj.getRowsNumber(stepSheet)
                    #记录用例步骤执行成功的个数
                    successfulStepNum = 0
                    for j in range(2, stepNum + 1):
                        #用例步骤中的第一行为标题，无须执行
                        stepRow = excelObj.getRow(stepSheet, j)
                        #获取用例步骤中描述
                        StepDescription = stepRow[caseStep_caseStepDescription-1].value
                        #获取函数名
                        keyWord = stepRow[caseStep_keyWord-1].value
                        print("keyWord = ", keyWord)
                        #获取操作元素的定位方式
                        locationType = stepRow[caseStep_locationType-1].value
                        #获取操作元素定位方式的表达式
                        locatorExpression = stepRow[caseStep_locatorExpression-1].value
                        #获取函数中的参数
                        operatorValue = stepRow[caseStep_operatorValue-1].value
                        #数值类数据从excel取出后为long型数据，转换为字符串，方便拼接
                        if isinstance(operatorValue, int):
                            operatorValue = str(operatorValue)
                        if keyWord  and locationType and locatorExpression and operatorValue:
                            step = keyWord + "('%s','%s','%s')" %(locationType, locatorExpression, operatorValue)
                        elif keyWord  and locationType and locatorExpression :
                            step = keyWord + "('%s','%s')" %(locationType, locatorExpression)
                        elif keyWord  and operatorValue :
                            step = keyWord + "('%s')" %operatorValue
                        elif keyWord:
                            step = keyWord + "()"
                        try:
                            #用例步骤执行执行成功，写入执行结果和日志
                            print(step)
                            eval(step)
                            successfulStepNum += 1
                            writeResult(excelObj, stepSheet, "Pass", j, "caseStep")
                            logger.info("执行步骤“%s”成功"%StepDescription)
                        except Exception as err:
                            #用例步骤执行执行成功
                            errPicPath = capture_screen()
                            errMsg = traceback.format_exc()
                            writeResult(excelObj, stepSheet, "Faild", j, "caseStep", errMsg = errMsg, errPicPath = errPicPath)
                            logger.error("执行步骤“%s”失败\n异常信息：%s" %(StepDescription, str(traceback.format_exc())))
                    if successfulStepNum == stepNum - 1:
                        successfulCaseNum += 1
                        writeResult(excelObj, caseSheet, "Pass", idx + 2, "testCase")
                        logger.info("用例“%s”执行成功" %caseName)
                    else:
                        writeResult(excelObj, caseSheet, "Faild", idx + 2, "testCase")
                        logger.info("用例“%s”执行失败" %caseName)
                elif frameworkName == "数据":
                    logger.info("**********调用数据驱动**********")
                    dataSourceSheetName = caseRow[testCase_dataSourceSheetName - 1].value
                    # print dataSourceSheetName,stepSheetName
                    stepSheet = excelObj.getSheetByName(stepSheetName)
                    dataSheet = excelObj.getSheetByName(dataSourceSheetName)
                    result = searchApp(excelObj, stepSheet, dataSheet)
                    if result:
                        successfulCaseNum += 1
                        writeResult(excelObj, caseSheet, "Pass",idx + 2,"testCase")
                        logger.info("用例“%s”执行成功" %caseName)
                    else:
                        writeResult(excelObj, caseSheet, "Faild", idx + 2, "testCase")
                        logger.info("用例“%s”执行失败" %caseName)
            else:
                # 清空不需要执行用例的执行时间和执行结果，
                writeResult(excelObj, caseSheet, "", idx + 2, "testCase")
                logger.info("用例“%s”被设置为忽略执行" % caseName)
        logger.info("共%s条用例，%s条需要被执行，本次执行通过%s条" % (caseNum - 1, requiredCaseNum, successfulCaseNum))
    except Exception as err:
        logger.error("驱动框架主程序发生异常\n异常信息：%s"% str(traceback.format_exc()))
if __name__ == '__main__':
    appRankAndSearchApp()