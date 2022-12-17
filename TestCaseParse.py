import os


class TestCaseParse(object):
    def __init__(self, inputScript, outputPath, webName):
        self.outputPath = outputPath
        self.webName = webName
        f_in = open(inputScript)
        self.fileLines = f_in.readlines()
        f_in.close()

        if not os.path.exists(outputPath + webName):
            os.mkdir(outputPath + webName)

    def getTestCaseList(self):
        testCaseList = []
        testCase = []

        iList = 0
        testCaseIndex = 0
        opr = 0
        appWaitActivity = ''
        for index, i in enumerate(self.fileLines):
            if 'desired_caps["appWaitActivity"]' in i or "desired_caps['appWaitActivity']" in i:
                # appWaitActivity = i.split(' = ')[1].strip()[1:-1]
                tempContent2 = i.split(' = ')[1].strip()[1:-1]
            if "# test case" in i:
                testCaseIndex = testCaseIndex + 1

            if "webdriver.Chrome" in i and i[0] != "#":
                opr = 0
                iList = iList + 1
                if iList == 1:
                    continue
                testCaseList.append(testCase)
                testCase = []

            else:
                if ("find_element" in i or "driver.back()" in i or "driver.press_keycode(" in i) and i[0] != "#":
                    opr = opr + 1
                    app = self.webName + "/"
                    if opr < 9:
                        screenshotPathInit = self.outputPath + app + str(iList - 1) + "/0" + str(opr) + ".png"
                        screenshotPath = self.outputPath + app + str(iList - 1) + "_/0" + str(opr) + ".png"
                        screenshotPathNext = self.outputPath + app + str(iList - 1) + "/0" + str(opr + 1) + ".png"

                        htmlPathInit = self.outputPath + app + str(iList - 1) + "/0" + str(opr) + ".html"
                        htmlPath = self.outputPath + app + str(iList - 1) + "_/0" + str(opr) + ".html"
                        htmlPathNext = self.outputPath + app + str(iList - 1) + "/0" + str(opr + 1) + ".html"

                    elif opr == 9:
                        screenshotPathInit = self.outputPath + app + str(iList - 1) + "/0" + str(opr) + ".png"
                        screenshotPath = self.outputPath + app + str(iList - 1) + "_/0" + str(opr) + ".png"
                        screenshotPathNext = self.outputPath + app + str(iList - 1) + "/" + str(opr + 1) + ".png"

                        htmlPathInit = self.outputPath + app + str(iList - 1) + "/0" + str(opr) + ".html"
                        htmlPath = self.outputPath + app + str(iList - 1) + "_/0" + str(opr) + ".html"
                        htmlPathNext = self.outputPath + app + str(iList - 1) + "/" + str(opr + 1) + ".html"
                    else:
                        screenshotPathInit = self.outputPath + app + str(iList - 1) + "/" + str(opr) + ".png"
                        screenshotPath = self.outputPath + app + str(iList - 1) + "_/" + str(opr) + ".png"
                        screenshotPathNext = self.outputPath + app + str(iList - 1) + "/" + str(opr + 1) + ".png"

                        htmlPathInit = self.outputPath + app + str(iList - 1) + "/" + str(opr) + ".html"
                        htmlPath = self.outputPath + app + str(iList - 1) + "_/" + str(opr) + ".html"
                        htmlPathNext = self.outputPath + app + str(iList - 1) + "/" + str(opr + 1) + ".html"

                    testAction = {'handle': i.strip('\n'), 'action': self.fileLines[index + 1],
                                  'widget': {}, 'screenshotPathInit': screenshotPathInit,
                                  'isHeuristic': 0,
                                  'screenshotPathNext': screenshotPathNext,
                                  'screenshotPath': screenshotPath, 'sIndex': 0,
                                  'needRepair': True, 'repairWidget': {},
                                  'isRepair': False, 'mustRepair': False,
                                  'testCaseFunctionIndex': testCaseIndex,
                                  'timeCost': 0, 'timeCostScreenshot': 0, 'timeCostMap': 0,
                                  'appWaitActivity': appWaitActivity, 'html': '',
                                  'htmlPathInit': htmlPathInit,
                                  'htmlPath': htmlPath, 'htmlPathNext': htmlPathNext, 'line': index + 1
                                  }

                    testCase.append(testAction)

                if "driver.tap" in i and i[0] != "#":
                    opr = opr + 1
                    app = self.webName + "/"
                    if opr < 9:
                        screenshotPathInit = self.outputPath + app + str(iList - 1) + "/0" + str(opr) + ".png"
                        screenshotPath = self.outputPath + app + str(iList - 1) + "_/0" + str(opr) + ".png"
                        screenshotPathNext = self.outputPath + app + str(iList - 1) + "/0" + str(opr + 1) + ".png"

                        htmlPathInit = self.outputPath + app + str(iList - 1) + "/0" + str(opr) + ".html"
                        htmlPath = self.outputPath + app + str(iList - 1) + "_/0" + str(opr) + ".html"
                        htmlPathNext = self.outputPath + app + str(iList - 1) + "/0" + str(opr + 1) + ".html"

                    elif opr == 9:
                        screenshotPathInit = self.outputPath + app + str(iList - 1) + "/0" + str(opr) + ".png"
                        screenshotPath = self.outputPath + app + str(iList - 1) + "_/0" + str(opr) + ".png"
                        screenshotPathNext = self.outputPath + app + str(iList - 1) + "/" + str(opr + 1) + ".png"

                        htmlPathInit = self.outputPath + app + str(iList - 1) + "/0" + str(opr) + ".html"
                        htmlPath = self.outputPath + app + str(iList - 1) + "_/0" + str(opr) + ".html"
                        htmlPathNext = self.outputPath + app + str(iList - 1) + "/" + str(opr + 1) + ".html"
                    else:
                        screenshotPathInit = self.outputPath + app + str(iList - 1) + "/" + str(opr) + ".png"
                        screenshotPath = self.outputPath + app + str(iList - 1) + "_/" + str(opr) + ".png"
                        screenshotPathNext = self.outputPath + app + str(iList - 1) + "/" + str(opr + 1) + ".png"

                        htmlPathInit = self.outputPath + app + str(iList - 1) + "/" + str(opr) + ".html"
                        htmlPath = self.outputPath + app + str(iList - 1) + "_/" + str(opr) + ".html"
                        htmlPathNext = self.outputPath + app + str(iList - 1) + "/" + str(opr + 1) + ".html"

                    tapX = int(i.strip().split("driver.tap([(")[1].split(",")[0])
                    tapY = int(i.strip().split("driver.tap([(")[1].split(",")[1].split(")")[0])

                    testAction = {'handle': i.strip('\n'), 'action': self.fileLines[index + 1],
                                  'widget': {}, 'screenshotPathInit': screenshotPathInit,
                                  'isHeuristic': 0,
                                  'screenshotPathNext': screenshotPathNext,
                                  'screenshotPath': screenshotPath, 'sIndex': 0,
                                  'needRepair': True, 'repairWidget': {},
                                  'isRepair': False, 'mustRepair': False,
                                  'testCaseFunctionIndex': testCaseIndex,
                                  'timeCost': 0, 'timeCostScreenshot': 0, 'timeCostMap': 0,
                                  'appWaitActivity': appWaitActivity, 'html': '', 'htmlPathInit': htmlPathInit,
                                  'htmlPath': htmlPath, 'htmlPathNext': htmlPathNext, 'line': index + 1, 'tapX': tapX,
                                  'tapY': tapY
                                  }

                    testCase.append(testAction)

                if "time.sleep" in i and i[0] != "#":
                    testAction = {'handle': i.strip('\n'), 'action': '',
                                  'widget': {}, 'screenshotPathInit': '',
                                  'screenshotPathNext': '', 'isHeuristic': 0,
                                  'screenshotPath': '', 'sIndex': -1,
                                  'needRepair': False, 'repairWidget': {},
                                  'isRepair': True, 'mustRepair': False,
                                  'testCaseFunctionIndex': testCaseIndex,
                                  'timeCost': 0, 'timeCostScreenshot': 0, 'timeCostMap': 0,
                                  'appWaitActivity': appWaitActivity, 'html': '', 'htmlPathInit': '',
                                  'htmlPath': '', 'htmlPathNext': '', 'line': index + 1}
                    testCase.append(testAction)

        testCaseList.append(testCase)

        for dicIndex in range(len(testCaseList)):
            if not os.path.exists(self.outputPath + self.webName + '/' + str(dicIndex)):
                os.mkdir(self.outputPath + self.webName + '/' + str(dicIndex))
                os.mkdir(self.outputPath + self.webName + '/' + str(dicIndex) + '_')
        return testCaseList
