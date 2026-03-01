# coding=utf-8
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
from datetime import timedelta
from flask import Flask, request,make_response
import base64
from DBH_Measure import runDBH


image_params=0.0

app = Flask(__name__)



@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'
# 设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG',])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)

# 上传图像
@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        img=base64.b64decode(request.form.get("image"))#解码
        # 定义一个图片存放的位置 存放在static下面
        with open("static/testimg/demo.jpg", "wb") as f:
            f.write(img)
        return "100" # 将结果传回给前端
#上传参数
@app.route('/uploadparams', methods=['POST', 'GET'])
def uploadparams():
    if request.method == 'POST':
        global image_params
        image_params=float(request.form.get("params"))#解码
        return "100"

#测量胸径
@app.route('/measure', methods=['GET'])
def measure():
    if request.method == 'GET':
        length = runDBH("static/testimg/demo.jpg",image_params)
        image_data = open("static/testimg/instance_out.jpg", "rb").read()
        response = make_response(image_data)
        response.headers['Content-Type'] = 'image/jpg'
        response.headers['image-focus'] = 27
        response.headers['length']=length
        return response

if __name__ == '__main__':
    app.run()
