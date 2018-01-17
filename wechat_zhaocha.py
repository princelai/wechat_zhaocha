#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 12:16:14 2018

@author: kevin
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import cv2
import random
import string

class zhaocha:
    def pull_screenshot(self):
        """
        截图后传回电脑
        """
        os.system('adb shell screencap -p /sdcard/ss.png')
        os.system('adb pull /sdcard/ss.png . >{}'.format(os.devnull))
        
    def read_img(self):
        """
        读取图像，并转换为RGB模式
        """
        self.img = cv2.imread('ss.png',0)
#        img = cv2.imread(os.path.join('img',random.choice(os.listdir('img'))),0)

    def save_pic(self):
        if not os.path.isdir(os.path.join(os.path.curdir,'img')):
            os.mkdir('img')
        file_name = lambda: ''.join(random.sample(string.ascii_letters + string.digits, 15))
        cv2.imwrite(os.path.join('img',file_name()+'.png'),self.img)
        
        
    def get_xy_cv2(self):
        img1 = self.img[169:979,215:1035]
        img2 = self.img[1030:1840,215:1035]
        kernel = np.ones((5,5),np.uint8)
        compare = np.abs(img1-img2)
        opening = cv2.morphologyEx(compare, cv2.MORPH_OPEN, kernel)
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)   
        dilation = cv2.dilate(closing,kernel,iterations = 4)
        erosion = cv2.erode(dilation,kernel,iterations = 3)
        image ,contours,hierarchy = cv2.findContours(erosion,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        self.contours = contours
        if len(contours) not in [3,10]:
            self.save_pic()            
        self.point = []
        for cnt in contours:
            M = cv2.moments(cnt)            
            self.point.append((int(M['m10']/M['m00'])+215,int(M['m01']/M['m00'])+169))
    

    def show_with_rectangle(self):
        plt.imshow(self.img)
        currentAxis=plt.gca()
        for cnt in self.contours:
            cnt2 = np.squeeze(cnt)
            x1,x2,y1,y2 = (cnt2[:,0].min(),cnt2[:,0].max(),cnt2[:,1].min(),cnt2[:,1].max())
            rect=patches.Rectangle((x1+215,y1+169),x2-x1,y2-y1,linewidth=1,edgecolor='r',facecolor='none')
            currentAxis.add_patch(rect)

    def touch_screen(self):
        for i in range(len(self.point)):
            (x,y) = self.point[i]
            cmd = f'adb shell input tap {x} {y}'
            os.system(cmd)

    def __call__(self):
        while True:
            try:
                input('Enter for continue.')
            except KeyboardInterrupt:
                print('\nBye~')
                break
            self.pull_screenshot()
            self.read_img()
            self.get_xy_cv2()
            self.show_with_rectangle()
            self.touch_screen()


if __name__ == '__main__':
    zc = zhaocha()
    zc()    