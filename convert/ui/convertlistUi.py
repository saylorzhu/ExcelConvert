__author__ = 'tylerzhu'
from PyQt5.QtWidgets import (
    QTreeWidget,
    QTreeWidgetItemIterator,
    QTreeWidgetItem,
    QMenu,
    QAction)
from PyQt5.QtCore import Qt, pyqtSignal
# from PyQt5.QtGui import QMen
import logging

logger = logging.getLogger('convert_logger')


class ConvertItem(QTreeWidgetItem):
    resData = None

    def __init__(self, parent):
        super(ConvertItem, self).__init__(parent)

    def setData(self, column, role, value):
        state = self.checkState(column)
        QTreeWidgetItem.setData(self, column, role, value)
        if (role == Qt.CheckStateRole and
            state != self.checkState(column)):
            treewidget = self.treeWidget()
            if treewidget is not None:
                treewidget.itemChecked.emit(self, column)

    def set_res_data(self, data):
        self.resData = data
        # print("set_res_data....", self, self.resData)

    def get_res_data(self):
        return self.resData

    def get_res_group(self):
        resGroup = []
        count = self.childCount()
        if count > 0:
            for i in range(0, count):
                resGroup.append(self.child(i))
        return resGroup


class ConvertList(QTreeWidget):

    itemChecked = pyqtSignal(object, int)
    root = None
    itemClicked = None

    def __init__(self):
        super(ConvertList, self).__init__()

        self.setHeaderHidden(True) # 隐藏表头
        self.itemChecked.connect(self.handle_item_checked)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.build_tree_context_menu)

    def build_tree_context_menu(self, point):
        # print(point)
        self.itemClicked = self.itemAt(point)
        if self.itemClicked is None:
            return
        # parent = self.itemClicked.parent()
        # if not parent:
        #     print(1)
        #     return
        # if parent.parent():
        #     print(2)
        #     return
        # print(self.itemClicked.get_res_data(), "()()()", self.itemClicked)
        menu = QMenu(self)
        action = QAction("查看C++类", self)
        action.triggered.connect(self.build_cpp_class)
        menu.addAction(action)
        action = QAction("查看C#类", self)
        action.triggered.connect(self.build_csharp_class)
        menu.addAction(action)
        menu.addSeparator()
        action = QAction("转换成二进制数据", self)
        action.triggered.connect(self.build_binrary_data)
        menu.addAction(action)
        action = QAction("转换成xml数据", self)
        action.triggered.connect(self.build_xml_data)
        menu.addAction(action)
        menu.popup(self.viewport().mapToGlobal(point))
        pass

    def parse_conv_list(self, convtree):
        self.blockSignals(True)
        self.clear()
        self.root = ConvertItem(self)
        self.root.setText(0, '配置表')
        self.root.setCheckState(0, Qt.Checked)
        #
        self.create_conv_tree(convtree)
        self.addTopLevelItem(self.root)
        self.blockSignals(False)
        #
        self.root.setExpanded(True)

    def select_res_group(self, groups):
        if self.root is None:
            return

        # 遍历所有转换叶子节点
        it = QTreeWidgetItemIterator(self.root)
        while it.value():
            node = it.value()
            if node.childCount() == 0:
                if int(node.resData["BinStyles"]) in groups:
                    node.setCheckState(0, Qt.Checked)
                else:
                    node.setCheckState(0, Qt.Unchecked)
            it += 1

    def convert(self):
        if self.root is None:
            return

        # 遍历所有转换叶子节点
        it = QTreeWidgetItemIterator(self.root)
        while it.value():
            node = it.value()
            if node.childCount() == 0:
                if node.checkState(0) == Qt.Checked:
                    # print("convert...", node.resData["Name"])
                    pass
            it += 1

    def handle_item_checked(self, item, column):
        self.blockSignals(True)
        # print('ItemChecked', int(item.checkState(column)))
        itemState = item.checkState(column)
        # check child nodes
        count = item.childCount()
        logger.debug("check " + item.text(column) + "'s child check state, child count:" + str(count))
        for i in range(0, count):
            child = item.child(i)
            child.setCheckState(column, itemState)
            childCount = child.childCount()
            if childCount > 0:
                for j in range(0, childCount):
                    child.child(j).setCheckState(column, itemState)

        # check parent nodes
        parent = item.parent()
        while parent is not None:
            count = parent.childCount()
            logger.debug("check " + parent.text(column) + "'s child check state, child count:" + str(count))
            checked = 0
            unchecked = 0
            partially = 0
            for i in range(column, count):
                state = parent.child(i).checkState(column)
                if state == Qt.Checked:
                    checked += 1
                elif state == Qt.Unchecked:
                    unchecked += 1
                else:
                    partially += 1

            if (partially > 0) \
                    or (checked > 0 and unchecked > 0):
                parent.setCheckState(column, Qt.PartiallyChecked)
                logger.debug("%s set check state: Qt.PartiallyChecked", parent.text(column))
            else:
                if checked > 0:
                    parent.setCheckState(column, Qt.Checked)
                    logger.debug("%s set check state: Qt.Checked", parent.text(column))
                else:
                    parent.setCheckState(column, Qt.Unchecked)
                    logger.debug("%s set check state: Qt.Unchecked", parent.text(column))


            # check parent's parent
            parent = parent.parent()

        self.blockSignals(False)

    def create_res_node_item(self, item, parent):
        node = ConvertItem(parent)
        node.setText(0, item.attrib["Name"])
        node.setCheckState(0, Qt.Checked)
        node.set_res_data(item.attrib)

    def create_comm_node_item(self, item, parent):
        node = ConvertItem(parent)
        node.setText(0, item.attrib["Name"])
        node.setCheckState(0, Qt.Checked)
        for res in item:
            if res.tag != "ResNode":
                continue
            # print(res.tag, res.attrib["Name"])
            self.create_res_node_item(res, node)

    def create_conv_tree(self, tree):
        for comm in tree:
            if comm.tag != "CommNode":
                continue
            # print(item.tag, item.attrib["Name"])
            self.create_comm_node_item(comm, self.root)

    def build_cpp_class(self, checked):
        print(self.itemClicked.get_res_data(), "****************************", checked)
        resGroup = self.itemClicked.get_res_group()
        if len(resGroup) > 0:
            # 包含多个资源转换节点
            pass
        else:
            # 只有一个资源节点
            resData = self.itemClicked.get_res_data()
            print(resData["EntryMapFile"])
            from convert.generateCSharpCode import CSharpGenerator
            test = CSharpGenerator()
            test.generate("data/" + resData["EntryMapFile"])
            pass
        pass

    def build_csharp_class(self, checked):
        # print(self.itemClicked.get_res_data(), "****************************", checked)
        resGroup = self.itemClicked.get_res_group()
        if len(resGroup) > 0:
            # 包含多个资源转换节点
            pass
        else:
            # 只有一个资源节点
            resData = self.itemClicked.get_res_data()
            # print(resData["EntryMapFile"])
            from convert.generateCSharpCode import CSharpGenerator
            test = CSharpGenerator()
            code = test.generate("data/" + resData["EntryMapFile"])

            from ui.preViewClass import PreViewClass
            dialog = PreViewClass(self)
            dialog.prev_view_code(code, "CSharp")
            if dialog.exec_():

                print("test")

            print("test1")
        pass

    def build_binrary_data(self, checked):
        print("build binrary data....")
        pass

    def build_xml_data(self, checked):
        print("build xml data....")
        pass

