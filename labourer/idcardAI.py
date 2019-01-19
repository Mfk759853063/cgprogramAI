# -*- coding: utf-8 -*-

from labourer.idcardLib.idcardocr import idcardocr
from baiduAI import BaiduAI
import cv2
import urllib.request, json
import os
import logging

def enableOpenCV(enabled):
    cv2.ocl.setUseOpenCL(enabled)

class IDCardAI:

    request_url = "http://t.hjlapp.com/cgProgramApi/labourer/getPage?platform=pc&queryCount=true"
    img_url = "http://t.hjlapp.com:9205"
    # request_url = "http://www.hjlapp.com/cgProgramApi/labourer/getPage?platform=pc&queryCount=true"
    # img_url = "http://www.hjlapp.com"
    logging.basicConfig()
    def __init__(self):
        self.page_index = 0
        self.page_size = 20
        self.total_count = 0
        self.all_data = []
        self.current_list = []
        self.faild_list = []
        self.success_list = []

    def find(self, img_name):
        idocr = idcardocr(cv2.UMat(cv2.imread(img_name)))
        return idocr

    def autoTask(self):
        self.__init__()
        self.loadMore(False)
        self.autoAuthImp()
        while len(self.all_data) < self.total_count:
            self.loadMore(True)
            self.autoAuthImp()
        logging.warning("执行完毕")
        logging.warning("{0}个识别成功{1}个识别失败".format(len(self.success_list),len(self.faild_list)))
        logging.warning(self.success_list)
        logging.warning(self.faild_list)
        return (self.success_list, self.faild_list)

    def loadMore(self, load_more):
        if load_more == False:
            self.page_index = 0
        else:
            self.page_index = self.page_index + 1
        '''params = dict(
            sss='Chicago,IL',
            ssss='Los+Angeles,CA',
            ss='Joplin,MO|Oklahoma+City,OK',
            a='false'
)       '''
        request_url = "{0}&pageIndex={1}&pageSize={2}".format(self.request_url,self.page_index,self.page_size)
        url = urllib.request.urlopen(request_url)
        try:
            response = json.loads(url.read().decode())
            if load_more:
                self.all_data.extend(response["data"]["rows"])
            else:
                self.all_data = response["data"]["rows"]
            self.current_list = response["data"]["rows"]
            self.total_count = response["data"]["totalNum"]
        except Exception as e:
            logging.warning(e)


    def autoAuthImp(self):
        for labourerDict in self.current_list:
            check_id_status = labourerDict["checkStatusIdcard"]
            hava_id_data = None
            if "idCarda" in labourerDict:
                hava_id_data = labourerDict["idCarda"]
            if hava_id_data and check_id_status == '0':
                # 待认证
                img_url = "{0}/{1}".format(self.img_url, hava_id_data)
                file_path = os.path.join(os.getcwd()+"/uploads/"+hava_id_data.split("/")[-1])
                urllib.request.urlretrieve(img_url, file_path)
                try:
                    logging.warning("准备识别{0}".format(labourerDict["name"]))
                    result = self.find(file_path)
                    if self.compare(result, labourerDict):
                        logging.warning("{0}识别成功".format(labourerDict["name"]))
                        self.success_list.append(labourerDict)
                    else:
                        if self.trybaiduAI(file_path, labourerDict):
                            logging.warning("{0}识别成功".format(labourerDict["name"]))
                            self.success_list.append(labourerDict)
                        else:
                            logging.warning("{0}识别失败".format(labourerDict["name"]))
                            self.faild_list.append(labourerDict)
                except Exception as e:
                    if self.trybaiduAI(file_path, labourerDict):
                        logging.warning("{0}识别成功".format(labourerDict["name"]))
                        self.success_list.append(labourerDict)
                    else:
                        logging.warning("{0}识别失败".format(labourerDict["name"]))
                        self.faild_list.append(labourerDict)



    def trybaiduAI(self, file_path, labourerDict):
        logging.warning("尝试使用百度AI识别")
        ai = BaiduAI()
        result = ai.find(file_path)
        result = result["words_result"]
        logging.warning(result)
        if "姓名" in result and "name" in labourerDict or "公民身份号码" in result and "idCard" in labourerDict:
            if result["姓名"]["words"] == labourerDict["name"] or result["公民身份号码"]["words"] == labourerDict["idCard"]:
                return True
        return False


    def compare(self, match_result, labourerDict):
        if "idnum" in match_result and "idCard" in labourerDict or "name" in match_result and "name" in labourerDict:
            if match_result["idnum"] == labourerDict["idCard"] or match_result["name"] == labourerDict["name"]:
                return True
        return False