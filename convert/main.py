__author__ = 'tylerzhu'

from PyQt5.QtGui import (QIcon)
from PyQt5.QtWidgets import (QApplication,
                             QMainWindow,
                             QHBoxLayout,
                             QVBoxLayout,
                             QWidget,
                             QPushButton,
                             QGroupBox)

from ui.convertlistUi import ConvertList
from ui.configUi import ConfigUI
from ui.convertResultUi import ResultUI
import logging
import time
import datetime
import os


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # set window's title, icon, size info
        self.setWindowTitle("配置转换工具")
        self.setWindowIcon(QIcon("res/main.ico"))
        self.setMinimumSize(160, 160)
        self.resize(1080, 680)

        widget = QWidget()
        self.setCentralWidget(widget)

        self.hbox = QHBoxLayout()
        self.hbox.setContentsMargins(5, 5, 5, 5)
        widget.setLayout(self.hbox)

        # 左边布局
        # 转换列表
        convGroupBox = QGroupBox("转换列表")
        convGroupBoxLayout = QHBoxLayout()
        convGroupBox.setLayout(convGroupBoxLayout)
        self.convertlist = ConvertList()
        convGroupBoxLayout.addWidget(self.convertlist)
        self.hbox.addWidget(convGroupBox)

        # 右边布局
        rwidget = QWidget()
        rwidgetLayout = QVBoxLayout()
        rwidget.setLayout(rwidgetLayout)
        self.hbox.addWidget(rwidget)
        # 1.配置
        confGroupBox = QGroupBox("配置")
        confGroupBoxLayout = QHBoxLayout()
        confGroupBox.setLayout(confGroupBoxLayout)
        self.configUI = ConfigUI()
        confGroupBoxLayout.addWidget(self.configUI)
        rwidgetLayout.addWidget(confGroupBox)

        # 2.转换结果
        convResultGroupBox = QGroupBox("转换结果")
        convResultGroupBoxLayout = QVBoxLayout()
        convResultGroupBox.setLayout(convResultGroupBoxLayout)
        self.resultUI = ResultUI()
        convResultGroupBoxLayout.addWidget(self.resultUI)
        rwidgetLayout.addWidget(convResultGroupBox)

        # 3. 转换按钮
        pbwidget = QWidget()
        vbox = QHBoxLayout()
        pbwidget.setLayout(vbox)
        clearPB = QPushButton("清空提示框")
        convPB = QPushButton("开始转换")
        # submit.clicked.connect(self.onSubmit)
        vbox.addStretch()
        vbox.addWidget(clearPB)
        vbox.addWidget(convPB)
        rwidgetLayout.addWidget(pbwidget)

        # 信号处理
        self.configUI.parseConfigSignal.connect(self.convertlist.parse_conv_list)
        self.configUI.selectResGroupSignal.connect(self.convertlist.select_res_group)
        convPB.clicked.connect(self.convertlist.convert)



def init_logger():
    # 创建一个logger
    logger = logging.getLogger('convert_logger')
    logger.setLevel(logging.DEBUG)
    # 创建一个handler，用于写入日志文件
    if not os.path.exists("log/"):
        os.makedirs("log")
    fh = logging.FileHandler('log/convert'
                             + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S') + '.log')
    fh.setLevel(logging.DEBUG)
    # 再创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # 定义handler的输出格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # 给logger添加handler
    logger.addHandler(fh)
    logger.addHandler(ch)

if __name__ == '__main__':



    import sys
    init_logger()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # window.showFullScreen()
    sys.exit(app.exec_())