import sys
import numpy as np
import requests
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (QApplication, QDialog, QFileDialog, QGridLayout, QLabel, QPushButton, QWidget,
                             QInputDialog, QLineEdit, QMainWindow)
from PyQt5.QtCore import *
import baiduTools       #另一个文件，存放着百度AI人脸识别功能所需要的函数
import re
import os
import random

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36"}
fileName='' #fileName为正在展示的图片的路径

class Menu(QWidget):        #创建类，生成窗口
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("人脸信息识别")
        self.resize(1500,900)

        #创建GUI界面所需要的标签和按钮
        self.btnOpen = QPushButton('打开本地图片', self)
        self.btnUrl = QPushButton('输入URL', self)
        self.btnDownload = QPushButton('下载图片', self)
        self.btnProcess = QPushButton('人脸信息', self)
        self.btnCompare = QPushButton('人脸对比',self)
        self.btnHelp = QPushButton('帮助', self)
        self.label1 = QLabel(self)      #展示图片的窗口
        self.label2 = QLabel(self)      #展示信息的窗口
        self.label1.setAlignment(Qt.AlignCenter)
        self.label1.setStyleSheet("QLabel{background:white;}")
        self.label2.setStyleSheet("QLabel{background:white;}")
        self.label1.setText("你不打开一张图片我没办法运行的")

        #GUI布局
        layout = QGridLayout(self)
        layout.addWidget(self.label1, 0, 1, 3, 2)
        layout.addWidget(self.label2, 0, 3, 3, 1)
        layout.addWidget(self.btnOpen, 4, 1, 1, 1)
        layout.addWidget(self.btnUrl, 4, 2, 1, 1)
        layout.addWidget(self.btnDownload, 4, 3, 1, 1)
        layout.addWidget(self.btnProcess, 5, 1, 1, 1)
        layout.addWidget(self.btnCompare, 5, 2, 1, 1)
        layout.addWidget(self.btnHelp, 5, 3, 1, 1)

        #将按钮与其对应的函数槽连接
        self.btnOpen.clicked.connect(self.open_func)
        self.btnUrl.clicked.connect(self.url_func)
        self.btnDownload.clicked.connect(self.download_func)
        self.btnProcess.clicked.connect(self.process_func)
        self.btnCompare.clicked.connect(self.compare_func)
        self.btnHelp.clicked.connect(self.help_func)

#实现打开图片功能的函数
    def open_func(self):
        global fileName
        try:
            imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "", "*.jpg;;*.png;;All Files(*)")
            self.show_img(imgName)
            fileName = imgName
        except:
            self.label2.setText("没打开，再试一次吧！")

#实现URL下载功能的函数
    def url_func(self):
        global fileName
        try:
            url, okPressed = QInputDialog.getText(self, "", "输入URL：", QLineEdit.Normal, "")
            response = requests.get(url, headers=headers)
            html = response.content
            imgName, tmp = QFileDialog.getSaveFileName(self, '保存图片', 'untitled', '*.jpg *.png *.bmp;;All Files(*)')
            fp = open(imgName, 'wb')
            fp.write(html)
            fp.close()
            self.show_img(imgName)
            fileName = imgName
        except:
            self.label2.setText("没下载下来怎么办？")

#在百度图片上搜索关键字并随机下载一张图片的函数
    def download_func(self):
        global fileName
        try:
            keyword, okPressed = QInputDialog.getText(self, "下载图片", "输入关键字：", QLineEdit.Normal, "")
            page_url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + keyword + '&pn=10&gsm=80&ct=&ic=0&lm=-1&width=0&height=0'    #下载的地址
            response = requests.get(page_url, headers=headers)
            html = response.text
            urllist = re.findall('"objURL":"(.*?)".', html, re.S)       #找到页面中所有的URL
            img_url = random.choice(urllist)                 #选择其中一张图片进行下载
            img = requests.get(img_url, headers=headers, timeout=20)
            name = keyword + '.jpg'
            fp = open(name, 'wb')
            fp.write(img.content)
            fp.close()
            self.show_img(name)
            fileName = name
        except:
            self.label2.setText("图片没下载下来，再试一次吧！")

#实现图片信息识别的函数
    def process_func(self):
        if fileName != '':
            try:
                result = baiduTools.get_info(fileName)  #函数具体见baiduTool.py
                self.label2.setText(result)
            except:
                self.label2.setText("识别失败，再试一次呗！")
        else:
            self.label2.setText('没图我识别个鬼哟！')

#实现图片对比功能的函数
    def compare_func(self):
        if fileName != '':
            try:
                imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "", "*.jpg;;*.png;;All Files(*)")
                score = baiduTools.compare(fileName, imgName)
                self.label2.setText("人脸相似度为" + score + "%")
            except:
                self.label2.setText("对比失败，再来一次吧")
        else:
            self.label2.setText("不打开图片我怎么判断啊！")

#帮助面板的内容
    def help_func(self):
        self.label2.setWordWrap(True)
        help_text="1. 在进行人脸识别前，请先打开一张人脸图片，可以从本地打开（打开本地图片），可以输入图片的URL地址进行下载（输入URL），也可以输入关键字，从百度图片上自动下载一张有关图片（下载图片）。\n" \
                  "2. 人脸信息是通过百度AI的人脸识别功能，自动捕捉图片中的人脸信息（包括年龄、长相、表情、、脸型、性别、眼镜、种族和人脸类型），捕捉到最多人脸数为5，其余人脸不予捕捉，顺序按照人脸大小进行排列\n" \
                  "3. 图片对比功能可以对比两张人脸的相似度，判断是否为同一人。\n" \
                  "4. 使用前请先检查网络连接稳定，若网络不稳定，则无法下载图片或进行人脸识别，开始识别人脸会比较慢，请耐心等待。\n" \
                  "感谢使用！"
        self.label2.setText(help_text)

#将图片展示在LABEL1中的函数
    def show_img(self, imgName):
        image = QPixmap(imgName).scaled(self.label1.width(),self.label1.height())
        self.label1.setPixmap(image)


if __name__ == '__main__':
    a = QApplication(sys.argv)
    main_UI = Menu()
    main_UI.show()
    sys.exit(a.exec_())
