import math
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import os
import time
import psutil
from PyQt5 import QtGui, QtCore

def qMin(va1, va2):
    if va1<=va2:
        return va1
    else:
        return va2
    pass

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
class cirulars(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint|Qt.Tool)  # 去边框


        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.fsize = 10
        self.resize(250, 250)
        self.layout = QGridLayout(self)
        # 背景填充灰色
        self.setAutoFillBackground(True)
        p = QPalette()
        p.setColor(QPalette.Background, QColor(237, 237, 237))
        self.setPalette(p)
        # 设置进度条颜色
        self.bg_color = QColor(0, 0xBF, 0xBB)
        self.bg_colors = QColor(0, 0xBF, 0xBB)
        # 设置界面刷新时间
        self.startTimer(80)
        self.m_waterOffset = 0.05
        self.m_offset = 50
        self.m_borderwidth = 10
        # 进度条进度范围0-100
        self.per_num = 0
        self.setStyleSheet("QSpinBox,QPushButton{background:transparent;border:1px solid black;}")
        self.statuc = False  # false is updata    true is star
        self.cunt =0  #0_4
        self.btn = QPushButton("", self)
        image_path = resource_path("exit.png")
        self.btn.setIcon(QtGui.QIcon(image_path))
        self.btn.setIconSize(QtCore.QSize(50, 50))
        self.btn.setGeometry(200,0,50,50)
        self.btn.clicked.connect(lambda: os._exit(0))
        self.btn.setStyleSheet("color:rgb(180,180,180)")


    def paintEvent(self, event):
        if self.cunt>0:
            self.cunt -=1
        # print(self.cunt)
        # 锯齿状绘画板；
        painter = QPainter()
        painter.setRenderHint(QPainter.Antialiasing)
        painter.begin(self)
        painter.setPen(Qt.NoPen)
        # 获取窗口的宽度和高度
        width, height = self.width(), self.height()
        side = qMin(width, height)
        percentage = 1 - self.per_num / 100
        if self.statuc:
            percentage=0
        # 水波走向：正弦函数 y = A(wx+l) + k
        # w 表示 周期，值越大密度越大
        w = 2 * math.pi / (side) # width ->side
        # A 表示振幅 ，理解为水波的上下振幅
        A = height * self.m_waterOffset
        # k 表示 y 的偏移量，可理解为进度
        k = height * percentage

        water1 = QPainterPath()
        water2 = QPainterPath()

        # 起始点
        water1.moveTo(0, height)
        water2.moveTo(0, height)
        self.m_offset += 0.6

        if (self.m_offset > (width / 2)):
            self.m_offset = 0
        i = 5
        rect = QRectF(self.fsize, self.fsize, width - self.fsize * 2, height - self.fsize * 2)

        while (i < width - 5):
            waterY1 = A * math.sin(w * i + self.m_offset) + k
            waterY2 = A * math.sin(w * i + self.m_offset + width / 2 * w) + k

            water1.lineTo(i, waterY1)
            water2.lineTo(i, waterY2)
            i += 1

        water1.lineTo(width - 5, height)
        water2.lineTo(width - 5, height)
        totalpath = QPainterPath()
        # totalpath.addRect(QRectF(5, 5, self.width() - 10, self.height() - 10))
        # painter.setBrush(Qt.gray)
        painter.drawRect(self.rect())
        painter.save()
        totalpath.addEllipse(rect)
        totalpath.intersected(water1)
        painter.setPen(Qt.NoPen)

        # 设置水波的透明度
        if self.statuc:
            if(self.cunt>5):
                watercolor1 = QColor(self.bg_colors)
                watercolor1.setAlpha(0) #100
                watercolor2 = QColor(self.bg_colors)
                watercolor2.setAlpha(0) #150
            else:
                watercolor1 = QColor(self.bg_colors)
                watercolor1.setAlpha(120 - (self.cunt +1 ) * 20)  # 100
                watercolor2 = QColor(self.bg_colors)
                watercolor2.setAlpha(120 - (self.cunt + 1 ) * 20+50)  # 150
        else:
            if (self.cunt > 5):
                watercolor1 = QColor(self.bg_color)
                watercolor1.setAlpha(0) #100
                watercolor2 = QColor(self.bg_color)
                watercolor2.setAlpha(0) #150
            else:
                watercolor1 = QColor(self.bg_color)
                watercolor1.setAlpha(120 - (self.cunt +1 ) * 20)  # 100
                watercolor2 = QColor(self.bg_color)
                watercolor2.setAlpha(120 - (self.cunt +1 ) * 20)  # 150

        path = totalpath.intersected(water1)
        painter.setBrush(watercolor1)
        painter.drawPath(path)

        path = totalpath.intersected(water2)
        painter.setBrush(watercolor2)
        painter.drawPath(path)
        painter.restore()
        '''绘制字体'''
        m_font = QFont()
        m_font.setFamily('Microsoft YaHei')
        m_font.setPixelSize(int(self.width() / 9))

        painter.setPen(Qt.black)
        painter.setFont(m_font)
        painter.drawText(60, 70, "BATTERY")
        m_font.setPixelSize(int(self.width() / 5))
        painter.setFont(m_font)
        painter.drawText(60, 130, "UwU")
        m_font.setPixelSize(int(self.width() / 9))
        painter.setFont(m_font)
        painter.drawText(90,200, "{}%".format(self.per_num))
        pen = QPen(QColor(int(153 - 1.53 * self.per_num),
                              int(217 - 0.55 * self.per_num),
                              int(234 - 0.02 * self.per_num)), 7)
        painter.setPen(pen)
        # painter.setPen(QColor(int(153 - 1.53 * self.per_num),
        #                       int(217 - 0.55 * self.per_num),
        #                       int(234 - 0.02 * self.per_num)),)  #
        # painter.setPen(self.pen)
        if self.statuc:
            painter.drawArc(rect, 0, 360 *16)
        else:
            if self.per_num>=100:
                painter.drawArc(rect, 0, 360 *16)
            else:
                painter.drawArc(rect, 90*16 - 57 * self.per_num , 57 * self.per_num)
                painter.end()

    # 鼠标进入处理
    def enterEvent(self, QEvent):
        self.setCursor(QCursor(Qt.PointingHandCursor))
        pass

    # 鼠标离开处理
    def leaveEvent(self, QEvent):
        self.setCursor(QCursor(Qt.ArrowCursor))
        pass

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 獲取滑鼠相對視窗的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改滑鼠圖示

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改視窗位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def timerEvent(self, event):
        battery = psutil.sensors_battery()

        percent = int(battery.percent)
        self.per_num =percent
        time.sleep(0)
        if self.per_num >= 100:
            self.per_num = 100
        self.update()
    def setAngles(self, vale:int):
        if vale<0:
            self.per_num = 0
        elif vale>100:
            self.per_num = 100
        else:
            self.per_num = vale


#

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwin = cirulars()
    mainwin.setWindowRole("20")
    mainwin.show()
    sys.exit(app.exec_())
