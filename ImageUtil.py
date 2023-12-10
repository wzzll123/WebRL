# encoding=utf-8
import base64
import json
from datetime import datetime
import cv2
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import torch.backends.cudnn as cudnn
import numpy as np
import torchvision
from torchvision import datasets, models, transforms
import timm
import time
import os
import copy


# 图片处理类
class ImageUtil(object):
    API_URL = 'https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/ocr'
    timeCostForOCR = 0
    isRerun = False

    # model = timm.create_model(
    #     'lcnet_050.ra2_in1k',
    #     # 'hf_hub:timm/lcnet_075.ra2_in1k',
    #     pretrained=True,
    #     num_classes=0,  # remove classifier nn.Linear
    # )
    model = models.shufflenet_v2_x0_5(pretrained=True)
    model.eval()
    # model.fc = nn.Sequential()
    # print(torch.__config__.parallel_info())
    # torch.jit.enable_onednn_fusion(True)
    # sample_input = [torch.rand(32, 3, 224, 224)]
    # traced_model = torch.jit.trace(model, sample_input)
    # traced_model = torch.jit.freeze(traced_model)

    def __init__(self, image_content):
        # print image_path

        self.image_content = image_content
        image_content = base64.b64decode(image_content)
        nparr1 = np.fromstring(image_content, np.uint8)
        img1 = cv2.imdecode(nparr1, cv2.IMREAD_COLOR)
        self.original_image = img1

        self.original_image_width = self.original_image.shape[1]
        self.original_image_height = self.original_image.shape[2]

        self.filtered_contour_by_text = []
        self.filtered_contour = []
        self.text_block = []

    # 获取图中轮廓信息
    def get_contour_information(self):
        contour_list = []
        gray_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        canny = cv2.Canny(thresh, 5, 500)
        kernel = np.ones((3, 3), np.uint8)
        dilate = cv2.dilate(canny, kernel, iterations=2)  # 扩大轮廓范围
        method_contour = cv2.RETR_LIST
        # contours, hierarchy, _ = cv2.findContours(dilate, method_contour, cv2.CHAIN_APPROX_SIMPLE)
        contours, hierarchy = cv2.findContours(dilate, method_contour, cv2.CHAIN_APPROX_SIMPLE)
        for index in range(len(contours)):
            box = {}
            x, y, w, h = cv2.boundingRect(contours[index])
            box['x'] = x
            box['y'] = y
            box['w'] = w
            box['h'] = h
            box['type'] = 'non-text'
            contour_list.append(box)
        return contour_list

    # 过滤图中轮廓信息
    def get_filtered_contour(self):

        if self.filtered_contour != []:
            return self.filtered_contour

        _contour_list = self.get_contour_information()
        temp = [box for box in _contour_list if not (box['h'] < 15 or (box['y'] > 150 and box['w'] < 15)
                                                     or box['y'] < 50
                                                     )]

        result = self.filter_contour(temp, rate=0.6)
        self.filtered_contour = result
        return result

    # 去除被text block覆盖的元素轮廓
    # 去除位于两个text block间的轮廓
    def get_filtered_contour_by_text(self):

        if self.filtered_contour_by_text != []:
            return self.filtered_contour_by_text

        _contour_list = self.get_filtered_contour()
        _text_block = self.get_text_block()
        contour_list = []
        for contour in _contour_list:
            label = False  # 用于标记该contour是否冲突
            for word1 in _text_block:
                if self.contour_is_covered(contour, word1, rate=0.6) and contour['h'] < 150:
                    label = True
            if not label:
                contour_list.append(contour)

        self.filtered_contour_by_text = contour_list
        return contour_list

    def get_text_information(self):
        # json_path = Config.IMAGE_PARSE_JSON_PATH + Config.APP_NAME + '/' + self.img_name + '_json.txt'
        # print(self.image_path.replace('.png.jpg','.txt'))
        # resp = requests.post("http://weet.oa.com/devreport/external/ocr", data=self.image_content)
        # return resp.json()['data']['detections']

        try:
            # cred = credential.Credential("AKID2oKb0BBjuqVt5vBXR6TZNt90e18znrsd", "kFSR9akdFchV4LM6ZlhNmxqSnreDVWXR")
            cred = credential.Credential("AKID73j8G8k59xUkkTw83h5C1ZqqZ0B4h38w", "YpoXz92j9I9j36sNddNp1waw1qNdcLnx")
            httpProfile = HttpProfile()
            httpProfile.endpoint = "ocr.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = ocr_client.OcrClient(cred, "ap-shanghai", clientProfile)

            req = tencentcloud.ocr.v20181119.models.GeneralBasicOCRRequest()
            params = {
                "ImageBase64": self.image_content
            }
            params = json.dumps(params, cls=MyEncoder)
            req.from_json_string(params)

            resp = client.GeneralBasicOCR(req)
            return resp.TextDetections


        except TencentCloudSDKException as err:
            Logger.mainLogger.info(err)

    def divideLineWord(self, lineList, divideParameter=32):
        returnList = []
        indexList = []
        for index, word in enumerate(lineList['words']):
            if index == 0:
                continue
            word_countour_size1 = lineList['words'][index - 1]['boundingBox'].split(',')
            word_countour_size2 = word['boundingBox'].split(',')

            if int(word_countour_size2[0]) - int(word_countour_size1[0]) - int(
                    word_countour_size1[2]) > divideParameter:
                indexList.append(index)
        for index, indexValue in enumerate(indexList):
            if len(returnList) == 0:
                returnList.append(lineList['words'][0:indexValue])
            else:
                returnList.append(lineList['words'][indexList[index - 1]:indexValue])
            if index == len(indexList) - 1:
                returnList.append(lineList['words'][indexValue:])
        if len(indexList) == 0:
            returnList.append(lineList['words'][0:])
        return returnList

    @staticmethod
    def getTextBlockByTecentAPI(baseImage):
        imageUtil = ImageUtil(baseImage)
        _json = imageUtil.get_text_information()
        all_text_block = []
        for wordItem in _json:
            if wordItem.Confidence < 80 or wordItem.ItemPolygon.Y < 50:
                continue

            text_block = {
                'x': wordItem.ItemPolygon.X,
                'y': wordItem.ItemPolygon.Y,
                'w': wordItem.ItemPolygon.Width,
                'h': wordItem.ItemPolygon.Height,
                'text': wordItem.DetectedText,
                'type': 'text'
            }
            all_text_block.append(text_block)
        return all_text_block

    # 获取位于同一行的文字
    # 返回结果为一行中水平距离足够接近的文本信息
    def get_text_block(self):

        if self.text_block != []:
            return self.text_block

        timeBefore = datetime.now()

        _json = self.get_text_information()

        all_text_block = []
        if _json is None or _json == []:
            return all_text_block

        for wordItem in _json:
            if wordItem.Confidence < 80 or wordItem.ItemPolygon.Y < 50:
                continue

            text_block = {
                'x': wordItem.ItemPolygon.X,
                'y': wordItem.ItemPolygon.Y,
                'w': wordItem.ItemPolygon.Width,
                'h': wordItem.ItemPolygon.Height,
                'text': wordItem.DetectedText,
                'type': 'text'
            }
            all_text_block.append(text_block)
        self.text_block = all_text_block
        return all_text_block

    # return time cost with the level of minutes
    def getOCRTimeCost(self):
        return ImageUtil.timeCostForOCR / 60.0

    # 消除存在于两个text block中的轮廓
    # 对于位于两个text block中的轮廓将其合并进text block并扩大text block的范围
    def delete_contour_between_text_block(self):
        _contour_list = self.get_filtered_contour_by_text()
        _text_block = self.get_text_block()
        _text_block = sorted(_text_block, key=lambda _text_block: _text_block['y'])
        new_contour_list, new_text_block = [], []
        for contour in _contour_list:
            label = True
            for index1, text_block1 in enumerate(_text_block):
                if index1 == len(_text_block) - 1:
                    if text_block1 not in new_text_block:
                        new_text_block.append(text_block1)
                    continue
                text_block2 = _text_block[index1 + 1]
                if text_block1['x'] <= contour['x'] <= text_block1['x'] + text_block1['w'] \
                        and text_block2['x'] <= contour['x'] <= text_block2['x'] + text_block2['w'] \
                        and text_block1['y'] <= contour['y'] <= text_block2['y']:
                    label = False
                    text_block1['h'] = contour['y'] + contour['h'] - text_block1['y'] + 10
                if text_block1 not in new_text_block:
                    new_text_block.append(text_block1)
            if label:
                new_contour_list.append(contour)
        return new_contour_list, new_text_block

    # 将垂直距离足够接近的轮廓合并
    def merge_text_block_vertical(self):
        contour_list, text_block = self.delete_contour_between_text_block()
        new_text_block = []
        labels = [False] * len(text_block)  # 用于标记该text block是否已经被合并
        for index1, text_block1 in enumerate(text_block):
            if labels[index1]:
                continue
            temp_text_block = {
                'x': text_block1['x'],
                'y': text_block1['y'],
                'w': text_block1['w'],
                'h': text_block1['h'],
                'container': [text_block1],
                'type': 'text'
            }
            labels[index1] = True
            original_y = text_block1['y']
            for index2, text_block2 in enumerate(text_block):
                if labels[index2]:
                    continue
                # 两个轮廓的垂直距离小于一个阀值且位于同一水平线上
                if abs(text_block2['y'] - (temp_text_block['y'] + temp_text_block['h'])) < 30 \
                        and abs(text_block2['x'] - temp_text_block['x']) <= 5:
                    temp_text_block['h'] = text_block2['y'] + text_block2['h'] - original_y
                    temp_text_block['w'] = max(temp_text_block['w'], text_block2['w'])
                    temp_text_block['container'].append(text_block2)
                    labels[index2] = True
            new_text_block.append(temp_text_block)
        return contour_list, self.filter_contour(new_text_block)

    # 将位于同一水平线上的轮廓合并进一个list
    # todo：如何控制距离阀值，将不应该出现的轮廓剔除
    def merge_contour_horizontal(self):
        _contour_list, _text_block = self.merge_text_block_vertical()
        contours = _contour_list + _text_block
        labels = [False] * len(contours)
        contour_list = []
        # print(self.original_image_width)
        for index1, contour1 in enumerate(contours):
            temp = []
            if labels[index1]:
                continue
            labels[index1] = True
            temp.append(contour1)
            for index2, contour2 in enumerate(contours):
                if not labels[index2] and abs(contour2['y'] - contour1['y']) < 30:
                    if (contour2['x'] < contour1['x']
                        and abs(contour1['x'] - (contour2['x'] + contour2['w'])) < self.original_image_width / 2) \
                            or (contour1['x'] <= contour2['x']
                                and abs(
                                contour2['x'] - (contour1['x'] + contour1['w'])) < self.original_image_width / 2):
                        temp.append(contour2)
                        labels[index2] = True
            if len(temp) != 0:
                contour_list.append(temp)
        return contour_list

    # 根据排序后的轮廓列表得到列表项
    def get_list_item(self):
        result = []
        _contour_list = self.merge_contour_horizontal()
        # print(_contour_list)
        for temp_list in _contour_list:
            if len(temp_list) < 0:
                continue
            # 因为是排过序的list，list中的一项即为y坐标接近的多个轮廓
            temp = {
                'x': 0,
                'y': 0,
                'w': 0,
                'h': 0,
                'container': temp_list
            }
            min_x, min_y = temp_list[0]['x'], temp_list[0]['y']
            min_w, min_h = 0, 0
            for contour in temp_list:
                if contour['x'] < min_x:
                    min_x = contour['x']
                    min_w = max(min_w, (contour['x'] + contour['w'] - min_x))
                else:
                    min_w = max(min_w, (contour['x'] + contour['w'] - min_x))
                if contour['y'] < min_y:
                    min_y = contour['y']
                    min_h = max(min_h, (contour['y'] + contour['h'] - min_y))
                else:
                    min_h = max(min_h, (contour['y'] + contour['h'] - min_y))
            temp['x'] = min_x - 5
            temp['y'] = min_y - 5
            temp['w'] = min_w + 10
            temp['h'] = min_h + 10
            if temp not in result:
                result.append(temp)
        # 过滤那些只含非文本元素的item
        final_result = []
        for temp in result:
            for son in temp['container']:
                if son['type'] != 'non-text' and temp not in final_result:
                    final_result.append(temp)
        # print(final_result)
        return final_result

    # 定义列表
    def identify_list_view(self):
        list_item = self.get_list_item()
        # print(list_item)
        item_labels = [-1] * len(list_item)  # 用于标记结构相同的列表项
        for index1, contour1 in enumerate(list_item):
            if item_labels[index1] != -1:
                continue
            item_labels[index1] = index1
            for index2, contour2 in enumerate(list_item):
                if item_labels[index2] != -1:
                    continue
                if self.contour_structure_identical(contour1, contour2):
                    item_labels[index2] = index1
        # print(item_labels)
        for item in set(item_labels):
            if item_labels.count(item) >= len(list_item) / 2:
                list_item_result = [list_item[index] for index in range(len(item_labels)) if item_labels[index] == item]
                print(list_item_result)
                # self.draw_picture(list_item_result, self.original_image)
                return True, list_item_result
        return False, None

    # 判断两个item的结构是否相等
    # 处理到text block层次
    def contour_structure_identical(self, contour1, contour2):
        # step1: 如果有type，则看type是否相等
        if (('type' in contour1.keys()) and ('type' in contour2.keys()) and (contour1['type'] == contour2['type'])) or \
                (('type' not in contour1.keys()) and ('type' not in contour2.keys())):
            # step2: 再看两个contour是否含有container，如果含有再看container的长度是否相等
            if (('container' not in contour1.keys()) and ('container' not in contour2.keys())) or (
                    'container' in contour1.keys()) and ('container' in contour2.keys()) and \
                    len(contour1['container']) == len(contour2['container']):
                # step3: 递归看container的内容的结构是否相等
                if ('container' not in contour1.keys()) and ('container' not in contour2.keys()):
                    return True
                for index1, child1 in enumerate(contour1['container']):
                    if not self.contour_structure_identical(child1, contour2['container'][index1]):
                        return False
            else:
                return False
        else:
            return False
        return True

    # 去除重叠的轮廓
    def filter_contour(self, contour_list, rate=0.8):
        result = []
        for contour1 in contour_list:
            if contour1['y'] > 1800:
                continue
            fail = 1
            for contour2 in contour_list:
                if self.contour_is_covered(contour1, contour2, rate) \
                        and contour1['h'] * contour1['w'] < contour2['h'] * contour2['w'] and contour2[
                    'w'] < 0.3 * self.original_image_width:
                    fail = 0
            if fail == 1:
                result.append(contour1)
        return result

    def getList(self):
        return self.get_text_block(), self.get_filtered_contour()

    def rectanCover(self, box1, box2, rate=0.8):
        x = max(box1['x'], box2['x'])
        x_ = min(box1['x'] + box1['w'], box2['x'] + box2['w'])
        y = max(box1['y'], box2['y'])
        y_ = min(box1['y'] + box1['h'], box2['y'] + box2['h'])
        area = min(box1['w'] * box1['h'], box2['w'] * box2['h'])
        if x_ > x and y_ > y and (x_ - x) * (y_ - y) > rate * area:
            return True
        return False

    # 判断两个轮廓是否有重叠
    @staticmethod
    def contour_is_covered(contour1, contour2, rate=0.8):
        x = max(contour1['x'], contour2['x'])
        x_ = min(contour1['x'] + contour1['w'], contour2['x'] + contour2['w'])
        y = max(contour1['y'], contour2['y'])
        y_ = min(contour1['y'] + contour1['h'], contour2['y'] + contour2['h'])
        area = min(contour1['w'] * contour1['h'], contour2['w'] * contour2['h'])
        if x_ > x and y_ > y and (x_ - x) * (y_ - y) > rate * area:
            return True
        return False

    @staticmethod
    def filter_matches(kp1, kp2, matches, ratio=0.75):
        mkp1, mkp2 = [], []
        for m in matches:
            if len(m) == 2 and m[0].distance < m[1].distance * ratio:
                m = m[0]
                mkp1.append(kp1[m.queryIdx])
                mkp2.append(kp2[m.trainIdx])
        p1 = np.float32([kp.pt for kp in mkp1])
        p2 = np.float32([kp.pt for kp in mkp2])
        kp_pairs = list(zip(mkp1, mkp2))
        return p1, p2, kp_pairs

    @staticmethod
    def explore_match(win, img1, img2, kp_pairs, initbox, status=None, H=None):
        similarPoints = []
        h1, w1 = img1.shape[:2]
        h2, w2 = img2.shape[:2]
        vis = np.zeros((max(h1, h2), w1 + w2), np.uint8)
        vis[:h1, :w1] = img1
        vis[:h2, w1:w1 + w2] = img2
        vis = cv2.cvtColor(vis, cv2.COLOR_GRAY2BGR)

        if H is not None:
            corners = np.float32([[0, 0], [w1, 0], [w1, h1], [0, h1]])
            corners = np.int32(cv2.perspectiveTransform(corners.reshape(1, -1, 2), H).reshape(-1, 2) + (w1, 0))
            cv2.polylines(vis, [corners], True, (255, 255, 255))

        if status is None:
            status = np.ones(len(kp_pairs), np.bool)

        p1 = np.int32([kpp[0].pt for kpp in kp_pairs])
        p2 = np.int32([kpp[1].pt for kpp in kp_pairs]) + (w1, 0)

        green = (0, 255, 0)
        red = (0, 0, 255)
        white = (255, 255, 255)
        kp_color = (51, 103, 236)
        for (x1, y1), (x2, y2), inlier in zip(p1, p2, status):
            if y1 > initbox['y'] and y1 < initbox['y'] + initbox['h'] and x1 > initbox['x'] and x1 < initbox['x'] + \
                    initbox[
                        'w'] and (y2 > 50 or h1 < w1):

                if inlier:
                    similarPoints.append((x2 - w1, y2))
                    col = green
                    cv2.circle(vis, (x1, y1), 2, col, -1)
                    cv2.circle(vis, (x2, y2), 2, col, -1)
                else:
                    col = red
                    r = 2
                    thickness = 3
                    cv2.line(vis, (x1 - r, y1 - r), (x1 + r, y1 + r), col, thickness)
                    cv2.line(vis, (x1 - r, y1 + r), (x1 + r, y1 - r), col, thickness)
                    cv2.line(vis, (x2 - r, y2 - r), (x2 + r, y2 + r), col, thickness)
                    cv2.line(vis, (x2 - r, y2 + r), (x2 + r, y2 - r), col, thickness)
        vis0 = vis.copy()
        for (x1, y1), (x2, y2), inlier in zip(p1, p2, status):
            if y1 > initbox['y'] and y1 < initbox['y'] + initbox['h'] and x1 > initbox['x'] and x1 < initbox['x'] + \
                    initbox[
                        'w'] and inlier and (y2 > 50 or h1 < w1):
                cv2.line(vis, (x1, y1), (x2, y2), green)

        outputPath = 'E:/wechatTest/wechatTestAndroid/old version/project-samples/uicase/meter/output/'
        cv2.imwrite("12.png", vis)
        return similarPoints

    @staticmethod
    def getSift(image1, image2, initBox, sift_ratio):
        img1 = cv2.imread(image1)
        img2 = cv2.imread(image2)

        img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        sift = cv2.AKAZE_create()

        kp1, des1 = sift.detectAndCompute(img1_gray, None)

        kp2, des2 = sift.detectAndCompute(img2_gray, None)
        if des2 is None:
            # print "image simple with none"
            return []
        # BFmatcher with default parms
        bf = cv2.BFMatcher(cv2.NORM_HAMMING)
        matches = bf.knnMatch(des1, des2, k=2)
        # TODO 0.5,0.6,0.7,0.8,0.9
        p1, p2, kp_pairs = ImageUtil.filter_matches(kp1, kp2, matches, sift_ratio)

        if len(kp_pairs) == 0:
            # print("no same element")
            return []

        similar = ImageUtil.explore_match('matches', img1_gray, img2_gray, kp_pairs, initBox)
        # img3 = cv2.drawMatchesKnn(img1_gray,kp1,img2_gray,kp2,good[:10],flag=2)

        return similar

    @staticmethod
    def getSurf(imagePath1, imagePath2, widgetLocation):
        img1 = cv2.imread(imagePath1, cv2.IMREAD_GRAYSCALE)  # queryImage
        img2 = cv2.imread(imagePath2, cv2.IMREAD_GRAYSCALE)  # trainImage
        surf = cv2.xfeatures2d.SURF_create(400)
        # find the keypoints and descriptors with ORB
        kp1, des1 = surf.detectAndCompute(img1, None)
        kp_image1 = cv2.drawKeypoints(img1, kp1, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        cv2.imwrite("1.png", kp_image1)
        kp2, des2 = surf.detectAndCompute(img2, None)
        # create BFMatcher object
        bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
        # Match descriptors.
        matches = bf.match(des1, des2)
        points = ImageUtil.filterMatchByLocation(matches, kp1, kp2, widgetLocation)
        return points

    @staticmethod
    def isPointInBox(x, y, widgetLocation):
        if (y > widgetLocation['y'] and y < widgetLocation['y'] + widgetLocation['h'] and x > widgetLocation[
            'x'] and x < widgetLocation['x'] + widgetLocation['w']):
            return True
        else:
            return False

    @staticmethod
    def filterMatchByLocation(matches, kp1, kp2, widgetLocation):
        points = []
        for match in matches:
            x = kp1[match.queryIdx].pt[0]
            y = kp1[match.queryIdx].pt[1]
            if (y > widgetLocation['y'] and y < widgetLocation['y'] + widgetLocation['h'] and x > widgetLocation[
                'x'] and x < widgetLocation['x'] + widgetLocation['w']):
                points.append(kp2[match.queryIdx].pt)
        return points

    @staticmethod
    def getSiftBase64(image1, image2, initBox, sift_ratio):
        nparr1 = np.fromstring(image1, np.uint8)
        img1 = cv2.imdecode(nparr1, cv2.IMREAD_COLOR)

        nparr2 = np.fromstring(image2, np.uint8)
        img2 = cv2.imdecode(nparr2, cv2.IMREAD_COLOR)

        img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        sift = cv2.AKAZE_create()

        kp1, des1 = sift.detectAndCompute(img1_gray, None)
        kp_image1 = cv2.drawKeypoints(img1_gray, kp1, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        cv2.imwrite("1.png", kp_image1)
        kp2, des2 = sift.detectAndCompute(img2_gray, None)
        kp_image2 = cv2.drawKeypoints(img2_gray, kp2, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        cv2.imwrite("2.png", kp_image2)
        if des2 is None:
            # print "image simple with none"
            return []
        # BFmatcher with default parms
        bf = cv2.BFMatcher(cv2.NORM_L1)
        matches = bf.knnMatch(des1, des2, k=2)
        good = []
        for m, n in matches:
            if m.distance < 0.95 * n.distance:
                good.append([m])
        # cv.drawMatchesKnn expects list of lists as matches.
        # TODO 0.5,0.6,0.7,0.8,0.9
        p1, p2, kp_pairs = ImageUtil.filter_matches(kp1, kp2, matches, sift_ratio)

        if len(kp_pairs) == 0:
            # print("no same element")
            return []

        similar = ImageUtil.explore_match('matches', img1_gray, img2_gray, kp_pairs, initBox)
        # img3 = cv2.drawMatchesKnn(img1_gray,kp1,img2_gray,kp2,good[:10],flag=2)

        return similar

    @staticmethod
    def getSimilarLeafNodeByCNNSelenium(widgetLocation, oldVersionImgPath, newVerSionImgPath, rootNode):
        oldImg = ImageUtil.openCropImg(oldVersionImgPath, widgetLocation)
        isLong = False
        if (widgetLocation['w'] / widgetLocation['h'] > 4 or widgetLocation['h'] / widgetLocation['w'] > 4):
            isLong = True
        oldImgFeature = ImageUtil.imgToFeatureTensor(oldImg, isLong)
        rankedAllLeafNode = []
        ImageUtil.dfsSeleniumNode(rootNode, newVerSionImgPath, isLong, rankedAllLeafNode, oldImgFeature, widgetLocation)
        sorted(rankedAllLeafNode, key=lambda t: t[1], reverse=True)
        return rankedAllLeafNode

    @staticmethod
    def dfsSeleniumNode(root, newVerSionImgPath, isLong, rankedAllLeafNode, oldImgFeature, widgetLocation):
        # from collections import namedtuple
        # soupLike = namedtuple('soupLike', ['attrs'])
        for el in root.find_elements_by_xpath('./child::*'):
            location = el.location
            size = el.size

            # if (size['width'] == 0 or size['height'] == 0):
            #     return
            # leafNode = soupLike(attrs={})
            leafNode = {}
            leafNode['x'] = location['x']
            leafNode['y'] = location['y']
            leafNode['w'] = size['width']
            leafNode['h'] = size['height']
            if ((size['width'] != 0 and size['height'] != 0) and
                    (abs(leafNode['h'] - widgetLocation['h']) < 60 or abs(
                        leafNode['w'] - widgetLocation['w']) < 60)):
                newImg = ImageUtil.openCropImg(newVerSionImgPath, leafNode)
                newImgFeature = ImageUtil.imgToFeatureTensor(newImg, isLong)
                similarity = torch.cosine_similarity(oldImgFeature, newImgFeature)
                if (similarity[0] > 0.5):
                    rankedAllLeafNode.append((el, similarity[0]))
            ImageUtil.dfsSeleniumNode(el, newVerSionImgPath, isLong, rankedAllLeafNode, oldImgFeature, widgetLocation)

    @staticmethod
    def getSimilarLeafNodeByCNN(widgetLocation, oldVersionImgPath, newVerSionImgPath, allLeafNode, theta):
        rankedAllLeafNode = []
        oldImg = ImageUtil.openCropImg(oldVersionImgPath, widgetLocation)
        # oldImg.save("old.png")
        isLong = False
        if (widgetLocation['w'] / widgetLocation['h'] > 4 or widgetLocation['h'] / widgetLocation['w'] > 4):
            isLong = True

        oldImgFeature = ImageUtil.imgToFeatureTensor(oldImg, isLong)
        from PIL import Image
        newAllImg = Image.open(newVerSionImgPath)

        for leafNode in allLeafNode:
            # abs(leafNode.attrs['h']-widgetLocation['h'])<100 or abs(leafNode.attrs['w']-widgetLocation['w'])<100 or
            # if(abs(leafNode.attrs['h']-widgetLocation['h'])<100 or abs(leafNode.attrs['w']-widgetLocation['w'])<100 or 0.7*widgetLocation['h']
            # <leafNode.attrs['h']<1.3*widgetLocation['h'] or 0.7*widgetLocation['w']<leafNode.attrs['w']<1.3*widgetLocation['w']):
            # newImg = ImageUtil.openCropImg(newVerSionImgPath, leafNode)
            edge = 0
            newImg = newAllImg.crop((leafNode['x'] - edge, leafNode['y'] - edge,
                                     leafNode['x'] + leafNode['w'] + 2 * edge
                                     , leafNode['y'] + leafNode['h'] + 2 * edge))
            newImg = newImg.convert('RGB')
            newImgFeature = ImageUtil.imgToFeatureTensor(newImg, isLong)
            similarity = torch.cosine_similarity(oldImgFeature, newImgFeature)
            if (similarity[0] > theta):
                rankedAllLeafNode.append((leafNode, similarity[0]))
            # else:
            #     continue
        sorted(rankedAllLeafNode, key=lambda t: t[1], reverse=True)
        return rankedAllLeafNode

    @staticmethod
    def openCropImg(imgPath, widgetLocation):
        from PIL import Image
        img = Image.open(imgPath)
        edge = 0
        img = img.crop((widgetLocation['x'] - edge, widgetLocation['y'] - edge,
                        widgetLocation['x'] + widgetLocation['w'] + 2 * edge
                        , widgetLocation['y'] + widgetLocation['h'] + 2 * edge))
        img = img.convert('RGB')
        return img

    @staticmethod
    def imgToFeatureTensor(img, isLong):
        return ImageUtil.imgToFeatureTensorTrim(img)
        # if(isLong):
        #     return ImageUtil.imgToFeatureTensorLong(img)
        # else:
        #     return ImageUtil.imgToFeatureTensorNotLong(img)

    @staticmethod
    def imgToFeatureTensorTrim(img):
        dataTransfroms = transforms.Compose([
            # transforms.Resize(256, interpolation=transforms.InterpolationMode.BILINEAR),
            transforms.Resize(256),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        imgTensor = dataTransfroms(img)
        imgFeature = ImageUtil.getConvOutput(imgTensor.unsqueeze(0))
        return imgFeature

    @staticmethod
    def imgToFeatureTensorNotLong(img):
        dataTransfroms = transforms.Compose([
            # transforms.Resize([32, 32]),
            #
            transforms.Resize(256),
            # transforms.CenterCrop(250),
            # transforms.Grayscale(3),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        imgTensor = dataTransfroms(img)
        imgFeature = ImageUtil.getConvOutput(imgTensor.unsqueeze(0))
        return imgFeature

    @staticmethod
    def imgToFeatureTensorLong(img):
        dataTransfroms = transforms.Compose([
            # transforms.Resize([32, 32]),
            transforms.Resize(256),
            # transforms.Grayscale(3),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        imgTensor = dataTransfroms(img)
        imgFeature = ImageUtil.getConvOutput(imgTensor.unsqueeze(0))
        return imgFeature

    @staticmethod
    def getSimilarityByCNN(oldVersionImgPath, newVerSionImgPath, widgetLocation, leafNode):
        similarity = 0
        oldImg = ImageUtil.openCropImg(oldVersionImgPath, widgetLocation)
        newImg = ImageUtil.openCropImg(newVerSionImgPath, leafNode)
        oldImgFeature = ImageUtil.imgToFeatureTensor(oldImg)
        newImgFeature = ImageUtil.imgToFeatureTensor(newImg)
        return torch.cosine_similarity(oldImgFeature, newImgFeature)

    @staticmethod
    def getConvOutput(imgTensor):
        # model = models.squeezenet1_1(pretrained=True)
        # model.eval()
        # model.fc = nn.Sequential()
        # model = models.mobilenet_v3_large(pretrained=True)
        # model.eval()
        # model.fc=nn.Sequential()
        # model = models.shufflenet_v2_x1_0(pretrained=True)
        # model.eval()
        # model.fc=nn.Sequential()



        with torch.no_grad():
            imgTensor = ImageUtil.model(imgTensor)
        return imgTensor

    @staticmethod
    def rankLeafNodeBySift(widgetLocation, oldVersionImg, newVerSionImg, allLeafNode):
        oldVersionImg = base64.b64decode(oldVersionImg)
        newVerSionImg = base64.b64decode(newVerSionImg)
        similarPoints = ImageUtil.getSiftBase64(oldVersionImg, newVerSionImg, widgetLocation, sift_ratio=0.8)
        rankedAllLeafNode = []
        for leafNode in allLeafNode:
            # leafNodeEntry:(leafNode,siftSum)
            sum = 0
            for (x, y) in similarPoints:
                if (y > leafNode.attrs['y'] and y < leafNode.attrs['y'] + leafNode.attrs['h'] and x > leafNode.attrs[
                    'x'] and x < leafNode.attrs[
                    'x'] + leafNode.attrs['w']):
                    sum = sum + 1
            if (sum > 0):
                rankedAllLeafNode.append((leafNode, sum * 1.0 / leafNode.attrs['h'] / leafNode.attrs['w']))
        sorted(rankedAllLeafNode, key=lambda t: t[1], reverse=True)
        return rankedAllLeafNode

    @staticmethod
    def rankNoneTextCandidateByCVTextMatchBySift(similarPoints, candidates):

        rankedCandidate = []
        candidateRankDic = {}

        for candidate in candidates:
            sum = 0
            for (x, y) in similarPoints:
                if y > candidate['y'] and y < candidate['y'] + candidate['h'] and x > candidate['x'] and x < candidate[
                    'x'] + candidate['w']:
                    sum = sum + 1
            candidateRankDic[str(candidate)] = sum * 1.0 / candidate['h'] / candidate['w']

            if candidateRankDic[str(candidate)] > 0:
                if rankedCandidate == []:
                    rankedCandidate.append(candidate)
                else:
                    for index, item in enumerate(rankedCandidate):
                        if candidateRankDic[str(candidate)] > candidateRankDic[str(item)]:
                            rankedCandidate.insert(index, candidate)
                            break

                        if index == len(rankedCandidate) - 1:
                            rankedCandidate.append(candidate)
                            break

        if len(rankedCandidate) == 0:
            return [{'x': point[0], 'y': point[1], 'w': 1, 'h': 1} for point in similarPoints]
        return rankedCandidate

    @staticmethod
    def isCVTextMatch(initBox, oldVersionImg, newVerSionImg):
        candidates = []

        if 'x' not in initBox:
            return [], '', False

        oldImage = ImageUtil(oldVersionImg)
        oldText = oldImage.get_text_block()
        # oldNoneText = oldImage.get_filtered_contour_by_text()

        newImage = ImageUtil(newVerSionImg)
        newText = newImage.get_text_block()
        newNoneText = newImage.get_filtered_contour_by_text()

        contourList = list(newText) + list(newNoneText)

        oldVersionImg = base64.b64decode(oldVersionImg)
        newVerSionImg = base64.b64decode(newVerSionImg)

        similar = ImageUtil.getSiftBase64(oldVersionImg, newVerSionImg, initBox, sift_ratio=0.8)

        Logger.mainLogger.info('oldText num: ' + str(len(newText)))
        for newItem in newText:
            Logger.mainLogger.info(str(newItem))

        initIsText = False
        matchedPairText = {}
        for oldTextItem in oldText:
            if ImageUtil.contour_is_covered(initBox, oldTextItem, 0.3):
                initIsText = True
                initText = dict(oldTextItem)
                Logger.mainLogger.info('initText: ' + str(initText))

            for newTextItem in newText:
                if oldTextItem['text'] == newTextItem['text']:
                    if str(oldTextItem) not in matchedPairText:
                        matchedPairText[str(oldTextItem)] = []
                    matchedPairText[str(oldTextItem)].append(newTextItem)
                    newText.remove(newTextItem)

        isMapped = False
        Logger.mainLogger.info('oldText num: ' + str(len(oldText)) + ', contour num: ' + str(len(contourList)))

        if len(oldText) == 0:
            isMapped = False
        elif len(matchedPairText) * 1.0 / len(oldText) >= 0.3:
            isMapped = True
        elif len(contourList) == 0 or len(similar) * 1.0 / len(contourList) >= 0.1:
            isMapped = True

        # todo bug????
        if initIsText:
            for matchedOld in matchedPairText:
                if initText['text'] == matchedPairText[matchedOld][0]['text']:
                    candidates = matchedPairText[matchedOld]
                    Logger.mainLogger.info('allSameText: ' + initText['text'])

            if len(candidates) == 0:
                for newTextItem in newText:
                    isTextSimilar = initText['text'].encode('utf8') in newTextItem['text'].encode('utf8') or \
                                    newTextItem['text'].encode('utf8') in initText['text'].encode(
                        'utf8') or ImageUtil.isTwoTextSimilar(initText['text'], newTextItem['text'])
                    if isTextSimilar:
                        candidates.append(newTextItem)
                        Logger.mainLogger.info('partialSameText: ' + newTextItem['text'])

        if len(candidates) == 0:
            candidates = ImageUtil.rankNoneTextCandidateByCVTextMatchBySift(similar, contourList)

        if candidates == []: return [], '', isMapped
        matchedType = 'isSureMatch' if len(candidates) == 1 else 'isPossibleMatch'
        return candidates, matchedType, isMapped

    @staticmethod
    def isTwoTextSimilar(text1, text2):
        '''
        if isinstance(text1, str):
            text1 = unicode(text1, 'utf-8')
        if isinstance(text2, str):
            text2 = unicode(text2, 'utf-8')
        '''

        for word1 in text1:
            if word1 in text2 and word1 != u' ':
                return True
        return False


if __name__ == '__main__':
    # Image.getSift('','')
    # ImageUtil.ocrParser()
    ##exit()
    # ImageUtil.getSift("/Users/xutongtong/Documents/GitHub/MMWebTest/meter/2.png",
    #             "/Users/xutongtong/Documents/GitHub/MMWebTest/meter/2.png", {'x': 0, 'y': 0, 'w': 100, 'h': 200}, 0.8)
    print(ImageUtil.isTwoTextSimilar(u'', u'fsfdfsdfsd'))
