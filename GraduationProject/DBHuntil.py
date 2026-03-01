import cv2
import glob
import numpy as np
from skimage.draw import line
import math
from PIL import Image
import matplotlib.pyplot as plt

#求解直线与轮廓的交点
def intersect(cnt, p1, p2):
    pp = []
    x, y, w, h = cv2.boundingRect(cnt)

    if p2[0] != p1[0]:  # 若存在斜率 y=kx+b
        k = (p2[1] - p1[1]) / (p2[0] - p1[0])
        b = p1[1] - p1[0] * k
        # 求解直线和boundingbox的交点A和B
        pa, pb = (x, int(k * x + b)), ((x + w), int(k * (x + w) + b))
    else:  # 若斜率不存在，垂直的直线
        pa, pb = (p1[0], y), (p1[0], y + h)

    for pt in zip(*line(*pa, *pb)):
        ptdown = (pt[0], pt[1] + 1)
        if (cv2.pointPolygonTest(cnt, pt, False) == 0 or cv2.pointPolygonTest(
                cnt, ptdown, False) == 0):  # 若点在轮廓上(或者下一个点在轮廓上)
            pp.append(pt)

    return pp


#基于椭圆拟合的树干外接矩形提取算法
def findRec(contours):
    def cart2pol(x, y):  #笛卡尔坐标系->极坐标系
        theta = np.arctan2(y, x)
        rho = np.hypot(x, y)
        return theta, rho

    def pol2cart(theta, rho):  #极坐标系->笛卡尔坐标系
        x = rho * np.cos(theta)
        y = rho * np.sin(theta)
        return x, y

    def rotate_contour(cnt, rotatepoint, angle):  #轮廓旋转函数
        cx = rotatepoint[0]
        cy = rotatepoint[1]
        cnt_norm = cnt - [cx, cy]  #将轮廓移动到旋转点

        coordinates = cnt_norm[:, 0, :]
        xs, ys = coordinates[:, 0], coordinates[:, 1]
        thetas, rhos = cart2pol(xs, ys)

        thetas = np.rad2deg(thetas)
        thetas = (thetas + angle) % 360
        thetas = np.deg2rad(thetas)

        xs, ys = pol2cart(thetas, rhos)

        cnt_norm[:, 0, 0] = xs
        cnt_norm[:, 0, 1] = ys

        cnt_rotated = cnt_norm + [cx, cy]
        cnt_rotated = cnt_rotated.astype(np.int32)

        return cnt_rotated

    ellip = cv2.fitEllipse(contours)  #椭圆拟合减少噪声的影响
    #ellip = cv2.fitEllipseDirect(contours)
    rotatepoint = ellip[0]
    rotateangel = 180 - ellip[2]
    rota = rotate_contour(contours, rotatepoint, rotateangel)
    x, y, w, h = cv2.boundingRect(rota)
    recmat = np.array([[[x, y]], [[x + w, y]], [[x + w, y + h]], [[x, y + h]]])
    rota_rec = rotate_contour(recmat, rotatepoint, -rotateangel)

    return rota_rec


#基于扫描线的胸径位置自动定位算法
def findDBH(conts,params, cam_mtx, f,depth,measurehigh=1300):

    ret = True
    DBHpoint = []
    fx=cam_mtx[0,0]
    fy=cam_mtx[1,1]
    #最小外接矩形
    x, y, w, h = cv2.boundingRect(conts)
    '''
    minrect = cv2.minAreaRect(conts)
    recbox = cv2.boxPoints(minrect)
    recbox = np.int0(recbox)
    '''
    rec = findRec(conts)
    recbox = rec.reshape(4, 2)
    sortbox = recbox.tolist()  #拟合得到的四个点需要进行排序
    sortbox.sort(key=lambda x: x[1])
    sortbox[0:2] = sorted(sortbox[0:2])
    sortbox[2:4] = sorted(sortbox[2:4])
    bl, tl = tuple(sortbox[2]), tuple(sortbox[0])  #bottom-left and top-left，转换为元组
    br, tr = tuple(sortbox[3]), tuple(sortbox[1])  #bottom-right and top-right
    for point in zip(*line(*bl, *tl)):
        '''
        hwpoint1, _ = calculate_XYZ(cam_mtx, rvecs, tvec, bl[0], bl[1])
        hwpoint2, _ = calculate_XYZ(cam_mtx, rvecs, tvec, point[0], point[1])
        '''

        imghigh=math.sqrt(pow(bl[0]-point[0],2)/(fx*fx)+pow(bl[1]-point[1],2)/(fy*fy))
        high=imghigh*(depth/math.cos(params/math.pi))
        if (high >= measurehigh-25 and high <= measurehigh + 25):
            point2 = ((br[0] - bl[0]) + point[0], (br[1] - bl[1]) + point[1])  #(bl)->(br)
            p = intersect(conts, point, point2)
            if len(p) > 1:
                DBHpoint.append(p[0])
                DBHpoint.append(p[-1])
                break
    if len(DBHpoint) < 2:
        ret = False
    return ret, DBHpoint, imghigh

#胸径计算模型
def calculateDBH(depth,params,cam_mtx,point1,point2,f):
    fx=cam_mtx[0, 0]
    fy=cam_mtx[1, 1]
    len=math.sqrt(pow(point1[0]-point2[0],2)/(fx*fx)+pow(point1[1]-point2[1],2)/(fy*fy))
    R = depth *len / (math.cos(params/math.pi)*(math.sqrt(4+len*len)-len))
    return 2*R

'''
获得图像深度
'''
def get_depth(cnt,params,h,w,high,cam_mtx,f):
    #获得轮廓最低点
    bottom_most = tuple(cnt[cnt[:, :, 1].argmax()][0])
    mid=(h/2,w/2)

    #mid_XY=pixel2image(cam_mtx,f,mid)
    h_pixel=abs(mid[1]-bottom_most[1])
    #获得图像坐标系中的高度差
    #h=abs(mid_XY[1]-bottom_most_XY[1])
    depth=h/math.tan(math.atan(h_pixel/f)-params/math.pi)
    print("depth：" + str(depth))
    return depth


def pixel2image(cam_mtx,f,p):
    fx = cam_mtx[0, 0]
    fy = cam_mtx[1, 1]
    u0 = cam_mtx[0, 2]
    v0 = cam_mtx[1, 2]
    dx = f / fx
    dy = f / fy

    p_X=(p[0]-u0)*dx
    p_Y=(p[1]-v0)*dy

    p_XY=(p_X,p_Y)
    return p_XY