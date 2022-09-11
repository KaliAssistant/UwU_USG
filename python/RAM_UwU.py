import sys
import os
import psutil
import time
from PyQt5.QtCore import*
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtGui, QtCore

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class CircularProgress(QWidget):
    def __init__(self):
        super().__init__()
        # 记录角度
        #self.cpu_temp = None
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.Tool)

        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.angle = 90
        # 这个是用于绘制的，angle才是真实的角度
        self.drawAngle = self.angle
        # 进度条宽度
        self.lineWidth = 10
        # 时间线做动画
        self.timeLine = QTimeLine(0, self)

        self.timeLine.frameChanged.connect(self.updateTimeline)
        self.startTimer(100)
        # 数字输入框
        #self.input = QSpinBox(self)
        #self.input.setRange(0, 360)
        #self.input.setValue(45)
        #self.input.setGeometry(10, 10, 90, 30)
        # 按钮
        #self.btn = QPushButton("Set", self)
        #self.btn.setGeometry(10, 45, 90, 30)
        #self.btn.clicked.connect(self.setAngle)
        self.setAngle()
        # 透明样式
        self.setStyleSheet("QSpinBox,QPushButton{background:transparent;border:1px solid black;}")
        self.per_num=0
        self.cpu_tmp=0
        self.btn = QPushButton("", self)
        image_path = resource_path("exit.png")
        self.btn.setIcon(QtGui.QIcon(image_path))
        self.btn.setIconSize(QtCore.QSize(50, 50))
        # self.btn.setGeometry(175,200,50,50)
        self.btn.clicked.connect(lambda: os._exit(0))
        self.btn.setStyleSheet("color:rgb(180,180,180)")

    def updateTimeline(self, frame):
        self.drawAngle = frame
        self.per_num = int(psutil.virtual_memory().percent)
        #temp = (psutil.sensors_temperatures().get('acpitz')[0][1])



    def timerEvent(self, event):
        self.angle = int(psutil.virtual_memory().percent*3.6)  # self.input.value()
        #self.cpu_temp = psutil.sensors_temperatures()["cpu_thermal"][0]
        self.per_num=int(psutil.virtual_memory().percent)
        self.timeLine.setFrameRange(self.drawAngle, self.angle)
        self.update()
        self.timeLine.start()
    def setAngle(self):
        self.drawAngle = self.angle
        self.angle =int(psutil.virtual_memory().percent) #self.input.value()
        #self.timeLine.stop()
        self.timeLine.setFrameRange(self.drawAngle, self.angle)
        self.update()
        self.timeLine.start()


    def paintEvent(self, event):
        # 这里有个问题是，pyqt5无法隐式吧QRect转为QRectF(PySide2可以)，所以这里直接用QRectF
        the_rect = QRectF(0, 0, self.width(), self.height())
        if the_rect.isNull():
            return
        # 画笔
        painter = QPainter(self)
        #painter.fillRect(the_rect, QColor("Cyan"))
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform, on=True)
        # 镜像翻转，这样就是顺时针
        painter.setViewport(self.width(), 0, -self.width(), self.height())

        # path默认OddEvenFill，这样就填充两个圆相交的部分
        the_path = QPainterPath()
        the_path.addEllipse(the_rect.adjusted(1, 1, -1, -1))
        the_path.addEllipse(the_rect.adjusted(
            1 + self.lineWidth, 1 + self.lineWidth, -1 - self.lineWidth, -1 - self.lineWidth))
        the_path_color=QColor(60, 60,60 )
        the_path_color.setAlpha(150)
        painter.fillPath(the_path, the_path_color)

        # 径向渐变（参数为中心点和起始角度），默认时从右侧开始逆时针算的
        the_gradient = QConicalGradient(the_rect.center(), 90)
        the_angle = self.drawAngle / 360
        the_gradient_color=QColor(255, 255, 255)
        the_gradient_color.setAlpha(200)
        the_gradient.setColorAt(0, the_gradient_color)
        the_gradient.setColorAt(the_angle, the_gradient_color)
        if the_angle + 0.001 < 1:
            the_gradient.setColorAt(the_angle + 0.001, QColor(0, 0, 0, 0))
        painter.fillPath(the_path, the_gradient)
        painterF = QPainter(self)
        #painterF.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform, on=True)
        m_font = QFont()
        m_font.setFamily('Microsoft YaHei')
        m_font.setPixelSize(int(self.width() / 12))
        m_font_color=QColor(180,180,180)
        m_font_color.setAlpha(180)
        painterF.setPen(m_font_color)
        painterF.setFont(m_font)
        painterF.drawText(160, 50, "RAM")
        painterF.drawText(165, 350, "{}%".format(int(self.angle/3.6)))
        #painterF.drawText(140,100,"{}".format(time.strftime('%H:%M', time.localtime())))

        painterT = QPainter(self)

        t_font = QFont()
        t_font.setFamily('Microsoft YaHei')
        t_font.setPixelSize(int(self.width() /8))
        t_font_color = QColor(180,180,180)
        t_font_color.setAlpha(180)

        painterT.setPen(t_font_color)
        painterT.setFont(t_font)
        painterT.drawText(135,150,"{}".format(time.strftime('%H:%M', time.localtime())))

        painterI = QPainter(self)

        i_font = QFont()
        i_font.setFamily('Microsoft YaHei')
        i_font.setPixelSize(int(self.width() / 6))
        i_font_color = QColor(180, 180, 180)
        i_font_color.setAlpha(180)

        painterI.setPen(i_font_color)
        painterI.setFont(i_font)
        painterI.drawText(125, 275, "UwU")




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
    # def mouseReleaseEvent(self, event): # 鼠标键公开时调用;
    #     if event.button() == Qt.LeftButton:
    #         print("t单击鼠标左键")  # 响应测试语句
    #     elif event.button() == Qt.RightButton:  # 右键按下
    #         print("t单击鼠标右键")  # 响应测试语句

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = CircularProgress()
    w.setWindowTitle("_CPU_")
    w.resize(400, 400)
    w.show()
    sys.exit(app.exec_())