import cv2
import glob
import numpy as np
from skimage.draw import line
import math
from PIL import Image
from DBHuntil import  findDBH, calculateDBH,get_depth,pixel2image
from PyQt5.QtGui import QPixmap, QImage
from inference import inference


def runDBH(src,params):
    cam_mtx = np.load('params/' + 'cam_mtx.npy')
    dist = np.load('params/' + 'dist.npy')
    ret, length, pic = measure(src,params, 27, cam_mtx, dist,1300)
    if ret:
        print("测量结果为：" + str(length))
        return length
    else:
        return 0

def measure(src,params, f,cam_mtx, dist, measurehigh=1300):
    img = cv2.imread(src)
    h, w = img.shape[:2]
    white = np.zeros((h, w, 3), np.uint8)
    white.fill(255)
    print("Start the Instance segmentation.")
    r_image_pil = inference(src,cam_mtx, dist)
    print("Success.")
    r_image = cv2.cvtColor(r_image_pil, cv2.COLOR_RGB2BGR)

    gray = cv2.cvtColor(r_image, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    #获取图像深度
    depth=get_depth(contours[0],params,h,w,1300,cam_mtx,f)
    ret2, DBHpoint, pixelhigh = findDBH(contours[0], params,cam_mtx,f,depth,
                                         measurehigh)
    if ret2:
        print("Success to find DBH.")
        cv2.line(white, DBHpoint[0], DBHpoint[1], (255, 0, 0), 15)
        DBH=calculateDBH(depth,params,cam_mtx,DBHpoint[0],DBHpoint[1],f)
        DBH = round(DBH, 1)
        return True, DBH, white
    else:
        print("Failed to find DBH.")
        return False, None, None

#length = runDBH("static/testimg/2.jpg",2.0)