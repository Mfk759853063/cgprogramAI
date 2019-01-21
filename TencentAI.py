# -*- coding: utf-8 -*-


import hashlib
import time
import random
import string
import requests
import base64
import requests
from urllib.parse import urlencode
import json

app_id = '2111605672'
app_key = 'VGawS1g7qwnYYUNK'

class TencentAI:
    def get_params(self, img):  # 鉴权计算并返回请求参数
        # 请求时间戳（秒级），用于防止请求重放（保证签名5分钟有效
        time_stamp = str(int(time.time()))
        # 请求随机字符串，用于保证签名不可预测,16代表16位
        nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 16))

        params = {'app_id': app_id,  # 请求包，需要根据不同的任务修改，基本相同
                  'image': img,  # 文字类的任务可能是‘text’，由主函数传递进来
                  'card_type': 0,  # 身份证件类可能是'card_type'
                  'time_stamp': time_stamp,  # 时间戳，都一样
                  'nonce_str': nonce_str,  # 随机字符串，都一样
                  # 'sign':''                      #签名不参与鉴权计算，只是列出来示意
                  }

        sort_dict = sorted(params.items(), key=lambda item: item[0], reverse=False)  # 字典排序
        sort_dict.append(('app_key', app_key))  # 尾部添加appkey
        rawtext = urlencode(sort_dict).encode()  # urlencod编码
        sha = hashlib.md5()
        sha.update(rawtext)
        md5text = sha.hexdigest().upper()  # MD5加密计算
        params['sign'] = md5text  # 将签名赋值到sign
        return params  # 返回请求包

    def find(self, image_path):
        url = "https://api.ai.qq.com/fcgi-bin/ocr/ocr_idcardocr"
        with open(image_path, 'rb') as bin_data:
            image_data = bin_data.read()
        image_data = base64.b64encode(image_data)
        params = self.get_params(image_data)
        return requests.post(url, params).json()