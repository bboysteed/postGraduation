import subprocess
import os
from xml.dom.minidom import parse
from utils.pycui import pycui
color = pycui()

def run_bench_file(input_,target):
    exefilepath = target.target_exe_path
    # # color.success("重写MakeFile...")
    # makeFile = open(os.path.join(exefilepath, "Makefile"), "w")
    # module_name = target.target_name
    # makeFile.write(
    #     f"CFLAGS = -lm -ftest-coverage -fprofile-arcs -fPIC\nall: {module_name}\nclean:\n\trm -f {module_name} {module_name}.gcda\n\trm -f {module_name}.gcno cov.xml")
    # makeFile.close()
    #清除编译痕迹
    # subprocess.call("make -C {} clean".format(exefilepath))
    #编译文件
    # subprocess.run("make -C {} all".format(exefilepath))
    #运行文件
    # print(input_)
    # os.system("{} {}".format(os.path.join(exefilepath,target.target_name),input_.decode()))
    # print(input_)
    # args=
    color.info(f'input a case :{" ".join([str(i) for i in input_])}')
    subprocess.run(args=[os.path.join(exefilepath,target.target_name)]+[str(i) for i in input_[:3]], input=" ".join([str(i) for i in input_[3:]]).encode()+b'\n')
    


def gcovr_save_xml(target_):
    os.system("gcovr -r {} --xml-pretty -o {}/cov.xml".format(target_.target_exe_path, target_.target_exe_path))


def parse_xml_and_get_rate(target_):
    rootNode = parse(os.path.join(os.path.abspath(target_.target_exe_path),"cov.xml")).documentElement
    line_rate = rootNode.getAttribute("line-rate")  # 行覆盖率
    branch_rate = rootNode.getAttribute("branch-rate")  # 分支覆盖率
    lines_covered = rootNode.getAttribute("lines-covered")  # 覆盖行数
    branches_covered = rootNode.getAttribute("branches-covered")  # 覆盖分支数
    color.success("line_rate: {}".format(line_rate))
    return line_rate