__author__ = 'tylerzhu'

from string import Template
from lxml import etree
import os
import codecs
from convert.metaParser import *


class CSharpGenerator:

    def generate(self, meta):

        # 解析Meta文件
        meta_config = MetaConfig(meta)
        print(meta_config.meta)

        # meta_config.macros
        macros = []
        for macro in meta_config.macros:
            # print(macro)
            macros.append(str.format("public const int %s = %s;\n" % (macro.name, macro.value)))

        main = meta_config.structs[-1]
        main_struct = ["public class " + main.name +"\n{"]
        for item in main.items:
            print(item.name, item.type, item.cname, item.size, item.count, item.refer)
            print("str(item.count).isdigit() and int(item.count) > 0):", (str(item.count).isdigit() and int(item.count) > 0))
            print("meta_config.get_macro_by_name(item.name) != None:", (meta_config.get_macro_by_name(item.name) != None))
            if (str(item.count).isdigit() and int(item.count) > 0) \
                    or (meta_config.get_macro_by_name(item.count) != None):
                main_struct.append("public " + item.type + "[] " + item.name + ";\n")
            else:
                main_struct.append("public " + item.type + " " + item.name + ";\n")
        main_struct.append("}\n")

        refer_structs = []
        for struct in meta_config.structs:
            print("***************************", struct.name)
            if struct.name == main.name:
                continue

            temp_struct = ["public class " + struct.name +"\n{"]
            # print(struct.name, struct.items, struct.sort_key, struct.is_refered, struct.version)
            for item in struct.items:
                # print(item.name, item.type, item.cname, item.size, item.count, item.refer)
                if item.count > 0:
                    temp_struct.append("public " + item.type + "[] " + item.name + ";\n")
                else:
                    temp_struct.append("public " + item.type + " " + item.name + ";\n")
            temp_struct.append("}\n")

            refer_structs.append(''.join(temp_struct))

        # 模版文件
        template_file = codecs.open("convert/template/csharp_template.tdl", "r", "utf-8")
        tmpl = Template(template_file.read())

        # print("********************", meta_config.structs[-1].name)
        # 模版替换
        lines = []
        lines.append(tmpl.substitute(
            namespace=meta_config.meta["name"],
            macros="".join(macros),
            main_struct=main.name,
            refer_structs="".join(refer_structs),
            main_structs="".join(main_struct),

        ))

        return ''.join(lines)
