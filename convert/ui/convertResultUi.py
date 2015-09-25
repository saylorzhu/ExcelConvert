__author__ = 'tylerzhu'
from PyQt5.QtWidgets import (QWidget,
                             QVBoxLayout,
                             QHBoxLayout,
                             QLabel,
                             QLineEdit,
                             QProgressBar,
                             QTextBrowser)
from PyQt5.QtCore import Qt
import logging

logger = logging.getLogger('convert_logger')


class ResultUI(QWidget):

    configFilePath = ""

    def __init__(self, parent=None):
        super(ResultUI, self).__init__(parent)

        layout = QVBoxLayout()
        self.setLayout(layout)
        # 转换结果
        resultText = QTextBrowser()
        # resultText.setFixedWidth(300)
        # resultText.setFixedHeight(300)
        resultText.setFontPointSize(11)
        layout.addWidget(resultText)
        # 转换进度
        progress = QProgressBar()
        layout.addWidget(progress)