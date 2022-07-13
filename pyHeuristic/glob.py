'''
Descripttion: 
version: 
Author: steed
Date: 2022-06-09 18:39:32
LastEditors: bboysteed 18811603538@163.com
LastEditTime: 2022-06-10 14:19:04
'''
import os


class Target:
    def __init__(self, num_points_, exe_path_, target_name_) -> None:
        self.num_points = num_points_
        self.target_exe_path = exe_path_
        self.target_name = target_name_
        self.makefile()

    def makefile(self):
        if not os.path.exists(os.path.join(self.target_exe_path, "Makefile")):
            makeFile = open(os.path.join(
                self.target_exe_path, "Makefile"), "w")
            module_name = self.target_name
            makeFile.write(
                f"CFLAGS = -lm -ftest-coverage -fprofile-arcs -fPIC\nall:\n\t$(CC) $(CFLAGS) {module_name}.c -lm -o {module_name}\nclean:\n\trm -f {module_name} {module_name}.gcda\n\trm -f {module_name}.gcno cov.xml\nhtml:\n\tgcovr -r . --html --html-details -o coverage.html")
            makeFile.close()
        #清除痕迹
        os.system("make -C {} clean".format(self.target_exe_path))
        #重新编译
        os.system("make -C {} all".format(self.target_exe_path))


def _init():
    """ 初始化 """

    global _global_dict
    _global_dict = {

    }


def set_value(key, value):
    """ 定义一个全局变量 """

    _global_dict[key] = value


def get_value(key, defValue=None):
    """ 获得一个全局变量,不存在则返回默认值 """

    try:
        return _global_dict[key]
    except KeyError:  # 查找字典的key不存在的时候触发
        return defValue
