from PyQt5.QtWidgets import (QWidget,
                             QGridLayout,
                             QHBoxLayout,
                             QLabel,
                             QLineEdit,
                             QCheckBox,
                             QPushButton,
                             QFileDialog)
from PyQt5.QtCore import Qt, pyqtSignal
from lxml import etree
import logging

logger = logging.getLogger('convert_logger')


class ConfigUI(QWidget):

    configFilePath = ""
    parseConfigSignal = pyqtSignal(etree._Element)
    selectResGroupSignal = pyqtSignal(list)

    def __init__(self, parent=None):
        super(ConfigUI, self).__init__(parent)

        grid = QGridLayout()
        self.setLayout(grid)
        ##
        grid.addWidget(QLabel("配置文件:"), 0, 0)
        grid.addWidget(QLabel("资源分组:"), 1, 0)
        grid.addWidget(QLabel("数据编码:"), 2, 0)
        ##
        self.configFileLE = QLineEdit()
        # self.configFileLE.setEnabled(False)
        self.configFileLE.setFocusPolicy(Qt.NoFocus)
        grid.addWidget(self.configFileLE, 0, 1)
        browsePB = QPushButton("浏览")
        browsePB.clicked.connect(self.browse_config_path)
        grid.addWidget(browsePB, 0, 2)
        ##
        self.resGroupWidget = QWidget()
        self.resGroupLayout = QHBoxLayout()
        self.resGroupWidget.setLayout(self.resGroupLayout)
        grid.addWidget(self.resGroupWidget, 1, 1)
        selectPB = QPushButton("选择")
        selectPB.clicked.connect(self.select_res_group)
        grid.addWidget(selectPB, 1, 2)

    # def create_config

    def browse_config_path(self):
        open = QFileDialog()
        # self.configFilePath = open.getOpenFileUrl(None, "选择转换列表文件")
        self.configFilePath = open.getOpenFileName(None, "选择转换列表文件", "./")
        self.configFileLE.setText(self.configFilePath[0])
        if self.configFilePath[0] != "":
            list = etree.parse(self.configFilePath[0])
            root = list.getroot()
            for item in root:
                if item.tag == "ConvTree":
                    # 转换树
                    self.parseConfigSignal.emit(item)
                elif item.tag == "ResStyleList":
                    # 资源分组
                    self.parse_res_group(item)

            pass

    def select_res_group(self):
        groups = self.resGroupWidget.children()
        if len(groups) > 0:
            resGroupArr = []
            for item in groups:
                if isinstance(item, QCheckBox):
                    if item.isChecked():
                        resGroupArr.append(int(item.text().split(" ")[1]))
            self.selectResGroupSignal.emit(resGroupArr)

    def parse_res_group(self, item):
        while self.resGroupLayout.count():
            self.resGroupLayout.takeAt(0)

        for node in item:
            if node.tag != "ResStyle":
                continue

            print(node.attrib["Name"])
            checkBox = QCheckBox(node.attrib["Name"] + " " + str(node.attrib["ID"]))
            self.resGroupLayout.addWidget(checkBox)
        self.resGroupLayout.addStretch()