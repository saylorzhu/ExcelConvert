__author__ = 'tylerzhu'

from lxml import etree


class Macro():
    def __init__(self, name, value, desc):
        self.name = name
        self.value = value
        self.desc = desc


class StructItem():
    def __init__(self, name, type, cname, size, count, refer):
        self.name = name
        self.type = type
        self.cname = cname
        self.size = size
        self.count = count
        self.refer = refer


class Struct():
    def __init__(self, name, sort_key, items, is_refered, version):
        self.name = name
        self.sort_key = sort_key
        self.items = items
        self.is_refered = is_refered
        self.version = version


class MetaConfig():
    def __init__(self, config):
        self.meta = {}
        self.macros = []
        self.structs = []
        #
        self.load_config(config)

    def get_macro_by_name(self, name):
        if name != "":
            for macro in self.macros:
                if macro.name == name:
                    return macro
        return None

    def load_config(self, config):
        # 解析meta文件
        meta_file = etree.parse(config)
        meta_root = meta_file.getroot()

        #
        self.meta = meta_root.attrib
        for node in meta_root:
            # macro
            if node.tag == "macro":
                macro = Macro(
                    node.attrib["name"],
                    node.attrib["value"],
                    node.attrib["desc"]
                )
                self.macros.append(macro)
            elif node.tag == "struct":
                self.structs.append(
                    self.parse_struct(node)
                )
        pass

    def parse_struct(self, node):
        struct_name = node.attrib["name"]
        struct_version = node.attrib["version"]
        struct_sortkey = None
        if "sortkey" in node.attrib:
            struct_sortkey = node.attrib["sortkey"]

        struct_items = []
        for item in node:
            if item.tag != "entry":
                continue
            name = item.attrib["name"]
            type = item.attrib["type"]
            cname = item.attrib["cname"]
            # 数组元素个数，如果为0表示不是数据
            count = 0
            if "count" in item.attrib:
                count = item.attrib["count"]
            # 字符串的大小，如果为0表示不是字符串
            size = 0
            if "size" in item.attrib:
                size = item.attrib["size"]
            refer = None
            if "refer" in item.attrib:
                refer = item.attrib["refer"]

            # name, type, cname, size, count, refer
            struct_item = StructItem(
                name, type, cname, size, count, refer
            )
            struct_items.append(struct_item)

        # 生成结构体（name, sort_key, items, is_refered, version）
        return Struct(
            struct_name, struct_sortkey, struct_items, False, struct_version
        )
        pass