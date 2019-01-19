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
    (success, faild) =  obj.autoTask()
    response = "自动处理成功{0}个，失败{1}个".format(len(success), len(faild))
    return jsonify({"msg": response,
                    "status": 0,
                    "data": {"success": success,
                            "faild": faild}})


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
    enableOpenCV(True)
    if os.path.exists("uploads") == False:
        os.makedirs("uploads")
    app.run(host="0.0.0.0", port=8383, debug=True)