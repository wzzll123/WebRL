# -*- coding: utf-8 -*-
import json
import pickle
import subprocess
from functools import wraps

import xpathProcess

success = True

import ImageUtil

from selenium import webdriver
import time
from PIL import Image
import RecordScreenAndWidght
import os
import base64
import htmlMatch
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains


class RepairWeb():
    globalSuccessList = []
    globalFailList = []

    candidatesUpperBound = 5

    def __init__(self, testCaseList, repairScriptPath, sBridge, webName, output, newUrl, enableHeuristic,
                 chromeDriverPath, repairMode, speedMode, theta_dom=0.7, theta_image=0.6, theta_combine=3):
        self.outputDir = output
        self.testCaseList = testCaseList
        self.repairedScript = repairScriptPath
        self.webName = webName
        self.newUrl = newUrl
        self.chromeDriverPath = chromeDriverPath
        self.repairMode = repairMode
        self.sleepTime = 0
        self.enableHeuristic = enableHeuristic
        self.cachedDB = output + '/' + self.newUrl.replace('/', '-') + 'xpath2loc' + '.pkl'
        self.scaleRatio = 1
        self.speedMode = speedMode
        self.generatedScriptPath = output + webName + '/repaired.txt'
        self.theta_dom = theta_dom
        self.theta_image = theta_image
        self.theta_combine = theta_combine

    def calculate_time(place=2):
        '''计算函数运行时间装饰器

        :param place: 显示秒的位数，默认为2位
        '''

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                beg = time.time()
                f = func(*args, **kwargs)
                end = time.time()
                s = '{}()：{:.%sf} s' % place
                print(s.format(func.__name__, end - beg))
                return f

            return wrapper

        return decorator

    # 遍历待修复的test cases， 对每一个test case 尝试修复
    def repair(self):
        repairedScript = open(self.repairedScript, 'w')
        repairedScript.write("import time\nfrom selenium import webdriver\n")
        totalTestAction = 0

        for indexTestCase in range(len(self.testCaseList)):
            totalTestAction = totalTestAction + len(self.testCaseList[indexTestCase])
        functionTestIndex = self.testCaseList[0][0]['testCaseFunctionIndex']
        for indexTestCase in range(len(self.testCaseList)):
            isRepaired = self.instrumentDriver(indexTestCase)

            # self.mainLogger.info('==========test case {} is tried==========='.format(indexTestCase))
            # self.mainLogger.info('isRepaired: ' + str(isRepaired))

            if isRepaired:
                # for test in self.testCaseList[indexTestCase]:
                #     print(test['handle'])
                self.geneRepairedScript(self.testCaseList[indexTestCase])

        for i in self.testCaseList:
            repairedScript.write("driver = webdriver.Chrome(\"" + self.chromeDriverPath + "\")" + "\n" +
                                 "driver.get(\"" + self.newUrl + "\")" + "\n")
            for j in i:
                if j['action'] != '' and j['action'] != '\n':
                    repairedScript.write(
                        "{}\n{}\n".format(j['handle'], j['action']))
                else:
                    repairedScript.write("{}\n\n".format(j['handle']))
            repairedScript.write("driver.quit()\n")
        repairedScript.close()

    def getDeltaTime(self, timeBefore, timeAfter):
        return (timeAfter - timeBefore).seconds + (timeAfter - timeBefore).microseconds / 1000000.0

    def detectXmlFail(self, oldWidget, xml):
        if 'x' not in oldWidget:
            return False

        x1, y1, w, h = int(oldWidget['x']), int(oldWidget['y']), int(oldWidget['w']), int(oldWidget['h'])
        x2 = x1 + w
        y2 = y1 + h

        bounds = '[' + str(x1) + ',' + str(y1) + '][' + str(x2) + ',' + str(y2) + ']'
        return not bounds in xml

    def findMatchedCandidateInCaseXmlFail(self, base_step, base_image, current_image):

        candidate, matchedType = self.getCVTextMatchCandidate(base_step, base_image, current_image)

        if candidate:
            # logger.info('not needRepair in cvTest:' + 'xmlFail, can not sure')
            isMatched = True
        else:
            # logger.info('not needRepair in cvTest:' + str(False))
            isMatched = False
        return isMatched, candidate, matchedType

    def getCVTextMatchCandidate(self, testStep, baseImg, newVerSionImg):

        candidates, matchedType, isMapped = ImageUtil.ImageUtil.isCVTextMatch(testStep['widget'], baseImg,
                                                                              newVerSionImg)
        # logger.info(testStep['operation']['widget'])
        testStep['candidateUpperBound'] = min(len(candidates), 5)
        for candidateIndex, candidate in enumerate(candidates):
            # logger.info(testStep['operation']['widget'])
            if 'hasTryCandidateNum' not in testStep:
                testStep['hasTryCandidateNum'] = 0

            if candidateIndex < testStep['hasTryCandidateNum']:
                continue

            testStep['needRepair'] = True

            # if not notNeedRepair:
            testStep['repairHandleStr'] = 'click: ' + str(candidate)
            testStep['targetNode'] = candidate  # todo node:= {x,y,w,h} def getCandidateThisTime

            return candidate, matchedType

        return [], ''

    def updateGlobalTextUpdateList(self, base_step, repair_detail, notMatchedNewNodeList):
        if str(base_step['sIndex']) not in repair_detail['globalTextUpdateList']:
            repair_detail['globalTextUpdateList'][str(base_step['sIndex'])] = []
            # isFirstFoundXml = True

        for notMatchedNewNode in notMatchedNewNodeList:
            notMatchedNewNodeAttrib = notMatchedNewNode.attrib
            notMatchedNewNodeAttrib['parent'] = ''
            repair_detail['globalTextUpdateList'][str(base_step['sIndex'])].append(notMatchedNewNodeAttrib)

    def getMatchedLeafNodeByWidgetXpath(self, oldWidgetXpath, sureMatchedLeafNodePairList, possibleMatchLeafPair,
                                        notMatchedOldLeafNodeList,
                                        notMatchedNewLeafNodeList, sureMatchedParentNodePairList):
        for node in sureMatchedLeafNodePairList.keys():
            if (node.attrs["xpath"] == oldWidgetXpath):
                isLeaf = True
                return isLeaf, node, "isSureMatch", sureMatchedLeafNodePairList[node]
        for node in sureMatchedParentNodePairList.keys():
            if (node.attrs["xpath"] == oldWidgetXpath):
                isLeaf = False
                return isLeaf, node, "isSureMatch", sureMatchedParentNodePairList[node]

        for node in possibleMatchLeafPair.keys():
            if (node.attrs["xpath"] == oldWidgetXpath):
                isLeaf = False
                matchedNodeList = possibleMatchLeafPair[node]
                return isLeaf, node, 'isPossibleMatch', matchedNodeList

        for node in notMatchedOldLeafNodeList:
            if (node.attrs["xpath"] == oldWidgetXpath):
                return True, node, 'noneMatch', notMatchedNewLeafNodeList

        return False, None, None, None

    def getMatchedParentNodeByWidgetXpath(self, oldWidgetXpath, matchedParentNodePairList, possibleParentMatchPair,
                                          notMatchedNewNodeList):
        for node in matchedParentNodePairList.keys():
            if (node.attrs["xpath"] == oldWidgetXpath):
                matchedNode = matchedParentNodePairList[node]
                return True, node, 'isSureMatch', matchedNode
        for node in possibleParentMatchPair.keys():
            if (node.attrs["xpath"] == oldWidgetXpath):
                matchedNodeList = possibleParentMatchPair[node]
                return True, node, 'isPossibleMatch', matchedNodeList

        return True, None, 'noneMatch', notMatchedNewNodeList

    # record xml to local
    def get_html_as_file(self, html, path):
        file = open(path, 'w')
        file.write(html)
        file.close()

    # 通过widget的xpath得到旧的HTML节点
    def getHtmlNodeBypath(self, widgetXpath, oldHtml):
        htmlProcess = htmlMatch.HtmlProcess()
        rootSoup = htmlProcess.getRoot(oldHtml)
        for child in rootSoup.descendants:
            if (child.name != None and child.attrs["xpath"] == widgetXpath):
                return child

    def getLevel1MatchDicInNewHtml(self, oldNode, allNode):
        matchDic = []
        for newNode in allNode:
            htmlProcess = htmlMatch.HtmlProcess()
            tmp = htmlProcess.caculateDomNodeMatchDegreeFirst(oldNode, newNode)
            if (tmp > 0.7):
                matchDic.append((newNode, tmp))
        return matchDic

    def getLevel2MatchDicInNewHtml(self, oldNode, allNode):
        matchDic = []
        for newNode in allNode:
            htmlProcess = htmlMatch.HtmlProcess()
            width = self.driver.execute_script("return document.documentElement.scrollWidth")
            height = self.driver.execute_script("return document.documentElement.scrollHeight")
            tmp = htmlProcess.caculateDomNodeMatchDegreeLocation(oldNode, newNode, self.oldTestStep['widget'],
                                                                 width, height)
            if (tmp > 0):
                matchDic.append((newNode, tmp))
        return matchDic

    def getColorMatchDicInNewHtml(self, oldNode, allNode):
        matchDic = []
        for newNode in allNode:
            htmlProcess = htmlMatch.HtmlProcess()
            width = self.driver.execute_script("return document.documentElement.scrollWidth")
            height = self.driver.execute_script("return document.documentElement.scrollHeight")
            tmp = htmlProcess.caculateColorNodeMatchDegree(oldNode, newNode, self.oldTestStep['widget'],
                                                           self.base_image, self.current_image,
                                                           width, height)
            if (tmp > 0):
                matchDic.append((newNode, tmp))
        return matchDic

    def getDicInNewHtml(self, oldNode, newHtml, theta=0.8):
        matchDic = []
        allLeafNode = []
        allNode = []
        htmlProcess = htmlMatch.HtmlProcess()
        rootSoup = htmlProcess.getRoot(newHtml)
        for child in rootSoup.html.descendants:
            if child.name is None or child.name in ['head', 'title', 'body']:
                continue
            if len(child.find_all(lambda x: x.name != '', recursive=False)) == 0:
                allLeafNode.append(child)
            allNode.append(child)
            tmp = htmlProcess.caculateNodeMatchDegree(oldNode, child, theta)
            if tmp > 0:
                matchDic.append((child, tmp))
        return matchDic, allLeafNode, allNode, rootSoup

    def getDicByAllAttrs(self, oldNode, newHtml):
        DONT_USE_ATTRS = ['xpath', 'class', 'classIndex']
        matchDic = []
        allLeafNode = []
        allNode = []
        htmlProcess = htmlMatch.HtmlProcess()
        rootSoup = htmlProcess.getRoot(newHtml)
        similarNodes2attrs = {}  # node has same attrs:attrsList
        attr2times = {}  # 属性出现的次数 如id:1
        sureMatchNodesList = []
        possibleMatchNodesList = []
        for attrName in oldNode.attrs.keys():
            if (attrName not in DONT_USE_ATTRS):
                attr2times[attrName] = 0
        attr2times['string'] = 0
        for child in rootSoup.html.descendants:
            if (child.name != None):
                if (len(child.find_all(lambda x: x.name != '', recursive=False)) == 0):
                    allLeafNode.append(child)
                allNode.append(child)
                hasSameAttrs, sameAttrsList, stringSimilarity = htmlProcess.compareOldNewNode(oldNode, child)
                if (hasSameAttrs):
                    similarNodes2attrs[child] = sameAttrsList
                    for attrName in sameAttrsList:
                        attr2times[attrName] += 1
        for similarNode in similarNodes2attrs:
            isSureMatch = False
            for attrName in similarNodes2attrs[similarNode]:
                if (attr2times[attrName] == 1):
                    isSureMatch = True
                    sureMatchNodesList.append(similarNode)
                    break
            if (isSureMatch == False):
                possibleMatchNodesList.append(similarNode)

        return sureMatchNodesList, possibleMatchNodesList, allLeafNode, allNode

    def getAllLeafNode(self, newHtml):
        htmlProcess = htmlMatch.HtmlProcess()
        rootSoup = htmlProcess.getRoot(newHtml)
        allNode = []
        for child in rootSoup.html.descendants:
            if (child.name != None):
                # if(self.speedMode is True):
                #     #only leaf node
                #     if(len(child.find_all(lambda x: x.name != '', recursive=False)) == 0):
                #         allNode.append(child)
                # else:
                allNode.append(child)
        return allNode, rootSoup

    def get_full_screenshot_as_file(self, driver, path):
        width = driver.execute_script("return document.documentElement.scrollWidth")
        height = driver.execute_script("return document.documentElement.scrollHeight")
        width = 1200
        if 'espn' in self.newUrl:
            width = 1600
        driver.set_window_size(width, height)
        driver.get_screenshot_as_file(path)
        img = Image.open(path)
        return img.width / width

    @calculate_time()
    def assignNodeLocationMain(self, rootSoup, el, widgetLocation):
        self.assignNodeLocationRec(rootSoup, el, widgetLocation)

    def assignNodeLocationRec(self, rootSoup, el, widgetLocation):
        location = el.location
        size = el.size
        if (size['width'] == 0 or size['height'] == 0):
            return
        if (abs(location['y'] - widgetLocation['y']) > 600):
            return
        rootSoup.attrs['x'] = location['x']
        rootSoup.attrs['y'] = location['y']
        rootSoup.attrs['w'] = size['width']
        rootSoup.attrs['h'] = size['height']
        self.allNodeRec.append(rootSoup)
        for child in rootSoup.children:
            if (child.name is None):
                continue
            try:
                if (child.name == 'svg'):
                    el = el.find_element_by_xpath('//' + "*[name()='svg']")
                else:
                    el = el.find_element_by_xpath('//' + child.attrs["xpath"].split('/')[-1])
            except Exception as e:
                # print(e)
                continue
            self.assignNodeLocationRec(child, el, widgetLocation)

    def getNodeLocationByRoot(self, rootSoup, widgetLocation):
        # print(rootSoup.html.attrs['xpath'])
        el = self.driver.find_element_by_xpath(rootSoup.html.attrs['xpath'])
        self.allNodeRec = []
        self.assignNodeLocationMain(rootSoup.html, el, widgetLocation)
        result = self.allNodeRec
        self.allNodeRec = []
        for leafNode in result:
            if (len(list(leafNode.descendants)) < 10):
                self.allNodeRec.append(leafNode)

    @calculate_time()
    def assignNodeLocation(self, allLeafNode):
        postProcessLeafNode = []
        if os.path.exists(self.cachedDB):
            with open(self.cachedDB, 'rb') as f:
                xpath2loc = pickle.load(f)
            for leafNode in allLeafNode:
                if leafNode.attrs["xpath"] in xpath2loc:
                    xpath = leafNode.attrs["xpath"]
                    leafNode.attrs['x'] = xpath2loc[xpath]['x']
                    leafNode.attrs['y'] = xpath2loc[xpath]['y']
                    leafNode.attrs['w'] = xpath2loc[xpath]['width']
                    leafNode.attrs['h'] = xpath2loc[xpath]['height']
                    if leafNode.attrs['w'] == 0 or leafNode.attrs['h'] == 0:
                        continue
                    postProcessLeafNode.append(leafNode)
            return postProcessLeafNode
        # if cachedDB is not exists
        xpath2loc = {}
        for leafNode in allLeafNode:
            try:
                el = self.driver.find_element_by_xpath(leafNode.attrs["xpath"])
                location = el.location
                size = el.size
            except:
                continue
            xpath2loc[leafNode.attrs["xpath"]] = {}
            leafNode.attrs['x'] = xpath2loc[leafNode.attrs["xpath"]]['x'] = location['x']
            leafNode.attrs['y'] = xpath2loc[leafNode.attrs["xpath"]]['y'] = location['y']
            leafNode.attrs['w'] = xpath2loc[leafNode.attrs["xpath"]]['width'] = size['width']
            leafNode.attrs['h'] = xpath2loc[leafNode.attrs["xpath"]]['height'] = size['height']
            if leafNode.attrs['w'] == 0 or leafNode.attrs['h'] == 0:
                continue
            postProcessLeafNode.append(leafNode)
        # maybe have bugs
        # TODO: only none match save the results
        if len(allLeafNode) > 300:
            with open(self.cachedDB, 'wb') as f:
                pickle.dump(xpath2loc, f)
        return postProcessLeafNode

    @calculate_time()
    def getCandidatesByCNN(self, widgetLocation, baseImagePath, currentImagePath, allLeafNode, theta):
        similarLeafNode = ImageUtil.ImageUtil.getSimilarLeafNodeByCNN(widgetLocation, baseImagePath, currentImagePath,
                                                                      allLeafNode, theta)
        # similarLeafNode = ImageUtil.ImageUtil.getSimilarLeafNodeByCNNAccumulate(widgetLocation, baseImagePath, currentImagePath,
        #                                                               allLeafNode, theta)

        rankedAllLeafNode = sorted(similarLeafNode, key=lambda t: t[1], reverse=True)
        return rankedAllLeafNode

    def getMatchTypeByDic(self, matchDic):
        matchType = ""
        if len(matchDic) == 0:
            matchType = "noneMatch"
        elif len(matchDic) == 1 or (matchDic[0][1] - matchDic[1][1] > 0.5):
            # elif len(matchDic) == 1:
            return "sureMatch"
        elif matchDic[0][1] >= 1:
            # todo: not just 1, maybe 2,3,4
            for i in range(len(matchDic)):
                if matchDic[i][1] < 1:
                    del matchDic[i:]
                    break
            matchDic = sorted(matchDic, key=lambda t: len(t[0]['xpath']), reverse=True)
            for item in matchDic:
                if item[0]['xpath'] not in matchDic[0][0]['xpath']:
                    return "possibleMatch"
            return "sureMatch"

        else:
            matchType = "possibleMatch"
        return matchType

    def getWidgetType(self, widgetLocation, ImagePath):
        with open(ImagePath, 'rb') as f:
            data = f.read()
            baseImage = base64.b64encode(data)  # 得到 byte 编码的数据
        all_text_block = ImageUtil.ImageUtil.getTextBlockByTecentAPI(baseImage)
        for text_block in all_text_block:
            if (ImageUtil.ImageUtil.isPointInBox(text_block["x"] + text_block["w"] / 2,
                                                 text_block["y"] + text_block["h"] / 2, widgetLocation)):
                return "text", text_block["text"]
        return "image", None

    def getCandidateByTextBlock(self, allLeafNode, text_block):
        candidateList = []
        for leafNode in allLeafNode:
            widgetLocation = {
                'x': leafNode.attrs['x'],
                'y': leafNode.attrs['y'],
                'w': leafNode.attrs['w'],
                'h': leafNode.attrs['h']
            }
            if (ImageUtil.ImageUtil.isPointInBox(text_block["x"] + text_block["w"] / 2,
                                                 text_block["y"] + text_block["h"] / 2, widgetLocation)):
                candidateList.append(leafNode)
        return candidateList

    def filterNodeByLocation(self, allNode, widgetLocation):
        result = []
        allNode = self.assignNodeLocation(allNode)
        for leafNode in allNode:
            if self.speedMode is False:
                result.append(leafNode)
            else:
                # and abs(leafNode.attrs['y'] - widgetLocation['y']) < 500
                if (0.6 < abs(leafNode.attrs['h'] / widgetLocation['h']) < 1.8 or 0.6 < abs(
                        leafNode.attrs['w'] / widgetLocation['w']) < 1.8
                        and len(list(leafNode.descendants)) < 15):
                    result.append(leafNode)
        return result

    def perform_save_repair(self, candidate, oldTestStep):
        print("xpath of candidate is:")
        print(candidate.attrs['xpath'])
        try:
            oldTestStep['targetNode'] = candidate
            el_repair = self.getSeleniumElement(candidate)
            self.performTestAction(oldTestStep, el_repair)
        except Exception as e:
            print(e)

    def processImageElementSelenium(self, root, oldTestStep, base_image, current_image):

        # rankedAllLeafNode = ImageUtil.ImageUtil.getSimilarLeafNodeByCNNAccumulate(oldTestStep['widget'], base_image,
        #                                                                         current_image, root)
        rankedAllLeafNode = ImageUtil.ImageUtil.getSimilarLeafNodeByCNNSelenium(oldTestStep['widget'], base_image,
                                                                                current_image, root)
        print("All possible match node:")
        print(rankedAllLeafNode[:(lambda x: 7 if x > 7 else x)(len(rankedAllLeafNode))])
        if (len(rankedAllLeafNode) > 0):
            candidate = rankedAllLeafNode[0][0]
            self.perform_save_repair(candidate, oldTestStep)

    def processImageElement(self, allNode, oldTestStep, base_image, current_image, theta):
        rankedAllLeafNode = self.getCandidatesByCNN(oldTestStep['widget'], base_image, current_image, allNode, theta)
        if len(rankedAllLeafNode) > 0:
            candidate = rankedAllLeafNode[0][0]
            self.perform_save_repair(candidate, oldTestStep)
        return rankedAllLeafNode

    def processImageElementPossible(self, allNode, oldTestStep, base_image, current_image, matchDic, theta,
                                    para_text_image=3):
        # combine text and image similarity
        final_list = []
        rankedAllLeafNode = self.getCandidatesByCNN(oldTestStep['widget'], base_image, current_image, allNode, theta)
        for i in range(len(rankedAllLeafNode)):
            node, image_similarity = rankedAllLeafNode[i]
            for node_tmp, text_similarity in matchDic:
                if node == node_tmp:
                    final_list.append((node, text_similarity * para_text_image + image_similarity.item()))
        final_list = sorted(final_list, key=lambda t: t[1], reverse=True)
        if len(final_list) > 0:
            candidate = final_list[0][0]
            self.perform_save_repair(candidate, oldTestStep)
        return rankedAllLeafNode



    def getWebEvoMatchedXpath(self, oldJson, newJson, baseImage, currentImage):
        # Run the Java program
        # java_output = subprocess.check_output(
        #         ['java', '-cp', 'WebEvo.jar', 'frame.algorithm.webevo.WebEvoWrapper', oldJson, newJson, baseImage, currentImage])
        try:
            java_output = subprocess.check_output(
                ['java', '-cp', 'WebEvo.jar', 'frame.algorithm.webevo.WebEvoWrapper', oldJson, newJson, baseImage, currentImage])
        except subprocess.CalledProcessError:
            return None
        java_output_str = java_output.decode('utf-8').strip()
        if java_output_str == 'null':
            return None
        else:
            return java_output_str



    def getSFTMMatcher(self, oldHtmlPath, newHtmlPath):
        # Run the Java program
        try:
            java_output = subprocess.check_output(
                ['java', '-cp', 'SFTM.jar', 'TreeMatcherWrapper', oldHtmlPath, newHtmlPath])
        except subprocess.CalledProcessError:
            return {}

        # Decode the byte string into a regular string
        java_output_str = java_output.decode('utf-8')

        # Initialize an empty dictionary
        java_map_dict = {}

        # Split the lines and populate the dictionary
        for line in java_output_str.split('\n'):
            if line.strip():  # Ignore empty lines
                key, value = line.split(':')
                java_map_dict[key.strip()] = value.strip()
        return java_map_dict

    # 修复每个具体的test case
    def instrumentDriver(self, testCaseIndex):
        start = time.time()
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("--force-device-scale-factor=1")
        self.driver = webdriver.Chrome(executable_path=self.chromeDriverPath, chrome_options=chrome_options)
        self.driver.get(self.newUrl)
        end = time.time()
        print("chrome initial time: " + str(end - start))
        isRepairedThisTest = True
        oldActionPointer = 0
        testCaseLength = len(self.testCaseList[testCaseIndex])
        while oldActionPointer < testCaseLength:
            oldTestStep = self.testCaseList[testCaseIndex][oldActionPointer]
            self.oldTestStep = oldTestStep
            base_image = oldTestStep['screenshotPathInit']
            current_image = oldTestStep['screenshotPath']
            self.base_image = base_image
            self.current_image = current_image
            print("xpath of test step {}: {}".format(oldActionPointer, oldTestStep['xpath']))
            # sleep api
            if 'sleep(' in oldTestStep['handle']:
                print(int(oldTestStep['handle'].strip().split('(')[1][0:-1]))
                time.sleep(int(oldTestStep['handle'].strip().split('(')[1][0:-1]))
                oldActionPointer += 1
                continue

            # record layout & screenshot
            self.scaleRatio = self.get_full_screenshot_as_file(self.driver, oldTestStep['screenshotPath'])
            # self.driver.get_screenshot_as_file(oldTestStep['screenshotPath'])
            currentHtml = str(self.driver.page_source)
            self.get_html_as_file(currentHtml, oldTestStep['htmlPath'])

            oldHtmlNode = self.getHtmlNodeBypath(oldTestStep["xpath"], oldTestStep['html'])
            print("oldHtmlNode:" + str(oldHtmlNode))
            try:
                el = RecordScreenAndWidght.RecordScreenAndWidget.getElementByRecordStep(self.driver, oldTestStep)
                # self.performTestAction(oldTestStep, el)
                oldActionPointer += 1
                continue
            except:
                print("encounter a broken test step")
            if self.repairMode == 'webEvo':
                oldNodes = [{'text': oldHtmlNode.text,
                             'xpath': oldHtmlNode.attrs['xpath'],
                             'x': oldTestStep['widget']['x'],
                             'y': oldTestStep['widget']['y'],
                             'w': oldTestStep['widget']['w'],
                             'h': oldTestStep['widget']['h']}]
                # Write the dictionary to a JSON file
                with open(os.path.join(self.outputDir, 'oldNodes.json'), 'w') as json_file:
                    json.dump(oldNodes, json_file, indent=4)

                allNode, rootSoup = self.getAllLeafNode(currentHtml)
                allNode = self.assignNodeLocation(allNode)
                newNodes = []
                for node in allNode:
                    newNodes.append(
                        {'text': node.text,
                         'xpath': node.attrs['xpath'],
                         'x': node.attrs['x'],
                         'y': node.attrs['y'],
                         'w': node.attrs['w'],
                         'h': node.attrs['h']})
                # Write the dictionary to a JSON file
                with open(os.path.join(self.outputDir, 'newNodes.json'), 'w') as json_file:
                    json.dump(newNodes, json_file, indent=4)
                matchedXpath = self.getWebEvoMatchedXpath(os.path.join(self.outputDir, 'oldNodes.json'),
                      os.path.join(self.outputDir, 'newNodes.json'),
                      self.base_image, self.current_image)
                if matchedXpath is not None:
                    for node in allNode:
                        if node.attrs['xpath'] == matchedXpath:
                            candidate = node
                            print("xpath of candidate is:")
                            print(candidate.attrs['xpath'])
                            try:
                                el_repair = self.getSeleniumElement(candidate)
                                self.performTestAction(oldTestStep, el_repair)
                            except Exception as e:
                                print(e)
                oldActionPointer += 1
                continue
            if self.repairMode == 'SFTM':
                xpathMatcher = self.getSFTMMatcher(oldTestStep['htmlPathInit'], oldTestStep['htmlPath'])
                normalizedXpathMatcher = {}
                from xpathProcess import normarlizaXpath
                for sourceXpath in xpathMatcher:
                    normalizedXpathMatcher[normarlizaXpath(sourceXpath)] = normarlizaXpath(xpathMatcher[sourceXpath])
                allNode, rootSoup = self.getAllLeafNode(currentHtml)
                if oldTestStep["xpath"] in normalizedXpathMatcher:
                    matchedXpath = normalizedXpathMatcher[oldTestStep['xpath']]
                    for node in allNode:
                        if node.attrs['xpath'] == matchedXpath:
                            candidate = node
                            print("xpath of candidate is:")
                            print(candidate.attrs['xpath'])
                            try:
                                el_repair = self.getSeleniumElement(candidate)
                                self.performTestAction(oldTestStep, el_repair)
                            except Exception as e:
                                print(e)

                oldActionPointer += 1
                continue

            if self.repairMode == 'CNN':
                # allNode, rootSoup = self.getAllLeafNode(currentHtml)
                # self.getNodeLocationByRoot(rootSoup,True,oldTestStep['widget'])
                # print(len(self.allNodeRec))
                allNode, _ = self.getAllLeafNode(currentHtml)
                allNode = self.filterNodeByLocation(allNode, oldTestStep['widget'])

                self.processImageElement(allNode, oldTestStep, base_image, current_image, 0)
                oldActionPointer += 1
                continue
            if self.repairMode == 'COLOR':
                allNode, rootSoup = self.getAllLeafNode(currentHtml)
                allNode = self.assignNodeLocation(allNode)
                # print(len(allNode))
                matchDic = self.getColorMatchDicInNewHtml(oldHtmlNode, allNode)
                matchDic = sorted(matchDic, key=lambda t: t[1], reverse=True)
                # print("All possible match node:")
                # print(matchDic[0:3])
                candidate = matchDic[0][0]
                print("xpath of candidate is:")
                print(candidate.attrs['xpath'])
                try:
                    el_repair = self.getSeleniumElement(candidate)
                    self.performTestAction(oldTestStep, el_repair)
                except Exception as e:
                    print(e)
                oldActionPointer += 1
                continue
            if self.repairMode == 'Hyb':
                matchDic, allLeafNode, allNode, rootSoup = self.getDicInNewHtml(oldHtmlNode, currentHtml,
                                                                                theta=self.theta_dom)
                # matchDic,allLeafNode,allNode=self.getDicInNewHtml(oldHtmlNode,currentHtml,theta=0.8)
                matchDic = sorted(matchDic, key=lambda t: t[1], reverse=True)
                matchType = self.getMatchTypeByDic(matchDic)
                print("matchType:" + matchType)
                if (matchType == "sureMatch"):
                    candidate = matchDic[0][0]
                    print("candidate:")
                    print(candidate)
                    self.perform_save_repair(candidate, oldTestStep)
                    oldActionPointer += 1
                    continue
                elif (matchType == "possibleMatch"):
                    # special cases: two candidates and one is child node of another
                    # using tag name to decide
                    # if(oldHtmlNode.name ==):
                    #     candidate =
                    #     self.perform_save_repair
                    #     oldActionPointer += 1
                    #     continue
                    # print(matchDic)
                    allCandidateNode = []
                    for candidateTurple in matchDic:
                        allCandidateNode.append(candidateTurple[0])
                    self.speedMode = False
                    allCandidateNode = self.filterNodeByLocation(allCandidateNode, oldTestStep['widget'])
                    self.speedMode = True
                    if len(allCandidateNode) == 0:
                        candidate = matchDic[0][0]
                        print("candidate:")
                        print(candidate)
                        self.perform_save_repair(candidate, oldTestStep)
                        oldActionPointer += 1
                        continue
                    # rankedAllLeafNode = self.processImageElement(allCandidateNode, oldTestStep, base_image,
                    #                                              current_image,
                    #                                              theta=0)
                    rankedAllLeafNode = self.processImageElementPossible(allCandidateNode, oldTestStep, base_image,
                                                                         current_image, matchDic,
                                                                         theta=0, para_text_image=self.theta_combine)
                    oldActionPointer += 1
                    continue
                elif (matchType == "noneMatch"):
                    # if (len(allNode) > 3500):
                    #     self.getNodeLocationByRoot(rootSoup, oldTestStep['widget'])
                    #     allNode = self.allNodeRec
                    # else:
                    allNode = self.filterNodeByLocation(allNode, oldTestStep['widget'])
                    # allNode=self.filterNodeByLocation(allNode,oldTestStep['widget'])
                    rankedAllLeafNode = self.getCandidatesByCNN(oldTestStep['widget'], base_image, current_image,
                                                                allNode, theta=self.theta_image)
                    if len(rankedAllLeafNode) > 0:
                        candidate = rankedAllLeafNode[0][0]
                        self.perform_save_repair(candidate, oldTestStep)
                    else:
                        print("fall back")
                        allNode = self.filterNodeByLocation(allNode, oldTestStep['widget'])
                        matchDic = self.getLevel2MatchDicInNewHtml(oldHtmlNode, allNode)
                        matchDic = sorted(matchDic, key=lambda t: t[1], reverse=True)
                        candidate = matchDic[0][0]
                        self.perform_save_repair(candidate, oldTestStep)
                    oldActionPointer += 1
                    continue
        self.driver.quit()
        return isRepairedThisTest

    def exploration(self, oldHtmlNode, allLeafNode):
        # 获得所有的leaf node
        # 一一点击、与旧节点匹配 如果有sure match，return
        # 如果所处url改变、driver.back
        executeList = []
        currentUrl = self.driver.current_url
        x = 0
        y = 0
        for leafNode in allLeafNode:
            if (leafNode.string == "Health Conditions"):
                print(leafNode)
                try:
                    executeList.clear()
                    executeList.append(leafNode)
                    # if(leafNode.name=="a"):
                    #     continue
                    el_repair = self.getSeleniumElement(leafNode)
                    location = el_repair.location
                    ActionChains(self.driver).move_by_offset(-x, -y).perform()
                    x = location["x"] + 1
                    y = location["y"] + 1
                    ActionChains(self.driver).move_by_offset(x, y).click().perform()
                    time.sleep(1)
                    # el_repair.click()
                    currentHtml = str(self.driver.page_source)
                    matchDic, allLeafNode, allNode, _ = self.getDicInNewHtml(oldHtmlNode, currentHtml)
                    matchDic = sorted(matchDic, key=lambda t: t[1], reverse=True)
                    matchType = self.getMatchTypeByDic(matchDic)
                    if (matchType == "sureMatch"):
                        executeList.append(matchDic[0][0])
                    if (currentUrl == self.driver.current_url):
                        self.driver.refresh()
                    else:
                        self.driver.back()
                    if (len(executeList) == 2):
                        break
                except Exception as e:
                    continue
        return executeList

    def writeToFile(self, file, str):
        import io
        outputFile = io.open(file, mode='w', encoding='utf-8')
        outputFile.write(str.decode('utf-8'))
        outputFile.close()

    # 触发具体的测试动作
    @calculate_time()
    def performTestAction(self, testStep, el):
        if ".click()" in testStep['action'] and testStep['action'] != "#":
            el.click()

        elif ".clear()" in testStep['action'] and testStep['action'] != "#":
            el.clear()


        elif ".send_keys" in testStep['action'] and testStep['action'][0] != "#":
            el.send_keys(testStep['action'].strip().split('(')[1][1:-2])
            # print 'send_keys:'
            # print testStep['action'].strip().split('(')[1][1:-2]

        elif "driver.back()" in testStep['handle'] and testStep['handle'][0] != "#":
            self.driver.back()

    # 获得本次测试工作的匹配控件
    def getSeleniumElement(self, targetNode):
        if ("id" in targetNode.attrs):
            el_repair = self.driver.find_element_by_id(targetNode.attrs["id"])
            return el_repair
        if (targetNode.string != None and targetNode.name == 'a'):
            el_repair = self.driver.find_element_by_link_text(targetNode.string)
            return el_repair
        if ("xpath" in targetNode.attrs):
            el_repair = self.driver.find_element_by_xpath(targetNode.attrs['xpath'])
            return el_repair
        if ("class" in targetNode.attrs):
            el_repair = self.driver.find_elements_by_class_name(targetNode.attrs["class"][0])[
                targetNode.attrs["classIndex"][targetNode.attrs["class"][0]]]
            return el_repair

        self.mainLogger.info("error in get Handle")
        exit(-1)

    def geneRepairedScript(self, testCase):
        for index, testStep in enumerate(testCase):
            if 'targetNode' not in testStep:
                continue
            if not testStep['needRepair']:
                continue
            targetNode = testStep['targetNode']
            if 'additionAction' in testStep:
                testStep['handle'] = str(testStep['additionAction'])
            if ("id" in targetNode.attrs):
                testStep['handle'] = 'el = driver.find_element_by_id("' + targetNode[
                    'id'] + '")'
            elif ('xpath' in targetNode.attrs):
                testStep['handle'] = 'el = driver.find_element_by_xpath("' + targetNode[
                    'xpath'] + '")'
            elif ("class" in targetNode.attrs):
                testStep['handle'] = ('el = driver.find_elements_by_class("' + targetNode.attrs["class"][0]
                                      + '")"[' + str(
                            targetNode.attrs["classIndex"][targetNode.attrs["class"][0]]) + ']')
            elif (targetNode.string != None):
                testStep['handle'] = 'el = driver.find_element_by_link_text("' + targetNode.string + '")'

            else:
                self.mainLogger.info("error in get Handle")
                pass
