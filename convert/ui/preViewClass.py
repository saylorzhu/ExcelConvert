__author__ = 'tylerzhu'
from PyQt5.QtWidgets import QDialog, QVBoxLayout
from PyQt5.QtWebKitWidgets  import QWebView

from pygments import highlight
from pygments.lexers.c_cpp import CppLexer
from pygments.lexers.dotnet import CSharpLexer
from pygments.formatters.html import HtmlFormatter


class PreViewClass(QDialog):

    def __init__(self, parent=None):
        super(PreViewClass, self).__init__(parent)
        self.resize(990, 550)

        # ��ֱ���֣����ֱ�񼰰�ť
        layout = QVBoxLayout()
        self.setLayout(layout)
        #
        self.webView = QWebView()
        layout.addWidget(self.webView)

    def prev_view_code(self, code, laugange):
        htmlFormatter = HtmlFormatter()
        lexer = CppLexer()
        if laugange == "Cpp":
            lexer = CppLexer()
        elif laugange == "CSharp":
            lexer = CSharpLexer()
        codeDiv = highlight(code, lexer, htmlFormatter)
        codeCss = htmlFormatter.get_style_defs(".highlight")
        #
        html = """
        <html>
            <head>
                <style type="text/css">
                %s
                </style>
            </head>
            <body>
            %s
            </body>
        </html>
        """ % (codeCss, codeDiv)
        self.webView.setHtml(html)
        self.setStyleSheet(codeCss)
        # 输出文件测试验证
        # ff = open('test.html', 'w')
        # ff.write(html)
        # ff.close()
        pass


