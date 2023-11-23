# coding:utf-8

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import xpathProcess
from PIL import Image
import StringUtil
import shelve
import os
import random
import sys

#imp.reload(sys)
#reload(sys)

#sys.setdefaultencoding('utf8')
# sys.setdefaultencoding( 'utf-8' )
success = True




class RecordScreenAndWidget(object):

    def __init__(self,  testCaseList, url,chromeDriverPath):
        self.url=url
        self.testCaseList = testCaseList
        self.chromeDriverPath=chromeDriverPath
    @staticmethod
    def getElementByRecordStep(driver,testStep):
        if 'find_element_by_id' in testStep['handle'] and testStep['handle'][0] != '#':
            # 按id查找元素
            tempContent1 = testStep['handle'].strip()  # 去除两侧空白
            tempList1 = tempContent1.split('_id')  # 以'_id'为界进行分割
            if len(tempList1) < 2:
                # TODO#
                assert False
            tempContent2 = tempList1[1]
            if len(tempContent2) < 5:  # ("") 长度为4
                # TODO#
                assert False
            el = driver.find_element_by_id(tempContent2[2:-2])
        elif 'find_element_by_name' in testStep['handle'] and testStep['handle'][0] != '#':
            # 按id查找元素
            tempContent1 = testStep['handle'].strip()  # 去除两侧空白
            tempList1 = tempContent1.split('_name')  # 以'_id'为界进行分割
            if len(tempList1) < 2:
                # TODO#
                assert False
            tempContent2 = tempList1[1]
            if len(tempContent2) < 5:  # ("") 长度为4
                # TODO#
                assert False
            el = driver.find_element_by_name(tempContent2[2:-2])
        elif 'find_element_by_accessibility_id' in testStep['handle'] and testStep['handle'][0] != '#':
            # 按accessibility找元素
            tempContent1 = testStep['handle'].strip()  # 去除两侧空白
            tempList1 = tempContent1.split('_id')  # 以'_id'为界进行分割
            if len(tempList1) < 2:
                # TODO#
                assert False
            tempContent2 = tempList1[1]
            if len(tempContent2) < 5:  # ("") 长度为4
                # TODO#
                assert False
            el = driver.find_element_by_accessibility_id(tempContent2[2:-2])
        elif 'find_element_by_link_text' in testStep['handle'] and testStep['handle'][0] != '#':
            # 按id查找元素
            tempContent1 = testStep['handle'].strip()
            tempList1 = tempContent1.split('_link_text')
            if len(tempList1) < 2:
                assert False
            tempContent2 = tempList1[1]
            if len(tempContent2) < 5:  # ("") 长度为4
                assert False
            el = driver.find_element_by_link_text(tempContent2[2:-2])
        elif ('find_element_by_css_selector' in testStep['handle'] and testStep['handle'][0] != '#'):
            tempContent1 = testStep['handle'].strip()
            tempList1 = tempContent1.split('_css_selector')
            if len(tempList1) < 2:
                assert False
            tempContent2 = tempList1[1]
            if len(tempContent2) < 5:  # ("") 长度为4
                assert False
            el = driver.find_element_by_css_selector(StringUtil.StringUtil.escapeString(tempContent2[2:-2]))
        elif ('find_element_by_xpath' in testStep['handle'] and testStep['handle'][0] != '#'):
            tempContent1 = testStep['handle'].strip()
            tempList1 = tempContent1.split('_xpath')
            if len(tempList1) < 2:
                assert False
            tempContent2 = tempList1[1]
            if len(tempContent2) < 5:  # ("") 长度为4
                assert False
            el = driver.find_element_by_xpath(StringUtil.StringUtil.escapeString(tempContent2[2:-2]))
        elif 'find_element_by_class_name' in testStep['handle'] and testStep['handle'][0] != '#':
            # 按类名找元素
            tempContent1 = testStep['handle'].strip()  # 去除两侧空白
            tempList1 = tempContent1.split('_name')  # 以'_id'为界进行分割
            if len(tempList1) < 2:
                # TODO#
                assert False
            tempContent2 = tempList1[1]
            if len(tempContent2) < 5:  # ("") 长度为4
                # TODO#
                assert False
            el = driver.find_element_by_class_name(tempContent2[2:-2])
        elif 'find_elements_by_id' in testStep['handle'] and testStep['handle'][0] != '#':
            # 按id查找多个元素
            tempContent1 = testStep['handle'].strip()  # 去除两侧空白
            tempList1 = tempContent1.split('_id')  # 以'_id'为界进行分割
            if len(tempList1) < 2:
                # TODO#
                assert False
            tempContent2 = tempList1[1]
            if len(tempContent2) < 8:  # ("")[] 长度为6
                # TODO#
                assert False
            tempContent3 = tempContent2[2:]  # 先去掉前面的 ("
            tempList2 = tempContent3.split(')')  # 按照 ) 分界
            if len(tempList2) < 2:
                # TODO#
                assert False
            tempContent4 = tempList2[0]
            if len(tempContent4) < 2:  # " 长度为1
                # TODO#
                assert False
            tempList3 = tempContent1.split(')[')
            if len(tempList3) < 2:
                # TODO#
                assert False
            tempContent5 = tempList3[1]
            if len(tempContent5) < 2:  # ] 长度为1
                # TODO#
                assert False
            el = driver.find_elements_by_id(tempContent4[0:-1])[int(tempContent5[0:-1])]
        elif 'find_elements_by_accessibility_id' in testStep['handle'] and testStep['handle'][0] != '#':
            # 按accessibility查找多个元素
            tempContent1 = testStep['handle'].strip()  # 去除两侧空白
            tempList1 = tempContent1.split('_id')  # 以'_id'为界进行分割
            if len(tempList1) < 2:
                # TODO#
                assert False
            tempContent2 = tempList1[1]
            if len(tempContent2) < 8:  # ("")[] 长度为6
                # TODO#
                assert False
            tempContent3 = tempContent2[2:]  # 先去掉前面的 ("
            tempList2 = tempContent3.split(')')  # 按照 ) 分界
            if len(tempList2) < 2:
                # TODO#
                assert False
            tempContent4 = tempList2[0]
            if len(tempContent4) < 2:  # " 长度为1
                # TODO#
                assert False
            tempList3 = tempContent1.split(')[')
            if len(tempList3) < 2:
                # TODO#
                assert False
            tempContent5 = tempList3[1]
            if len(tempContent5) < 2:  # ] 长度为1
                # TODO#
                assert False
            el = driver.find_elements_by_accessibility_id(tempContent4[0:-1])[int(tempContent5[0:-1])]
        elif 'find_elements_by_class_name' in testStep['handle'] and testStep['handle'][0] != '#':
            # 按类名查找多个元素
            tempContent1 = testStep['handle'].strip()  # 去除两侧空白
            tempList1 = tempContent1.split('_name')  # 以'_name'为界进行分割
            if len(tempList1) < 2:
                # TODO#
                assert False
            tempContent2 = tempList1[1]
            if len(tempContent2) < 8:  # ("")[] 长度为6
                # TODO#
                assert False
            tempContent3 = tempContent2[2:]  # 先去掉前面的 ("
            tempList2 = tempContent3.split(')')  # 按照 ) 分界
            if len(tempList2) < 2:
                # TODO#
                assert False
            tempContent4 = tempList2[0]
            if len(tempContent4) < 2:  # " 长度为1
                # TODO#
                assert False
            tempList3 = tempContent1.split(')[')
            if len(tempList3) < 2:
                # TODO#
                assert False
            tempContent5 = tempList3[1]
            if len(tempContent5) < 2:  # ] 长度为1
                # TODO#
                assert False
            try:
                el = driver.find_elements_by_class_name(tempContent4[0:-1])[int(tempContent5[0:-1])]
            except:
                print(testStep['handle'])
                print(tempContent4[0:-1])
                print(int(tempContent5[0:-1]))
                quit()
        else:
            el=None
        return el



    def instrumentDriver(self):
        print('\nprocess 1----record screenshot and element in the old version n\n')
        for testIndex, testCase in enumerate(self.testCaseList):
            print('==========test case {} start==========='.format(testIndex))
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument("--force-device-scale-factor=1")
            driver = webdriver.Chrome(executable_path=self.chromeDriverPath, chrome_options=chrome_options)
            driver.get(self.url)
            time.sleep(5)

            for indexStep, testStep in enumerate(testCase):
                print('\n====================================================================================\n')
                print('test step {} start'.format(indexStep + 1))
                if "time.sleep" in testStep['handle'] and testStep['handle'][0] != "#":
                    # 识别到了睡眠语句
                    tempContent1 = testStep['handle'].strip('\n')
                    tempList1 = tempContent1.split('(')  # 以左括号为分界
                    if len(tempList1) < 2:
                        # TODO#
                        assert False
                    tempContent2 = tempList1[1]
                    if len(tempContent2) < 2:
                        # TODO#
                        assert False
                    # 去除右括号，至少留下一位数字
                    time.sleep(int(tempContent2[0:-1]))

                    if indexStep == len(testCase) - 1:
                        testStep['nextHtml'] = str(driver.page_source)
                        if indexStep != 0:
                            self.get_html_as_file(testStep['nextHtml'], testStep['htmlPathNext'])
                            self.get_full_screenshot_as_file(driver,testCase[indexStep - 1]['screenshotPathNext'])
                            # driver.get_screenshot_as_file(testCase[indexStep - 1]['screenshotPathNext'])
                        time.sleep(1)

                    if indexStep == len(testCase) - 2 and "time.sleep" in testCase[indexStep + 1]['handle']:
                        if indexStep != 0:
                            testCase[indexStep - 1]['nextHtml'] = str(driver.page_source)
                            self.get_html_as_file(testCase[indexStep - 1]['nextHtml'], testCase[indexStep - 1]['htmlPathNext'])
                            self.get_full_screenshot_as_file(driver,testCase[indexStep - 1]['screenshotPathNext'])
                            # driver.get_screenshot_as_file(testCase[indexStep - 1]['screenshotPathNext'])
                        time.sleep(1)

                    continue

                time.sleep(1)
                scaleRatio=self.get_full_screenshot_as_file(driver,testStep['screenshotPathInit'])
                # driver.get_screenshot_as_file(testStep['screenshotPathInit'])
                testStep['html']=str(driver.page_source)
                self.get_html_as_file(testStep['html'], testStep['htmlPathInit'])

                # 更换提示语句输出方式
                print('screen capture before test step {}'.format(indexStep + 1))
                print('perform test step {}: {}'.format(indexStep + 1, testStep['handle']))

                el=RecordScreenAndWidget.getElementByRecordStep(driver,testStep)
                if "driver.back()" in testStep['handle'] and testStep['handle'][0] != "#":
                    driver.back()

                elif "driver.press_keycode(" in testStep['handle'] and testStep['handle'][0] != "#":
                    driver.press_keycode(int(testStep['handle'].split('(')[1][0:-1]))

                if 'find_element' in testStep['handle'] and testStep['handle'][0] != '#':
                    location = el.location
                    size = el.size
                    widget = {'x': location['x']*scaleRatio, 'y': location['y']*scaleRatio, 'w': size['width']*scaleRatio, 'h': size['height']*scaleRatio}
                    testStep['widget'] = widget
                    widgetXpath=xpathProcess.generateXpathFromSeleniumElement(el,"")
                    testStep["xpath"]=widgetXpath
                    assert widget['w'] > 0 and widget['h'] > 0, 'The size of widget should not be 0'
                    print('record test element x,y,w,h: {},{},{},{}'.format(widget['x'], widget['y'], widget['w'],
                                                                            widget['h']))
                    print ('record test element xpath: {}'.format(widgetXpath))

                    # locationFile.write("x:" + str(location['x']) + ":")
                    # locationFile.write("y:" + str(location['y']) + ":")
                    ##locationFile.write("width:" + str(size['width']) + ":")
                    # locationFile.write("height:" + str(size['height']) + ":")
                    # locationFile.close()

                if ".click()" in testStep['action'] and testStep['action'] != "#":
                    time.sleep(1)
                    el.click()

                elif ".clear()" in testStep['action'] and testStep['action'] != "#":
                    el.clear()

                elif ".send_keys" in testStep['action'] and testStep['action'][0] != "#":
                    time.sleep(1)
                    el.send_keys(testStep['action'].strip().split('(')[1][1:-2])
                    # print 'send_keys:'
                    # print testStep['action'].strip().split('(')[1][1:-2]
                    # f_out.write("try:\n\ttime.sleep(1)\n\tdriver.hide_keyboard()\nexcept:\n\tprint" + '"' + "dddd" + '"' + "\n")
                    # f_out.write("time.sleep(1)\n")


                # todo driver.tap
                if "driver.tap" in testStep['handle'] and testStep['handle'][0] != "#":
                    driver.tap([(testStep['tapX'], testStep['tapY'])])

                # screenshot for the last end screen
                if indexStep == len(testCase) - 1:
                    time.sleep(2)
                    testStep['nextHtml'] = str(driver.page_source)
                    self.get_html_as_file(testStep['nextHtml'], testStep['htmlPathNext'])
                    self.get_full_screenshot_as_file(driver,testStep['screenshotPathNext'])
                    #driver.get_screenshot_as_file(testStep['screenshotPathNext'])
                    time.sleep(1)
            print('\n==========test case {} end==========='.format(testIndex))
            driver.quit()



    def get_html_as_file(self, html, path):
        if path is '':
            return
        file = open(path, 'w')
        file.write(html)
        file.close()
    def get_full_screenshot_as_file(self,driver,path):
        width = driver.execute_script("return document.documentElement.scrollWidth")
        height = driver.execute_script("return document.documentElement.scrollHeight")
        width=1200

        if 'espn' in self.url:
            width=1600
        driver.set_window_size(width, height)
        # time.sleep(1)
        driver.get_screenshot_as_file(path)
        img = Image.open(path)
        return img.width/width


