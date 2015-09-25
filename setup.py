import sys
from cx_Freeze import setup, Executable

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os", "xlrd3", "xlwt3", "lxml"],
    "excludes": ["tkinter"],
    "include_files": ["res"]
}

#
executables = [
    Executable("main.py", base=base, targetName="ExcelConvert.exe", compress=True, icon="res/main.ico")
]

setup(name="setup",
      version="0.1",
      description="excel convert tool!",
      author="tylerzhu",
      author_email="saylor.zhu@gmail.com",
      options={"build_exe": build_exe_options},
      executables=executables,
)