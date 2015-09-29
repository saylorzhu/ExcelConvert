__author__ = 'tylerzhu'


class TResHead():
    def __init__(self):
        self.magic = 1397052237
        self.version = 7
        self.unit = 0
        self.count = 0
        self.metalibHash = 0
        self.resVersion = 0
        self.createTime = ""
        self.resEncoding = "utf-8"
        self.contentHash = 0


class TResHeadExt():
    def __init__(self):
        self.dataOffset = 140
        self.buff = 0


class TResHeadAll():
    def __init__(self):
        self.resHead = TResHead()
        self.resHeadExt = TResHeadExt()