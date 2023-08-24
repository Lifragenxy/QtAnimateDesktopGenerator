import sys
# import os
import cv2

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import *
from PySide2.QtCore import *
# from PySide2.QtGui import QPalette, QBrush, QPixmap
# import PySide2 as pq
from generator2 import main as generate
from threading import Thread


class Ui_MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        # self.videoName, _ = QFileDialog.getOpenFileName(self, "Open", "", "*.mp4;;*.avi;;All Files(*)")
        self.videoName = "./video.mp4"
        self.timer_camera = QtCore.QTimer()  # 初始化定时器
        self.cap = cv2.VideoCapture()  # 初始化摄像头
        self.cap = cv2.VideoCapture(self.videoName)
        self.CAM_NUM = 0
        self.set_ui()
        self.slot_init()

    def slot_init(self):
        self.timer_camera.timeout.connect(self.show_camera)

    def keyPressEvent(self, event):
        print("按下：" + str(event.key()))
        # 举例
        if (event.key() == Qt.Key_Escape):
            print('测试：ESC')
            self.cap.release()
            self.timer_camera.stop()
            sys.exit()
        if (event.key() == Qt.Key_A):
            print('测试：A')
        if (event.key() == Qt.Key_1):
            print('测试：1')
        if (event.key() == Qt.Key_Enter):
            print('测试：Enter')
        if (event.key() == Qt.Key_Space):
            print('测试：Space')

    def show_camera(self):
        flag, self.image = self.cap.read()
        try:
            show = cv2.resize(self.image, (640, 480))
            if flag == False:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                flag, self.image = self.cap.read()
            if flag == False:
                sys.exit()
            show = cv2.resize(self.image, (self.width(), self.height()))
            self.showFullScreen()
            show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
            showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
            self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(showImage))

        except Exception:
            # 此时已经播放完了一次，需要重新播放一轮
            self.timer_camera = QtCore.QTimer()  # 初始化定时器
            self.cap = cv2.VideoCapture()
            self.cap = cv2.VideoCapture(self.videoName)
            self.CAM_NUM = 0

            flag = True
            if self.videoName == "":
                flag = self.cap.open(0)
            if flag == False:
                pass
            else:
                self.timer_camera.start(30)

            self.slot_init()


    def set_ui(self):
        global lock
        self.__layout_main = QtWidgets.QHBoxLayout()
        self.label_show_camera = QtWidgets.QLabel()
        # self.label_show_camera.setFixedSize(741, 581)
        self.label_show_camera.setAutoFillBackground(True)
        self.__layout_main.setContentsMargins(0, 0, 0, 0)
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowSystemMenuHint | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)
        self.__layout_main.addWidget(self.label_show_camera)
        self.setLayout(self.__layout_main)
        self.setWindowTitle(u'setAsCamwallpaperce84aa7d-3cec-4ef8-b6fd-b3d76e56aa20')
        self.showFullScreen()
        self.showMaximized()
        lock = 1
        flag = True
        if self.videoName == "":
            flag = self.cap.open(0)
        if flag == False:
            pass
        else:
            self.timer_camera.start(30)


def main():
    App = QApplication(sys.argv)
    win = Ui_MainWindow()
    win.show()

    sys.exit(App.exec_())


lock = 0


if __name__ == '__main__':
    main_thread = Thread(target=main)
    generator_thread = Thread(target=generate)
    main_thread.start()
    while (lock == 0):
        pass
    generator_thread.start()