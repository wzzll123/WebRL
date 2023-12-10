# coding:utf-8
import time

import TestCaseParse
import RecordScreenAndWidght
import RepairWeb
import shelve
from datetime import datetime
import os


class TestRepairRunner:
    def __init__(self,testName,url,newUrl,repairMode,speedMode=True,tool='WebRL',
                 chromeDriverPath='/Users//Desktop/chromedriver', theta_dom=0.7, theta_image=0,theta_combine=0):
        self.rootPath = os.getcwd()

        self.webName = testName
        self.functionName = testName
        self.url = url
        self.newUrl = newUrl
        # self.rootPath = rootPath
        self.tool = tool
        self.chromeDriverPath = chromeDriverPath
        # self.outputPath = self.rootPath + tool + '_output/'
        self.outputPath = os.path.join(self.rootPath, tool + '_output/')
        self.enableHeuristic = True
        self.webScript = os.path.join(self.rootPath, 'webTestScript', self.functionName + '.py')
        # self.webScript = self.rootPath + 'webTestScript/' + self.functionName + '.py'
        self.repairMode=repairMode
        self.speedMode=speedMode
        self.create_folder()
        self.theta_dom=theta_dom
        self.theta_image=theta_image
        self.theta_combine=theta_combine
    def create_folder(self):
        if not os.path.exists(self.outputPath):
            os.mkdir(self.outputPath)
        if not os.path.exists(self.outputPath + self.webName + '/'):
            os.mkdir(self.outputPath + self.webName + '/')
    def tracer(self):
        # db for the based version is fixed in guider
        dbName = self.outputPath + self.webName + '/' + 'testOldVersion' + '.db'
        s = shelve.open(dbName)

        # timeCostLog = Logger.Logger(outputPath + webName + '/' + 'timeTotalCost.log')
        timeBefore = datetime.now()
        # cache test case information
        self.sBridge = {}

        if 'testCaseList' in s:
            testCaseList=s["testCaseList"]
            self.testCaseList = testCaseList
            s.close()

        else:
            # test Case  recognize
            testParse = TestCaseParse.TestCaseParse(self.webScript, self.outputPath, self.webName)
            testCaseList = testParse.getTestCaseList()
            self.testCaseList=testCaseList

            s['testCaseList'] = testCaseList
            recordScreenWidget = RecordScreenAndWidght.RecordScreenAndWidget(testCaseList,self.url,self.chromeDriverPath)
            recordScreenWidget.instrumentDriver()

            timeAfter = datetime.now()
            deltaTime = (timeAfter - timeBefore).seconds + (timeAfter - timeBefore).microseconds / 1000000.0
            # todo timeCostLog.debug("record for version N:"+str(deltaTime/60.0))
            # give label for each screen

            # htmlLabel = ImageLabel.ImageLabel(testCaseList)
            # htmlLabel.getHtmlLabel()
            # sBridge = htmlLabel.getSBridge()

            timeAfterLabel = datetime.now()
            deltaTime = (timeAfterLabel - timeAfter).seconds + (timeAfterLabel - timeAfter).microseconds / 1000000.0
            # timeCostLog.debug("Image label for version N:" + str(deltaTime / 60.0))
            # timeCostLog.debug("Image map for version N:" + str(Map.Map.timeCostForMap/ 60.0))
            # timeCostLog.debug("Image ocr for version N:" + str(Image_beifen.Image.timeCostForOCR / 60.0))

            s['testCaseList'] = testCaseList
            s.close()

#raw_input("1.Assure the based version is uninstalled, and the updated version is installed; 2.Click on the enter button in your terminal; 3. Once the app is successfully started, manually set the app in the target page.")

    def run_test_repair(self):
        print ('\nprocess 2----repair the broken tests in the updated version n+1; once the app is started, manually set the app into the target page.\n')

        repair = RepairWeb.RepairWeb(self.testCaseList,
                                           self.outputPath + self.webName + '/repairedScript.py', self.sBridge, self.webName, self.outputPath,self.newUrl,
                                           self.enableHeuristic,self.chromeDriverPath,self.repairMode,self.speedMode,self.theta_dom,self.theta_image,self.theta_combine)
        repair.repair()

    def run_trace_repair(self):
        start = time.time()
        self.tracer()
        end = time.time()
        print("trace time: " + str(end - start))
        self.run_test_repair()
