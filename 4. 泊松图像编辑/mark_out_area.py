# -*- coding: utf-8 -*-
# @Time    : 2023/1/5 12:07
# @Author  : hp
# @Email   : bingzhenli@hotmail.com
# @File    : draw_polygon.py
# @Project : parttime-exps


import cv2

import numpy as np
import joblib
import matplotlib.pyplot as plt


def _callback(event, x, y, flags, param):
    global img2
    assert img is not None
    img2 = img.copy()

    if event == cv2.EVENT_LBUTTONDOWN:
        pts.append((x, y))

    if event == cv2.EVENT_RBUTTONDOWN:
        pts.pop()

    if len(pts) > 0:
        cv2.circle(img2, pts[-1], 3, (0, 0, 255), -1)

    if len(pts) > 1:
        for i in range(len(pts) - 1):
            cv2.circle(img2, pts[i], 5, (0, 0, 255), -1)
            cv2.line(img=img2, pt1=pts[i], pt2=pts[i + 1], color=(255, 0, 0), thickness=2)

    cv2.imshow('create_polygon', img2)


def draw_polygon(img_pth, pkl_pth, is_save_mask=False):
    global img, pts
    pts = []
    if isinstance(img_pth, str):
        img = cv2.imread(img_pth)
    else:
        img = img_pth

    cv2.namedWindow('create_polygon')
    cv2.setMouseCallback('create_polygon', _callback)

    print("[USAGES]: \n"
          " 1) LEFT CLICK mouse  -> select point\n"
          " 2) RIGHT CLICK mouse -> detect last point\n"
          " 3) press 'p'         -> plot polygon and show, and save points into 'points.pkl' file\n"
          " 5) press 'ESC'       -> exist")

    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break
            
        if key == ord("p"):
            mask = np.zeros(img.shape, np.uint8)
            points = np.array(pts, np.int32)
            points = points.reshape((-1, 1, 2))

            mask = cv2.polylines(mask, [points], True, (255, 255, 255), 2)
            mask2 = cv2.fillPoly(mask.copy(), [points], (255, 255, 255))
            if is_save_mask:
                cv2.imwrite("mask.jpg", mask2)
            mask3 = cv2.fillPoly(mask.copy(), [points], (0, 255, 0))

            show_image = cv2.addWeighted(src1=img, alpha=0.8, src2=mask3, beta=0.2, gamma=0)
            polygon = cv2.bitwise_and(mask2, img)
            
            plt.figure(figsize=(10, 10))
            plt.subplot(1, 3, 1)
            if len(img2.shape) == 3:
                plt.imshow(cv2.merge(cv2.split(img2)[::-1])); plt.title("polygon points")
            else:
                plt.imshow(img2, cmap=plt.cm.gray); plt.title("polygon points")
                
            plt.subplot(1, 3, 2)
            if len(mask2.shape) == 3:
                plt.imshow(cv2.merge(cv2.split(mask2)[::-1])); plt.title("mask")
            else:
                plt.imshow(mask2, cmap=plt.cm.gray); plt.title("mask")
                
            plt.subplot(1, 3, 3)
            if len(show_image.shape) == 3:
                plt.imshow(cv2.merge(cv2.split(show_image)[::-1])); plt.title("image with mask")
            else:
                plt.imshow(show_image, cmap=plt.cm.gray); plt.title("image with mask")
            # plt.subplot(2, 2, 4)
            # plt.imshow(polygon); plt.title("bitwise_and")
            plt.show()
            
            joblib.dump(value=pts, filename=pkl_pth)
            print("[INFO] polygon points coordinates had been saved in 'points.pkl' ... ")
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    draw_polygon("src.jpg", "points.pkl")
