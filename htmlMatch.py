# encoding=utf-8
from __future__ import division
import os
import logging
import xpathProcess

import Levenshtein

import ImageUtil

logger = logging.getLogger("meter")
from bs4 import BeautifulSoup

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


class HtmlProcess:
    def __init__(self):
        self.classDic = {}
        self.idDic = {}
        self.descriptDic = {}
        self.textDic = {}

        self.childNodeRes = []
        self.parentNodeRes = []
        self.NonBodyTag = ["script", "style", "meta", "link"]

    def definePopWindowType(self, xml, screen_w, screen_h):
        root = self.getRoot(xml)
        while 'bounds' not in root.attrib:
            for child in root:
                root = child
                break

        pageBounds = root.get('bounds')
        x1 = pageBounds.split('[')[1].split(',')[0]
        y1 = pageBounds.split(']')[0].split(',')[1]
        x2 = pageBounds.split('][')[1].split(',')[0]
        y2 = pageBounds.split('][')[1].split(',')[1].split(']')[0]

        if int(x2) - int(x1) == screen_w and int(y2) - int(y1) == screen_h:
            return 'isCommon'
        else:
            return 'isPop'

    def definePopWindowTypeByInferedWindow(self, xml, xml_refer):
        root = self.getRoot(xml)
        while 'bounds' not in root.attrib:
            for child in root:
                root = child
                break

        pageBounds = root.get('bounds')
        x1 = pageBounds.split('[')[1].split(',')[0]
        y1 = pageBounds.split(']')[0].split(',')[1]
        x2 = pageBounds.split('][')[1].split(',')[0]
        y2 = pageBounds.split('][')[1].split(',')[1].split(']')[0]

        root_ref = self.getRoot(xml_refer)
        while 'bounds' not in root_ref.attrib:
            for child in root_ref:
                root_ref = child
                break

        pageBounds = root_ref.get('bounds')
        x1_ref = pageBounds.split('[')[1].split(',')[0]
        y1_ref = pageBounds.split(']')[0].split(',')[1]
        x2_ref = pageBounds.split('][')[1].split(',')[0]
        y2_ref = pageBounds.split('][')[1].split(',')[1].split(']')[0]

        if int(x2) - int(x1) == int(x2_ref) - int(x1_ref) and int(y2) - int(y1) == int(y2_ref) - int(y1_ref):
            return 'isCommon'
        else:
            return 'isPop'

    def getWidthHeightByInferedWindow(self, xml_refer):

        root_ref = self.getRoot(xml_refer)
        while 'bounds' not in root_ref.attrib:
            for child in root_ref:
                root_ref = child
                break

        pageBounds = root_ref.get('bounds')
        x1_ref = pageBounds.split('[')[1].split(',')[0]
        y1_ref = pageBounds.split(']')[0].split(',')[1]
        x2_ref = pageBounds.split('][')[1].split(',')[0]
        y2_ref = pageBounds.split('][')[1].split(',')[1].split(']')[0]

        return int(x2_ref) - int(x1_ref), int(y2_ref) - int(y1_ref)

    def currentNewNodeIsInBridge(self, xml2, sBridge):
        for xml1, sIndex in list(sBridge.items()):
            if self.isXmlMatch(xml1, xml2, isSureLevelMatch=True, isSureMatch=True, givenThreshold=0.6,
                               isBuildSBridge=False)[0]:
                logger.info(
                    'isInBridge:' + str(sIndex) + ', score is: ' + str(self.isXmlMatch(xml1, xml2, False, False))[8])
                return True, sIndex

        for xml1, sIndex in list(sBridge.items()):
            if self.isXmlMatch(xml1, xml2, isSureLevelMatch=False, isSureMatch=True, givenThreshold=0.6,
                               isBuildSBridge=False)[0]:
                logger.info(
                    'isInBridge:' + str(sIndex) + ', score is: ' + str(self.isXmlMatch(xml1, xml2, False, False))[8])
                return True, sIndex

        return False, None

    def getOkButton(self, xml):
        res = self.getUIElementsList(xml)

        # define ok list
        okList = ['知道了', '我知道了' '确定', '查看', 'ok', 'Ok', 'OK', '确认']

        for node in res:
            if node.get('text') in okList:
                return node
        return None

    def getRoot(self, htmlFile):
        # xmlFile = xmlFile.replace("&", "")
        # xmlFile = xmlFile.replace("#", "")
        soup = BeautifulSoup(htmlFile)  # <class 'xml.etree.ElementTree.ElementTree'>
        # 获取根节点 <Element 'data' at 0x02BF6A80>
        # 去除script、style等标签
        for NotBodyTag in self.NonBodyTag:
            for NonBodyElement in soup.findAll(NotBodyTag):
                NonBodyElement.extract()
        # 将每个节点的xpath添加到属性中
        xpathProcess.addXpathToSoupAttribute(soup)
        # 将每个节点class的index添加到属性中
        self.denoteCurrentHtmlIndex(soup)
        self.initIDDic()
        # add string to attrb
        return soup

    def getUIElementsList(self, xmlFile):
        self.res = []
        tree = ET.parse(xmlFile)  # <class 'xml.etree.ElementTree.ElementTree'>
        root = tree.getroot()  # 获取根节点 <Element 'data' at 0x02BF6A80>

        self.printAllnodes(root)
        return self.res

    def printAllnodes(self, node):
        if 'class' in list(node.keys()):
            self.res.append(node.attrib)
        for child in node:
            self.printAllnodes(child)

    def printAlChildnodes(self, node):
        hasChild = False
        for child in node:
            hasChild = True
            self.printAlChildnodes(child)

        if not hasChild:
            self.res.append(node.attrib)

    def findCertainNode(self, root, certainNode):
        if self.certainNode != '':
            return
        if root.attrib == certainNode:
            self.certainNode = root
        for child in root:
            self.findCertainNode(child, certainNode)

    def initIDDic(self):
        self.classDic = {}
        self.idDic = {}
        self.descriptDic = {}
        self.textDic = {}

    # 对xml进行重写，把默认xml的index重写为脚本中的索引index ，保存在本地的字典里
    def denoteCurrentHtmlIndex(self, root):
        if "class" in root.attrs:
            if ("classIndex" not in root.attrs.keys()):
                root.attrs['classIndex'] = {}
            for className in root.attrs['class']:
                if className not in list(self.classDic.keys()):
                    self.classDic[className] = 1
                else:
                    self.classDic[className] = self.classDic[className] + 1
                root.attrs['classIndex'][className] = self.classDic[className] - 1

            # if 'id' in root.attrib :
            #     if root.attrib['id'] not in list(self.idDic.keys()):
            #         self.idDic[root.attrib['id']] = 1
            #     else:
            #         self.idDic[root.attrib['id']] = self.idDic[root.attrib['id']] + 1
            #     root.set('idIndex', self.idDic[root.attrib['id']] - 1)
        # print root.attrib
        for child in root.children:
            if (child.name != None):
                self.denoteCurrentHtmlIndex(child)

    def getChildNodeList(self, root):
        hasChild = False
        for child in root.children:
            if (child.name != None):
                hasChild = True
                self.getChildNodeList(child)

        if not hasChild:
            self.childNodeRes.append(root)
            # avoid the case that listview contains no child widget, but denoted as a child widget.
            # listTypeList = ['android.widget.ListView', 'android.support.v7.widget.RecyclerView', 'android.view.View',

    #             #                 'android.widget.GridView']
    #             # if root.get('class') not in listTypeList:
    #             #     if (root.get('w') >= 30 and root.get('h') >= 30) or root.get('text') != '':
    #             #         self.childNodeRes.append(root)
    #             # elif root.get('class') == 'android.view.View' and (
    #             #         root.get('text') != '' or root.get('content-desc') != '' or root.get('resource-id') != ''):
    #             #     self.childNodeRes.append(root)

    def getParentNodeList(self, root):
        hasChild = False
        for child in root.children:
            if (child.name != None):
                hasChild = True
                self.getParentNodeList(child)
        if hasChild:
            self.parentNodeRes.append(root)

    def matchNodePair__(self, oldChildNodeList, newChildNodeList, oldChild2ParentDic, newChild2ParentDic):
        # todo descript,text,id, with their index;  scrollable,etc
        res = {}
        # denote whether the match relation is sure
        temp_oldCompareMatch = []
        temp_newCompareMatch = []
        temp_oldPartialMatch = []
        temp_newPartialMatch = []

        # one - multipal match
        possibleMatchPair = {}
        # sublingMatchedNodePairs = {}
        subingMatchedParentNodePairs = {}

        for oldNode in oldChildNodeList:
            sureMatchedNum = 0
            for newNode in newChildNodeList:
                if self.isNodeMatched(oldNode, newNode, True, True):
                    sureMatchedNum = sureMatchedNum + 1
                    sureMatchCandidateNode = newNode
            if sureMatchedNum == 1:
                res[oldNode] = sureMatchCandidateNode
                temp_oldCompareMatch.append(oldNode)
                temp_newCompareMatch.append(sureMatchCandidateNode)

                # 结构信息使用与否； layout
                if True:
                    sublingMatchedNodePairs, shouldMatchedNewNodeList = self.denoteSublingNodeAsSureMatch(oldNode,
                                                                                                          sureMatchCandidateNode,
                                                                                                          oldChild2ParentDic,
                                                                                                          newChild2ParentDic,
                                                                                                          newChildNodeList,
                                                                                                          subingMatchedParentNodePairs)

                    for sublingOldNode, sublingNewNode in sublingMatchedNodePairs.items():
                        if sublingOldNode not in res:
                            res[sublingOldNode] = sublingNewNode
                            temp_oldCompareMatch.append(sublingOldNode)
                            temp_newCompareMatch.append(sublingNewNode)

                    for shouldMatchedNewNode in shouldMatchedNewNodeList:
                        if shouldMatchedNewNode not in temp_newCompareMatch:
                            temp_newCompareMatch.append(shouldMatchedNewNode)
            elif sureMatchedNum > 1:
                pass
                # Logger.xmlProcessLogger.info('isSureMatch num >1, here Path should be refactored.')

        oldChildNodeListAfterCompareMatch = []
        newChildNodeListAfterCompareMatch = []
        for i in range(len(oldChildNodeList)):
            if oldChildNodeList[i] not in temp_oldCompareMatch:
                oldChildNodeListAfterCompareMatch.append(oldChildNodeList[i])
        for j in range(len(newChildNodeList)):
            if newChildNodeList[j] not in temp_newCompareMatch:
                newChildNodeListAfterCompareMatch.append(newChildNodeList[j])

        # todo partial compare
        for oldNodeAfterCompareMatch in oldChildNodeListAfterCompareMatch:
            matchedNum = 0
            matchedNumAllNewNode = 0
            targetNewNodeAfterCompareMatch = []
            for newNodeAfterCompareMatch in newChildNodeListAfterCompareMatch:
                if self.isNodeMatched(oldNodeAfterCompareMatch, newNodeAfterCompareMatch, False, True):
                    matchedNum = matchedNum + 1
                    targetNewNodeAfterCompareMatch.append(newNodeAfterCompareMatch)

            for newNode in newChildNodeList:
                if self.isNodeMatched(oldNodeAfterCompareMatch, newNode, False, True) and newNode not in res.values():
                    matchedNumAllNewNode = matchedNumAllNewNode + 1
                    targetNewNode = newNode
            # unique condition 1
            if matchedNum == 1:
                # res.append(list([oldNodeAfterCompareMatch,targetNewNodeAfterCompareMatch]))
                res[oldNodeAfterCompareMatch] = targetNewNodeAfterCompareMatch[0]

                temp_oldPartialMatch.append(oldNodeAfterCompareMatch)
                temp_newPartialMatch.append(targetNewNodeAfterCompareMatch[0])

                # avoid repeated matching
                newChildNodeListAfterCompareMatch.remove(targetNewNodeAfterCompareMatch[0])

            elif matchedNumAllNewNode == 1:
                res[oldNodeAfterCompareMatch] = targetNewNode

                temp_oldPartialMatch.append(oldNodeAfterCompareMatch)
                temp_newPartialMatch.append(targetNewNode)
            elif matchedNum > 1:
                '''
                # unique condition 2
                isUniqueCondition2 = False
                for candidateMatchedNewNode in targetNewNodeAfterCompareMatch:
                    idSame = oldNodeAfterCompareMatch.get('resource-id')==candidateMatchedNewNode.get('resource-id') and oldNodeAfterCompareMatch.get('resource-id')!=''
                    # todo 7.22 how to measure the use of parent mapping
                    isMatchedParent,_ = self.denotePartialSameParentAsSameByMarchedChildNode(oldNodeAfterCompareMatch,candidateMatchedNewNode)
                    if idSame:
                        isUniqueCondition2 = True

                        res[oldNodeAfterCompareMatch] = candidateMatchedNewNode

                        temp_oldPartialMatch.append(oldNodeAfterCompareMatch)
                        temp_newPartialMatch.append(candidateMatchedNewNode)

                        # avoid repeated matching
                        newChildNodeListAfterCompareMatch.remove(candidateMatchedNewNode)
                        break
                '''
                # todo 7.22 parent nodes map to  map more child nodes.
                # if not isUniqueCondition2:
                possibleMatchPair[oldNodeAfterCompareMatch] = list(targetNewNodeAfterCompareMatch)
                temp_oldPartialMatch.append(oldNodeAfterCompareMatch)
                for item in targetNewNodeAfterCompareMatch:
                    temp_newPartialMatch.append(item)

        notMatchedOldNodeList = []
        notMatchedNewNodeList = []
        for node in oldChildNodeList:
            if node not in temp_oldPartialMatch and node not in temp_oldCompareMatch:
                notMatchedOldNodeList.append(node)

        for node in newChildNodeList:
            if node not in temp_newPartialMatch and node not in temp_newCompareMatch:
                # filter widgets more likely to be a candidate
                if node.get('h') * 1.0 / node.get('w') > 0.1 and (
                        'image' in node.get('class').lower() or node.get('text') != '' or node.get(
                    'resource-id') != '' or node.get('content-desc') != ''):
                    notMatchedNewNodeList.append(node)

        return res, possibleMatchPair, notMatchedOldNodeList, notMatchedNewNodeList, subingMatchedParentNodePairs

    # 对每个oldXml中节点进行匹配，返回一对一，一对多，没有匹配到的，以及可能匹配的节点
    def matchNodePair(self, oldChildNodeList, newChildNodeList, oldChild2ParentDic, newChild2ParentDic):
        # todo descript,text,id, with their index;  scrollable,etc
        res = {}
        # denote whether the match relation is sure
        temp_oldCompareMatch = []
        temp_newCompareMatch = []
        temp_oldPartialMatch = []
        temp_newPartialMatch = []

        # one - multipal match
        possibleMatchPair = {}
        # sublingMatchedNodePairs = {}
        subingMatchedParentNodePairs = {}

        # 对每一个oldNode找到其匹配的新节点
        for oldNode in oldChildNodeList:
            sureMatchedNum = 0  # 相似的节点数目
            for newNode in newChildNodeList:
                if self.isNodeMatched(oldNode, newNode, True, True):  # 根据xml中的几个参数进行匹配
                    sureMatchedNum = sureMatchedNum + 1
                    sureMatchCandidateNode = newNode
            # 当且仅当有一个相似的节点
            if sureMatchedNum == 1:
                res[oldNode] = sureMatchCandidateNode
                temp_oldCompareMatch.append(oldNode)
                temp_newCompareMatch.append(sureMatchCandidateNode)
                # 返回新旧节点的最恰当的子节点的匹配对 res 以及 和新节点有覆盖关系的节点集合 shouldMatchedNewNodeList
                sublingMatchedNodePairs, shouldMatchedNewNodeList = self.denoteSublingNodeAsSureMatch(oldNode,
                                                                                                      sureMatchCandidateNode,
                                                                                                      oldChild2ParentDic,
                                                                                                      newChild2ParentDic,
                                                                                                      newChildNodeList,
                                                                                                      subingMatchedParentNodePairs)

                for sublingOldNode, sublingNewNode in list(sublingMatchedNodePairs.items()):
                    if sublingOldNode not in res:
                        res[sublingOldNode] = sublingNewNode
                        temp_oldCompareMatch.append(sublingOldNode)
                        temp_newCompareMatch.append(sublingNewNode)

                for shouldMatchedNewNode in shouldMatchedNewNodeList:
                    if shouldMatchedNewNode not in temp_newCompareMatch:
                        temp_newCompareMatch.append(shouldMatchedNewNode)
            elif sureMatchedNum > 1:
                pass
                # Logger.xmlProcessLogger.info('isSureMatch num >1, here Path should be refactored.')

        oldChildNodeListAfterCompareMatch = []
        newChildNodeListAfterCompareMatch = []
        for i in range(len(oldChildNodeList)):
            if oldChildNodeList[i] not in temp_oldCompareMatch:
                oldChildNodeListAfterCompareMatch.append(oldChildNodeList[i])
        for j in range(len(newChildNodeList)):
            if newChildNodeList[j] not in temp_newCompareMatch:
                newChildNodeListAfterCompareMatch.append(newChildNodeList[j])

        # 局部比较，对老xml中没有匹配到的节点找到对应的匹配项
        for oldNodeAfterCompareMatch in oldChildNodeListAfterCompareMatch:
            matchedNum = 0
            matchedNumAllNewNode = 0
            targetNewNodeAfterCompareMatch = []
            for newNodeAfterCompareMatch in newChildNodeListAfterCompareMatch:
                if self.isNodeMatched(oldNodeAfterCompareMatch, newNodeAfterCompareMatch, False, True):
                    matchedNum = matchedNum + 1
                    targetNewNodeAfterCompareMatch.append(newNodeAfterCompareMatch)

            for newNode in newChildNodeList:
                if self.isNodeMatched(oldNodeAfterCompareMatch, newNode, False, True) and newNode not in list(
                        res.values()):
                    matchedNumAllNewNode = matchedNumAllNewNode + 1
                    targetNewNode = newNode
            # unique condition 1
            if matchedNum == 1:
                # res.append(list([oldNodeAfterCompareMatch,targetNewNodeAfterCompareMatch]))
                res[oldNodeAfterCompareMatch] = targetNewNodeAfterCompareMatch[0]

                temp_oldPartialMatch.append(oldNodeAfterCompareMatch)
                temp_newPartialMatch.append(targetNewNodeAfterCompareMatch[0])

                # avoid repeated matching
                newChildNodeListAfterCompareMatch.remove(targetNewNodeAfterCompareMatch[0])

            elif matchedNumAllNewNode == 1:
                res[oldNodeAfterCompareMatch] = targetNewNode

                temp_oldPartialMatch.append(oldNodeAfterCompareMatch)
                temp_newPartialMatch.append(targetNewNode)
            elif matchedNum > 1:
                possibleMatchPair[oldNodeAfterCompareMatch] = list(targetNewNodeAfterCompareMatch)
                temp_oldPartialMatch.append(oldNodeAfterCompareMatch)
                for item in targetNewNodeAfterCompareMatch:
                    temp_newPartialMatch.append(item)

        # 没有匹配到的新旧节点
        notMatchedOldNodeList = []
        notMatchedNewNodeList = []
        for node in oldChildNodeList:
            if node not in temp_oldPartialMatch and node not in temp_oldCompareMatch:
                notMatchedOldNodeList.append(node)

        for node in newChildNodeList:
            if node not in temp_newPartialMatch and node not in temp_newCompareMatch:
                # filter widgets more likely to be a candidate
                if node.get('w') != 0 and node.get('h') * 1.0 / node.get('w') > 0.1 and (
                        'image' in node.get('class').lower() or node.get('text') != '' or node.get(
                    'resource-id') != '' or node.get('content-desc') != ''):
                    notMatchedNewNodeList.append(node)

        return res, possibleMatchPair, notMatchedOldNodeList, notMatchedNewNodeList, subingMatchedParentNodePairs

    # 通过比较resource_id，content-desc，text判断两个节点是否相似（两个相同即可）
    def isNodeMatched(self, node1, node2, isCompleteMatched, isChildNode):

        attribDic1 = node1.attrib
        attribDic2 = node2.attrib

        # diff the root node
        if 'class' not in attribDic1 and 'class' not in attribDic2:
            return True
        elif 'class' not in attribDic1 or 'class' not in attribDic2:
            return False

        # match abstracted root node
        if 'resource-id' not in attribDic1 and 'resource-id' not in attribDic2:
            return True

        if isCompleteMatched:
            resource_id1 = ''
            if 'resource-id' in attribDic1:
                resource_id1 = attribDic1['resource-id']
            resource_id2 = ''
            if 'resource-id' in attribDic2:
                resource_id2 = attribDic2['resource-id']

            idSame = resource_id1 == resource_id2 and resource_id1 != ''
            descriptSame = 'content-desc' in attribDic1 and 'content-desc' in attribDic2 and attribDic1[
                'content-desc'] == attribDic2['content-desc']
            textLikeSame = 'text' in attribDic1 and 'text' in attribDic2 and (
                    attribDic1['text'].encode('utf8') in attribDic2['text'].encode('utf8') or attribDic2[
                'text'].encode('utf8') in attribDic1['text'].encode('utf8'))

            Rule_IsSure = (idSame and descriptSame) or (idSame and textLikeSame) or (textLikeSame and descriptSame)

            if Rule_IsSure:
                return True
            return False

        else:
            if self.isNodeMatched(node1, node2, True, True):
                return True

            resource_id1 = ''
            if 'resource-id' in attribDic1:
                resource_id1 = attribDic1['resource-id']
            resource_id2 = ''
            if 'resource-id' in attribDic2:
                resource_id2 = attribDic2['resource-id']

            idSame = resource_id1 == resource_id2 and resource_id1 != ''
            descriptSame = 'content-desc' in attribDic1 and 'content-desc' in attribDic2 and attribDic1[
                'content-desc'] == attribDic2['content-desc']
            textLikeSame = 'text' in attribDic1 and 'text' in attribDic2 and (
                    attribDic1['text'].encode('utf8') in attribDic2['text'].encode('utf8') or attribDic2[
                'text'].encode('utf8') in attribDic1['text'].encode('utf8'))
            Rule_IsPossibleMatch = idSame or descriptSame or textLikeSame

            if Rule_IsPossibleMatch:
                return True
            return False

    def denotePartialSameParentAsSameParentByMatchedChildNodeList(self, matchedNodePairList):
        matchedParentNodePairList = {}
        isMatchedTwoRoot = True

        for oldNode, newNode in list(matchedNodePairList.items()):
            isMatchedTwoParent, partialMatchedParentNodePairList = self.denotePartialSameParentAsSameByMarchedChildNode(
                oldNode, newNode)
            isMatchedTwoRoot = isMatchedTwoRoot and isMatchedTwoParent
            matchedParentNodePairList.update(partialMatchedParentNodePairList)

        return isMatchedTwoRoot, matchedParentNodePairList

    def denotePartialSameParentAsSameByMarchedChildNode(self, oldNode, newNode):
        matchedParentNodePairList = {}
        isMatchedTwoParent = True

        parentLevel = 3

        while oldNode.get('parent') != None and newNode.get('parent') != None:
            oldParentNodeListWithinGivenLevel = self.getParentNodeListWithinGivenLevel(oldNode, parentLevel)
            newParentNodeListWithinGivenLevel = self.getParentNodeListWithinGivenLevel(newNode, parentLevel)
            hasFound = False

            # parent node compare match
            for newParentNode in newParentNodeListWithinGivenLevel:
                if self.isNodeMatched(oldNode.get('parent'), newParentNode, True, False):
                    matchedParentNodePairList[oldNode.get('parent')] = newParentNode

                    oldNode = oldNode.get('parent')
                    newNode = newParentNode

                    hasFound = True
                    break

            if hasFound:
                continue

            for oldParentNode in oldParentNodeListWithinGivenLevel:
                if self.isNodeMatched(oldParentNode, newNode.get('parent'), True, False):
                    matchedParentNodePairList[oldParentNode] = newNode.get('parent')

                    oldNode = oldParentNode
                    newNode = newNode.get('parent')

                    hasFound = True
                    break

            if hasFound:
                continue

            # parent node incomplete match

            if self.isNodeMatched(oldNode.get('parent'), newNode.get('parent'), False, False):
                matchedParentNodePairList[oldNode.get('parent')] = newNode.get('parent')

                oldNode = oldNode.get('parent')
                newNode = newNode.get('parent')
            else:
                isMatchedTwoParent = False
                break
        return isMatchedTwoParent, matchedParentNodePairList

    def matchXml(self, oldNode, newNode, matchedNodePairList):
        if not self.isNodeMatched(oldNode, newNode, True, False) and (
                oldNode not in matchedNodePairList or matchedNodePairList[oldNode] != newNode):
            return False

        # to find a direct api to get the number of child node
        oldChildNodeNum = 0
        newChildNodeNum = 0
        oldChildNodeList = []
        newChildNodeList = []
        for node in oldNode:
            oldChildNodeNum = oldChildNodeNum + 1
            oldChildNodeList.append(node)
        for node in newNode:
            newChildNodeNum = newChildNodeNum + 1
            newChildNodeList.append(node)

        matchedNum = 0
        for oldChildNode in oldChildNodeList:
            if oldChildNode in matchedNodePairList and matchedNodePairList[oldChildNode] in newChildNodeList:
                matchedNum = matchedNum + 1
                if not self.matchXml(oldChildNode, matchedNodePairList[oldChildNode], matchedNodePairList):
                    return False

            else:
                for newChildNode in newChildNodeList:
                    if self.isNodeMatched(oldChildNode, newChildNode, True, False):
                        matchedNum = matchedNum + 1
                        if not self.matchXml(oldChildNode, newChildNode, matchedNodePairList):
                            return False

        if matchedNum == min(len(oldChildNodeList), len(newChildNodeList)):
            return True
        else:
            return False

    def getParentNodeListWithinGivenLevel(self, givenNode, parentLevel):
        res = []
        level = 0
        while level < parentLevel:
            if givenNode.get('parent') != None:
                res.append(givenNode.get('parent'))
                givenNode = givenNode.get('parent')
                level = level + 1
            else:
                break
        return res

    def scoreTwoNode(self, matchedChildNodePairList, possibleMatchPair, notMatchedOldNodeList, notMatchedNewNodeList):
        matchedNum = len(matchedChildNodePairList)
        possibleMatchedNumOldNode = len(list(possibleMatchPair.keys()))
        notMatchedOldNodeListNum = len(notMatchedOldNodeList)
        newNodeSet = set()
        for key, value in list(possibleMatchPair.items()):
            for item in value:
                newNodeSet.add(item)

        matchScoreForOldNode = 1.0 * (matchedNum + possibleMatchedNumOldNode) / (
                matchedNum + possibleMatchedNumOldNode + notMatchedOldNodeListNum)
        matchScoreForOldNodeIsSureLevelMatch = 1.0 * (matchedNum) / (
                matchedNum + possibleMatchedNumOldNode + notMatchedOldNodeListNum)

        return matchScoreForOldNode, matchScoreForOldNodeIsSureLevelMatch

    def compareOldNewNode(self, oldNode, newNode):
        DONT_USE_ATTRS = ['xpath', 'class']
        hasSameAttrs = False
        sameAttrs = []
        for attrName in oldNode.attrs:
            if (attrName in newNode.attrs and oldNode.attrs[attrName] == newNode.attrs[attrName]):
                if (attrName not in DONT_USE_ATTRS):
                    hasSameAttrs = True
                    sameAttrs.append(attrName)
        # string similarity
        if (oldNode.string is None and oldNode.text == ''):
            string1 = ''
        elif (oldNode.string is None and oldNode.text != ''):
            string1 = oldNode.text.strip()
        else:
            string1 = oldNode.string.strip()
        stringValue = 0
        if (string1 == '' or newNode.string is None):
            stringValue = 0
        else:
            string1 = string1.lower()
            string2 = newNode.string.strip().lower()
            similarity = Levenshtein.jaro_winkler(string1, string2)
            if (similarity > 0.9):
                stringValue = similarity
        if (stringValue != 0):
            hasSameAttrs = True
            sameAttrs.append('string')
        return hasSameAttrs, sameAttrs, stringValue

    def colorLevSimi(self, str1, str2):
        return 1 - Levenshtein.distance(str1, str2) / max(len(str1), len(str2))

    def caculateDomNodeMatchDegreeLocation(self, oldNode, newNode, widgetLocation, screenWidth,
                                           screenHeight):
        attrlist = ['h', 'w', 'x', 'y']
        attr2value = {}
        attr2weight = {}
        locationAttrlistWidth = ['x', 'w']
        locationAttrlistHeight = ['y', 'h']
        weightlist = [1, 1, 1, 1]
        for i, attr in enumerate(attrlist):
            attr2value[attr] = 0
            attr2weight[attr] = weightlist[i]
        for attr in locationAttrlistWidth:
            attr2value[attr] = 1 - abs(widgetLocation[attr] - newNode.attrs[attr]) / screenWidth
        for attr in locationAttrlistHeight:
            attr2value[attr] = 1 - abs(widgetLocation[attr] - newNode.attrs[attr]) / screenHeight
        # xpath
        # attr2value['xpath'] = Levenshtein.jaro_winkler(oldNode.attrs['xpath'], newNode.attrs['xpath'])
        similarity = 0
        for attr in attrlist:
            similarity += attr2weight[attr] * attr2value[attr]
        return similarity

    def caculateDomNodeMatchDegreeFirst(self, oldNode, newNode):
        attr2weight = {}
        attr2value = {}
        attrlist = ['id', 'class', 'name', 'value', 'alt', 'src', 'href', 'onclick', 'linktext', 'title',
                    'placeholder', 'aria-label']
        attrInAttrSouplist = ['id', 'name', 'value', 'type', 'alt', 'src', 'href', 'onclick', 'title',
                              'placeholder', 'aria-label']
        otherslist = ['linktext', 'label', 'image']
        # weightlist = [0.86, 0.35, 0.80, 0.61, 0.44, 0.21, 0.57, 0.62, 0.62, 0.26, 0.66, 0.33, 0.66, 0.72, 0.60, 0.65,
        #               0.76, 0.31, 0.12]
        weightlist = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                      1, 1, 1]
        for i, attr in enumerate(attrlist):
            attr2value[attr] = 0
            attr2weight[attr] = weightlist[i]
        for attr in attrInAttrSouplist:
            if (attr in oldNode.attrs and attr in newNode.attrs and max(len(oldNode.attrs[attr]),
                                                                        len(newNode.attrs[attr]) != 0)):
                similarity = Levenshtein.jaro_winkler(oldNode.attrs[attr], newNode.attrs[attr])
                if (similarity > 0.8):
                    attr2value[attr] = similarity
                # attr2value[attr] = self.colorLevSimi(oldNode.attrs[attr], newNode.attrs[attr])
        # linktext
        if (oldNode.string is None and oldNode.text == ''):
            string1 = ''
        elif (oldNode.string is None and oldNode.text != ''):
            string1 = oldNode.text.strip()
        else:
            string1 = oldNode.string.strip()
        if (string1 == '' or newNode.string is None):
            attr2value['linktext'] = 0
        else:
            string1 = string1.lower()
            string2 = newNode.string.strip().lower()
            similarity = Levenshtein.jaro_winkler(string1, string2)
            if (similarity > 0.8):
                attr2value['linktext'] = similarity
        # class
        if ('class' in oldNode.attrs and 'class' in newNode.attrs and (len(oldNode.attrs['class']) != 0 or
                                                                       len(newNode.attrs['class']) != 0)):
            oldClassStr = ''.join(oldNode.attrs['class'])
            newClassStr = ''.join(newNode.attrs['class'])
            if (oldClassStr == newClassStr):
                attr2value['class'] = 1

        similarity = 0
        for attr in attrlist:
            similarity += attr2value[attr]
        return similarity

    def caculateColorNodeMatchDegree(self, oldNode, newNode, widgetLocation, base_image, current_image, screenWidth,
                                     screenHeight):
        attr2weight = {}
        attr2value = {}
        attrlist = ['id', 'class', 'name', 'value', 'type', 'tagName', 'alt', 'src', 'href', 'size', 'onclick', 'h', 'w'
            , 'xpath', 'x', 'y', 'linktext', 'label', 'image']
        attrInAttrSouplist = ['id', 'name', 'value', 'type', 'alt', 'src', 'href', 'onclick'
            , 'xpath']
        locationAttrlistWidth = ['x', 'w']
        locationAttrlistHeight = ['y', 'h']
        otherslist = ['tagName', 'size', 'linktext', 'label', 'image', 'class']
        # weightlist = [0.86, 0.35, 0.80, 0.61, 0.44, 0.21, 0.57, 0.62, 0.62, 0.26, 0.66, 0.33, 0.66, 0.72, 0.60, 0.65,
        #               0.76, 0.31, 0.12]
        weightlist = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                      1, 1, 1]
        for i, attr in enumerate(attrlist):
            attr2value[attr] = 0
            attr2weight[attr] = weightlist[i]
        for attr in locationAttrlistWidth:
            attr2value[attr] = 1 - abs(widgetLocation[attr] - newNode.attrs[attr]) / screenWidth
        for attr in locationAttrlistHeight:
            attr2value[attr] = 1 - abs(widgetLocation[attr] - newNode.attrs[attr]) / screenHeight
        for attr in attrInAttrSouplist:
            if (attr in oldNode.attrs and attr in newNode.attrs and max(len(oldNode.attrs[attr]),
                                                                        len(newNode.attrs[attr]) != 0)):
                attr2value[attr] = self.colorLevSimi(oldNode.attrs[attr], newNode.attrs[attr])
        # tagname
        if (oldNode.name == newNode.name):
            attr2value['tagName'] = 1
        # linktext
        if (oldNode.string is not None and newNode.string is not None):
            attr2value['linktext'] = self.colorLevSimi(oldNode.string, newNode.string)
        # image
        # oldImg = ImageUtil.ImageUtil.openCropImg(base_image,widgetLocation)
        # newImg = ImageUtil.ImageUtil.openCropImg(current_image,newNode)
        # if(oldImg==newImg):
        #     attr2value['image'] = 1
        # size
        if (oldNode.name == 'input' and newNode.name == 'input'):
            if ('size' in oldNode.attrs and 'size' in newNode.attrs and oldNode.attrs["size"] == newNode.attrs["size"]):
                attr2value['size'] = 1

        # class
        if ('class' in oldNode.attrs and 'class' in newNode.attrs and (len(oldNode.attrs['class']) != 0 or
                                                                       len(newNode.attrs['class']) != 0)):
            oldClassStr = ''.join(oldNode.attrs['class'])
            newClassStr = ''.join(newNode.attrs['class'])
            attr2value['class'] = self.colorLevSimi(oldClassStr, newClassStr)
        # label
        oldlabel = None
        newlabel = None
        if (oldNode.name == 'input' and newNode.name == 'input'):
            for label in oldNode.parent.find_all('label'):
                if 'id' in oldNode.attrs and 'id' in newNode.attrs and label.attrs['for'] == oldNode.attrs['id']:
                    oldlabel = label.string
            for label in newNode.parent.find_all('label'):
                if 'id' in oldNode.attrs and 'id' in newNode.attrs and label.attrs['for'] == newNode.attrs['id']:
                    newlabel = label.string
            if oldlabel is not None and newlabel is not None:
                print('label is not None')
                attr2value['label'] = self.colorLevSimi(oldlabel, newlabel)

        similarity = 0
        for attr in attrlist:
            similarity += attr2weight[attr] * attr2value[attr]
        return similarity

    def caculateNodeMatchDegree(self, oldNode, newNode, theta=0.8):
        idValue = 0
        titleValue = 0
        altValue = 0
        stringValue = 0
        nameValue = 0
        placeholderValue = 0
        valueValue = 0
        arialabelValue = 0
        typeValue = 0
        classValue = 0
        textValue = 0
        textAttr = {'value': 0, 'type': 0, 'title': 0, 'alt': 0, 'aria-label': 0, 'placeholder': 0}
        if ('id' in oldNode.attrs and 'id' in newNode.attrs and oldNode.attrs["id"] == newNode.attrs["id"]):
            idValue = 1
        if ('name' in oldNode.attrs and 'name' in newNode.attrs and oldNode.attrs["name"] == newNode.attrs["name"]):
            nameValue = 1

        for attr in textAttr:
            if (attr in oldNode.attrs and attr in newNode.attrs):
                similarity = Levenshtein.ratio(oldNode.attrs[attr], newNode.attrs[attr])
                if (similarity > theta):
                    textValue += similarity

        # if(oldNode.string is None and oldNode.text == ''):
        #     string1=''
        # elif (oldNode.string is None and oldNode.text != ''):
        #     string1=oldNode.text.strip()
        # else:
        #     string1 = oldNode.string.strip()
        # if(string1=='' or newNode.string is None ):
        #     stringValue=0
        # else:
        #     string1=string1.lower()
        #     string2=newNode.string.strip().lower()
        #     similarity = Levenshtein.ratio(string1, string2)
        #     if(similarity>theta):
        #         stringValue=similarity

        string1 = oldNode.text.strip().lower()
        string2 = newNode.text.strip().lower()


        similarity = Levenshtein.jaro_winkler(string1, string2)
        if string1 == '' or string2 == '':
            similarity = 0
        if similarity > theta:
            stringValue = similarity
        return idValue + stringValue + nameValue + textValue

    def preprocess(self, sentence):
        return [w for w in sentence.lower().split() if w not in self.stop_words]

    # def wordMoverDistance(self,string1,string2):
    #     string1=self.preprocess(string1)
    #     string2=self.preprocess(string2)
    #     distance = self.model.wmdistance(string1,string2)
    #     return 1/1+distance
    def jaccard(self, string1, string2):
        set1 = set(string1)
        set2 = set(string2)
        return len(set1 & set2) / len(set1 | set2)

    def editDistance(self, string1, string2):
        if (len(string1) == 0):
            return len(string2)
        if (len(string2) == 0):
            return len(string1)
        dp = [[] for i in range(len(string1) + 1)]
        for firstDimension in dp:
            for i in range(len(string2) + 1):
                firstDimension.append(0)
        for i in range(len(string1) + 1):
            dp[i][0] = i
        for i in range(len(string2) + 1):
            dp[0][i] = i
        for i in range(len(string1)):
            for j in range(len(string2)):
                if (string1[i] == string2[j]):
                    dp[i + 1][j + 1] = dp[i][j]
                else:
                    dp[i + 1][j + 1] = min(dp[i][j] + 1, dp[i + 1][j] + 1, dp[i][j + 1] + 1)
        return 1 - dp[len(string1)][len(string2)] / max(len(string1), len(string2))

    def isHtmlNodeMatched(self, oldNode, newNode):
        idSame = 'id' in oldNode.attrs and 'id' in newNode.attrs and oldNode.attrs["id"] == newNode.attrs["id"]
        titleSame = 'title' in oldNode.attrs and 'title' in newNode.attrs and oldNode.attrs["title"] == newNode.attrs[
            "title"]
        stringSame = oldNode.string != None and newNode.string != None and oldNode.string == newNode.string
        altSame = 'alt' in oldNode.attrs and 'alt' in newNode.attrs and oldNode.attrs["alt"] == newNode.attrs["alt"]

        Rule_IsSure = idSame or titleSame or stringSame or altSame
        if Rule_IsSure:
            return True
        return False

    def matchHtmlNodePair(self, oldNodeList, newNodeList):

        # todo descript,text,id, with their index;  scrollable,etc

        matchDict = {}
        matchNewNodeList = []
        for oldNode in oldNodeList:
            matchDict[oldNode] = []
            sureMatchedNum = 0  # 相似的节点数目
            for newNode in newNodeList:
                if self.isHtmlNodeMatched(oldNode, newNode):  # 根据xml中的几个参数进行匹配
                    matchDict[oldNode].append(newNode)
                    matchNewNodeList.append(newNode)
                    # sureMatchedNum = sureMatchedNum + 1
                    # sureMatchCandidateNode = newNode
        possibleMatchedNodePair = {}
        notMatchedNewNodeList = []
        notMatchedOldNodeList = []
        sureMatchedNodePairList = {}
        for oldNode in matchDict.keys():
            if (len(matchDict[oldNode]) == 1):
                sureMatchedNodePairList[oldNode] = matchDict[oldNode][0]
            elif (len(matchDict[oldNode]) == 0):
                notMatchedNewNodeList.append(oldNode)
            else:
                possibleMatchedNodePair[oldNode] = matchDict[oldNode]
        for newNode in newNodeList:
            if (newNode not in matchNewNodeList):
                notMatchedNewNodeList.append(newNode)
        return sureMatchedNodePairList, possibleMatchedNodePair, notMatchedOldNodeList, notMatchedNewNodeList

    def isHtmlMatch(self, html1, html2, isSureLevelMatch, isSureMatch, givenThreshold=0.6, isBuildSBridge=False):
        oldRoot = self.getRoot(html1)
        newRoot = self.getRoot(html2)

        # 对xml进行重写，把默认xml的index重写为脚本中的索引index ，保存在本地的字典里

        self.denoteCurrentHtmlIndex(oldRoot)
        self.initIDDic()
        self.denoteCurrentHtmlIndex(newRoot)
        self.initIDDic()

        # 把所有的叶子节点和父节点都抽出来备用
        self.getChildNodeList(oldRoot.html)
        oldChildNodeList = list(self.childNodeRes)
        self.childNodeRes = []

        self.getChildNodeList(newRoot.html)
        newChildNodeList = list(self.childNodeRes)
        self.childNodeRes = []

        self.getParentNodeList(oldRoot.html)
        oldParentNodeList = list(self.parentNodeRes)
        self.parentNodeRes = []

        self.getParentNodeList(newRoot.html)
        newParentNodeList = list(self.parentNodeRes)
        self.parentNodeRes = []

        # -----------------------------------------------------------------------------------------------------------------
        # 上面均是一些匹配过程的预处理操作

        # denote a map from childNode to bigggest parentNode node Covered with other sub-childNode parentNode
        # 将单一屏幕上有若干ID相同的控件与其最大"不相交父节点"建立映射关系，以供之后匹配过程使用；这对应着android里的列表类结构
        # 从而用于防止子节点的属性缺失
        # oldChild2ParentDic, newChild2ParentDic = self.denoteMaxNoneCoveredParentToChildNode(oldChildNodeList,
        #                                                                                     newChildNodeList)
        # define rules to match child nodes
        # 基于xml的属性匹配叶子节点，同时利用父子节点间的结构信息优化匹配
        # 分别为：匹配叶子节点，可能匹配叶子节点，不匹配叶子节点，可能优化的相邻父节点（sublingMatchedParentNodePairs）
        # matchedChildNodePairList, possibleMatchPair, notMatchedOldNodeList, notMatchedNewNodeList, sublingMatchedParentNodePairs = self.matchNodePair(
        #     oldChildNodeList, newChildNodeList, oldChild2ParentDic, newChild2ParentDic)
        sureMatchedLeafNodePairList, possibleMatchedleafNodePair, notMatchedOldLeafNodeList, notMatchedNewleafNodeList = self.matchHtmlNodePair(
            oldChildNodeList, newChildNodeList)
        # print(sureMatchedLeafNodePairList)
        isMatchedTwoChildList = False

        # set threshold aroad to isSureMatch
        scoreTheshrold = givenThreshold if not isSureMatch else givenThreshold - 0.1
        # 基于控件匹配的比例定义xml间的匹配计算比例然后和设定的阈值进行比较
        scoreMappingBig, scoreMappingIsSureMatch = self.scoreTwoNode(sureMatchedLeafNodePairList,
                                                                     possibleMatchedleafNodePair,
                                                                     notMatchedOldLeafNodeList,
                                                                     notMatchedNewleafNodeList)

        if scoreMappingBig >= scoreTheshrold:
            isMatchedTwoChildList = True

        # 计算父节点间的匹配关系
        matchedParentNodePairList, possibleParentMatchPair, _, _ = self.matchHtmlNodePair(oldParentNodeList,
                                                                                          newParentNodeList)

        return isMatchedTwoChildList, sureMatchedLeafNodePairList, matchedParentNodePairList, possibleMatchedleafNodePair, possibleParentMatchPair, notMatchedOldLeafNodeList, notMatchedNewleafNodeList, scoreMappingBig

    def seperateAreaMatch(self, oldXml, newXml):
        subOldAreas = self.getSubAreas(oldXml)
        subNewAreas = self.getSubAreas(newXml)

        for subOldArea in subOldAreas:
            hasFound = False
            for subNewArea in subNewAreas:
                if self.isXmlMatchGivenAreas(oldXml, newXml, subOldArea, subNewArea):
                    hasFound = True
                    break
            if hasFound:
                subOldAreas.remove(subOldArea)
                subNewAreas.remove(subNewArea)
            else:
                return False
        if subNewAreas != []:
            return False
        return True

    def isXmlMatchGivenAreas(self, oldXml, newXml, subOldArea, subNewArea):
        return False

    def denoteMaxNoneCoveredParentToChildNode(self, oldChildNodeList, newChildNodeList):
        idNumLargerThan1 = []
        oldChild2ParentDic = {}
        newChild2ParentDic = {}
        idNumDic = {}
        mergedList = oldChildNodeList + newChildNodeList
        for item in mergedList:
            if item.get('resource-id') != '':
                if item.get('resource-id') not in idNumDic:
                    idNumDic[item.get('resource-id')] = 1
                else:
                    idNumDic[item.get('resource-id')] = idNumDic[item.get('resource-id')] + 1

        for id_, idNum in list(idNumDic.items()):
            if idNum > 2:
                idNumLargerThan1.append(id_)

        for id_ in idNumLargerThan1:

            # old Child
            itemWithSameId = list([])
            for oldChild in oldChildNodeList:
                if oldChild.get('resource-id') == id_:
                    itemWithSameId.append(oldChild)

            parentItemWithSameId = list(itemWithSameId)
            if len(itemWithSameId) == 1:
                oldChild2ParentDic[itemWithSameId[0]] = itemWithSameId[0]
            elif len(itemWithSameId) == 0:
                pass
            else:
                while not self.isCoveredNodeList(self.getNodeListParent(parentItemWithSameId)):
                    parentItemWithSameId = self.getNodeListParent(parentItemWithSameId)

                for index in range(len(itemWithSameId)):
                    oldChild2ParentDic[itemWithSameId[index]] = parentItemWithSameId[index]

            # new Child
            itemWithSameId = list([])
            for newChild in newChildNodeList:
                if newChild.get('resource-id') == id_:
                    itemWithSameId.append(newChild)

            parentItemWithSameId = list(itemWithSameId)
            if len(itemWithSameId) == 1:
                newChild2ParentDic[itemWithSameId[0]] = itemWithSameId[0]
            elif len(itemWithSameId) == 0:
                pass
            else:
                while not self.isCoveredNodeList(self.getNodeListParent(parentItemWithSameId)):
                    parentItemWithSameId = self.getNodeListParent(parentItemWithSameId)

                for index in range(len(itemWithSameId)):
                    newChild2ParentDic[itemWithSameId[index]] = parentItemWithSameId[index]

        return oldChild2ParentDic, newChild2ParentDic

    def isCoveredTwoNode(self, node1, node2, isConsiderNode1LargerThanNode2=False):
        x1, y1, w1, h1 = node1.get('x'), node1.get('y'), node1.get('w'), node1.get('h')
        x2, y2, w2, h2 = node2.get('x'), node2.get('y'), node2.get('w'), node2.get('h')

        if x1 is None or y1 is None or w1 is None or h1 is None:
            return False
        if x2 is None or y2 is None or w2 is None or h2 is None:
            return False

        if not isConsiderNode1LargerThanNode2:
            if abs(x2 + 0.5 * w2 - x1 - 0.5 * w1) < (0.5 * w1 + 0.5 * w2) and abs(y2 + 0.5 * h2 - y1 - 0.5 * h1) < (
                    0.5 * h1 + 0.5 * h2):
                return True
            if x1 == x2 and y1 == y2 and w1 == w2 and h1 == h2:
                return True

            return False
        else:
            if w1 * h1 < w2 * h2:
                return False
            if abs(x2 + 0.5 * w2 - x1 - 0.5 * w1) < (0.5 * w1 + 0.5 * w2) and abs(y2 + 0.5 * h2 - y1 - 0.5 * h1) < (
                    0.5 * h1 + 0.5 * h2):
                return True
            if x1 == x2 and y1 == y2 and w1 == w2 and h1 == h2:
                return True

            return False

    def isCoveredNodeList(self, nodeList):
        for index_i, i in enumerate(nodeList):
            for index_j, j in enumerate(nodeList):
                if index_i == index_j:
                    continue
                else:
                    if self.isCoveredTwoNode(i, j):
                        return True
        return False

    def getNodeListParent(self, nodeList):
        res = []
        for node in nodeList:
            if node.get('parent') == None:
                raise RuntimeError('no parent node exists, check the method of define areas')
            else:
                res.append(node.get('parent'))
        return res

    # 返回和和新节点有覆盖关系的节点集合 shouldMatchedNewNodeList 以及新旧节点的最恰当的子节点的匹配对 res
    def denoteSublingNodeAsSureMatch(self, oldNode, sureMatchCandidateNode, oldChild2ParentDic, newChild2ParentDic,
                                     newChildNodeList, subingMatchedParentNodePairs):
        if oldNode not in oldChild2ParentDic or sureMatchCandidateNode not in newChild2ParentDic:
            return {}, []
        shouldMatchedNewNodeList = []
        res = {}

        matchedOldParentNode = oldChild2ParentDic[oldNode]
        matchedNewParentNode = newChild2ParentDic[sureMatchCandidateNode]

        # 从映射关系中找到唯一匹配项
        subingMatchedParentNodePairs[matchedOldParentNode] = matchedNewParentNode

        oldThisIdList = []
        newThisIdList = []

        for newChildNode in newChildNodeList:
            # 如果两个节点符合重合规则
            if self.isCoveredTwoNode(newChildNode, matchedNewParentNode):
                shouldMatchedNewNodeList.append(newChildNode)

        for oldNode, oldParentNode in list(oldChild2ParentDic.items()):
            # 如果父母节点匹配则把子节点添加
            if oldParentNode == matchedOldParentNode:
                oldThisIdList.append(oldNode)
        for newNode, newParentNode in list(newChild2ParentDic.items()):
            if newParentNode == matchedNewParentNode:
                newThisIdList.append(newNode)

        # 找到最匹配的一对子节点
        for i in oldThisIdList:
            hasFoundChildPair = False
            for j in newThisIdList:
                if (i.get('resource-id') == j.get('resource-id') and j.get('resource-id') != '') or (
                        i.get('content-desc') == j.get('content-desc') and j.get('content-desc') != '') or (
                        i.get('text') == j.get('text') and j.get('text') != ''):
                    res[i] = j
                    hasFoundChildPair = True
            if not hasFoundChildPair:
                res[i] = matchedNewParentNode

        return res, shouldMatchedNewNodeList

    def sublingProcessPossibleParentMatchPair(self, possibleParentMatchPair, sublingMatchedParentNodePairs):
        matchedParentNodePairListAfterSublingProcess = {}
        possibleParentMatchPairAfterSublingProcess = {}

        for oldParentNode, newParentNodeList in list(possibleParentMatchPair.items()):
            for newParentNode in newParentNodeList:
                isCoveredBySublingMatched = False
                for targetedOldParentNode, targetedNewParentNode in list(sublingMatchedParentNodePairs.items()):
                    if self.isCoveredTwoNode(targetedOldParentNode, oldParentNode, True) and self.isCoveredTwoNode(
                            targetedNewParentNode, newParentNode, True):
                        isCoveredBySublingMatched = True
                        break

                if isCoveredBySublingMatched:
                    matchedParentNodePairListAfterSublingProcess[oldParentNode] = newParentNode
                    # newParentNodeList_ = newParentNodeList.remove(newParentNode)
                    # possibleParentMatchPairAfterSublingProcess[oldParentNode] = newParentNodeList_
                    break
            if not isCoveredBySublingMatched:
                possibleParentMatchPairAfterSublingProcess[oldParentNode] = newParentNodeList

        return matchedParentNodePairListAfterSublingProcess, possibleParentMatchPairAfterSublingProcess

    # water api
    def getElementTriggerWithoutRepair(self, testStep, xml1, xml2):
        selector = testStep['handle']

        widget = testStep['widget']

        # 'click point' return None directly
        if widget['x'] == -1 and widget['y'] == -1 and widget['w'] == 0 and widget['h'] == 0:
            return 'notNeedRepair'
        else:
            x, y, w, h = widget['x'], widget['y'], widget['w'], widget['h']

        if 'find_element_by_id' in testStep['handle'] and testStep['handle'][0] != '#':
            # print testStep['handle'].strip()
            attribute = 'resource-id'
            value = testStep['handle'].strip().split('_id')[1][2:-2]
            # el = driver.find_element_by_id(testStep['handle'].strip().split('_id')[1][2:-2])
        elif 'find_element_by_accessibility_id' in testStep['handle'] and testStep['handle'][0] != '#':
            # print testStep['handle'].strip().split('_id')[1][2:-2]
            attribute = 'content-desc'
            value = testStep['handle'].strip().split('_id')[1][2:-2]
            # el = driver.find_element_by_accessibility_id(testStep['handle'].strip().split('_id')[1][2:-2])
        elif 'find_element_by_class_name' in testStep['handle'] and testStep['handle'][0] != '#':
            # print testStep['handle'].strip()
            attribute = 'class'
            value = testStep['handle'].strip().split('_name')[1][2:-2]
            # el = driver.find_element_by_class_name(testStep['handle'].strip().split('_name')[1][2:-2])
        elif 'find_elements_by_id' in testStep['handle'] and testStep['handle'][0] != '#':
            attribute = 'resource-id'
            value = testStep['handle'].strip().split('_id')[1][2:].split(')')[0][0:-1]
            # el = driver.find_elements_by_id(testStep['handle'].strip().split('_id')[1][2:].split(')')[0][0:-1])[
            #   int(testStep['handle'].strip().split(')[')[1][0:-1])]
            # print testStep['handle'].strip().split('_id')[1][2:].split(')')[0][0:-1]
            # print int(testStep['handle'].strip().split(')[')[1][0:-1])
        elif 'find_elements_by_accessibility_id' in testStep['handle'] and testStep['handle'][0] != '#':
            attribute = 'content-desc'
            value = testStep['handle'].strip().split('_id')[1][2:].split(')')[0][0:-1]
            # el = driver.find_elements_by_accessibility_id(
            #   testStep['handle'].strip().split('_id')[1][2:].split(')')[0][0:-1])[
            #  int(testStep['handle'].strip().split(')[')[1][0:-1])]
            # print testStep['handle'].strip().split('_id')[1][2:].split(')')[0][0:-1]
            # print int(testStep['handle'].strip().split(')[')[1][0:-1])
        elif 'find_elements_by_class_name' in testStep['handle'] and testStep['handle'][0] != '#':
            # print testStep['handle'].strip().split('_name')[1][2:].split(')')[0][0:-1]
            # print int(testStep['handle'].strip().split(')[')[1][0:-1])
            attribute = 'class'
            value = testStep['handle'].strip().split('_name')[1][2:].split(')')[0][0:-1]
            # el = \
            # driver.find_elements_by_class_name(testStep['handle'].strip().split('_name')[1][2:].split(')')[0][0:-1])[
            #   int(testStep['handle'].strip().split(')[')[1][0:-1])]
            # print i.strip().split('_name')[1][2:].split(')')[0][0:-1]
        elif 'find_element_by_android_uiautomator' in testStep['handle'] and testStep['handle'][0] != '#':
            # print testStep['handle'].strip().split('_name')[1][2:].split(')')[0][0:-1]
            # print int(testStep['handle'].strip().split(')[')[1][0:-1])
            attribute = 'text'
            value = testStep['handle'].strip().split('_uiautomator')[1][2:][0:-2].replace("\\", "")
            value = value.split("\"")[1]
            print(testStep['handle'].strip().split('_uiautomator')[1][2:][0:-2].replace("\\", ""))
            # el = driver.find_element_by_android_uiautomator(
            #   testStep['handle'].strip().split('_uiautomator')[1][2:][0:-2].replace("\\", ""))
            # print i.strip().split('_name')[1][2:].split(')')[0][0:-1]

        else:
            # Logger.mainLogger.info("test handle is not defined in 1043,xmlMatch")
            # Logger.mainLogger.info(str(testStep['selector']))
            return 'notNeedRepair'

        oldRoot = self.getRoot(xml1)
        newRoot = self.getRoot(xml2)

        # class, id , text, desc  index denote
        self.denoteCurrentXmlIndex(oldRoot)
        self.initIDDic()

        self.denoteCurrentXmlIndex(newRoot)
        self.initIDDic()

        # define rules to match child nodes

        self.getChildNodeList(oldRoot)
        oldChildNodeList = list(self.childNodeRes)
        self.childNodeRes = []

        self.getChildNodeList(newRoot)
        newChildNodeList = list(self.childNodeRes)
        self.childNodeRes = []

        self.getParentNodeList(oldRoot)
        oldParentNodeList = list(self.parentNodeRes)
        self.parentNodeRes = []

        self.getParentNodeList(newRoot)
        newParentNodeList = list(self.parentNodeRes)
        self.parentNodeRes = []

        oldNodeList = oldChildNodeList + oldParentNodeList
        newNodeList = newChildNodeList + newParentNodeList

        # Logger.mainLogger.info("x, y, w, h, attribute, value, oldNodeList,textContains,textStart:"+str(x)+' '+str(y)+' '+str(w)+' '+str(h)+' '+str(attribute)+' '+str(value)+' oldNodeList '+str(textContains)+' '+str(textStart))
        oldTargetNode, oldTargetNodeIndex = self.findNodeByBoundAndAttribute(x, y, w, h, attribute, value, oldNodeList)

        if oldTargetNodeIndex == None:
            pass
            # Logger.mainLogger.info("oldTargetNode == None is"+str(oldTargetNode is None))
            # Logger.mainLogger.info("oldTargetNodeIndex == None")

        if oldTargetNodeIndex == None: return 'notNeedRepair'

        newTargetNode = self.findNodeByAttributeAndIndex(attribute, value, oldTargetNodeIndex, newNodeList)

        if newTargetNode == None: return self.findWaterSimilarNodeByAttributeAndIndex(oldTargetNode, newNodeList)

        # todo for water application only
        if newTargetNode != None:
            return [newTargetNode.attrib]

        return 'notNeedRepair'

    def findNodeByBoundAndAttribute(self, x, y, w, h, attribute, value, oldNodeList):

        # selector diff when difining
        # if attribute == 'description':
        #     attribute = 'content-desc'

        for node in oldNodeList:
            if x == node.get('x') and y == node.get('y') and w == node.get('w') and h == node.get(
                    'h'):
                pass
                # Logger.mainLogger.info('found same bounds')
                # Logger.mainLogger.info(value)
                # Logger.mainLogger.info(node.get(attribute))

            if x == node.get('x') and y == node.get('y') and w == node.get('w') and h == node.get(
                    'h') and value == node.get(attribute):
                if attribute == 'resource-id':
                    return node, node.get('idIndex')
                elif attribute == 'content-desc':
                    return node, node.get('content-descIndex')
                elif attribute == 'text':
                    return node, node.get('textIndex')
                elif attribute == 'class':
                    return node, node.get('classIndex')

                else:
                    raise RuntimeError('not support api other than id,content-desc,text,class now')
        return None, None

    def findNodeByAttributeAndIndex(self, attribute, value, oldTargetNodeIndex, newNodeList):

        # selector diff when difining
        # if attribute == 'description':
        #     attribute = 'content-desc'

        if attribute == 'resource-id':
            specificIndex = 'idIndex'
        elif attribute == 'content-desc':
            specificIndex = 'content-descIndex'
        elif attribute == 'text':
            specificIndex = 'textIndex'
        elif attribute == 'class':
            specificIndex = 'classIndex'

        else:
            raise RuntimeError('not support api other than id,content-desc,text,class now')

        for node in newNodeList:
            if value == node.get(attribute) and oldTargetNodeIndex == node.get(specificIndex):
                return node
        return None

    def findWaterSimilarNodeByAttributeAndIndex(self, oldTargetNode, newNodeList):
        candidateNodeList = []
        for node in newNodeList:
            if oldTargetNode.get("resource-id") == node.get("resource-id") and node.get("resource-id") != '':
                candidateNodeList.append(node.attrib)
        for node in newNodeList:
            if oldTargetNode.get('content-desc') == node.get('content-desc') and node.get('content-desc') != '':
                candidateNodeList.append(node.attrib)
        for node in newNodeList:
            if oldTargetNode.get('text') == node.get('text') and node.get('text') != '':
                candidateNodeList.append(node.attrib)
        for node in newNodeList:
            if oldTargetNode.get('class') == node.get('class') and node.get('class') != '':
                candidateNodeList.append(node.attrib)
        return candidateNodeList
