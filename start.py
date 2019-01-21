# -*- coding: utf-8 -*-
import os
from labourer.idcardAI import *
from flask import Flask, abort, request, jsonify
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)

# 测试数据暂时存放
tasks = []

@app.route('/idcard/autotask', methods=['get'])
def idcardAutoTask():
    obj = IDCardAI()
    (success, faild, real_success) =  obj.autoTask()
    response = "自动处理结果识别成功{0}个，失败{1}个，认证成功{2}个".format(len(success), len(faild), len(real_success))
    return jsonify({"msg": response,
                    "status": 0,
                    "data": {
                        "authed": real_success,
                        "finded": success,
                        "unfind": faild}})

@app.route('/idcard/auth', methods=['POST'])
def auth():
    if 'file' not in request.files:
        return jsonify({"msg": "no file", "status": -1})
    file = request.files['file']
    if file:
        filepath = os.path.join("uploads/"+file.filename)
        file.save(filepath)
        response = IDCardAI().find(filepath)
        if response:
            return jsonify(response)
        else:
            return jsonify({"msg": "auto auth fail", "status": -1})

    else:
        return jsonify({"msg": "no file", "status": -1})

if __name__ == "__main__":
    if os.path.exists("uploads") == False:
        os.makedirs("uploads")
    app.run(host="0.0.0.0", port=9993, debug=True)