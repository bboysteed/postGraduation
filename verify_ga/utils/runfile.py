import subprocess
import os
from xml.dom.minidom import parse
from utils.pycui import pycui
color = pycui()

def run_bench_file(input_,target):
    exefilepath = target.target_exe_path
    color.info(f'input a case :{" ".join([str(i) for i in input_])}')

    if target.target_name == "tcas":
        subprocess.run(args=[os.path.join(exefilepath,target.target_name)]+[str(i) for i in input_],check=False)
    elif target.target_name == "totinfo":
        subprocess.run(args=[os.path.join(exefilepath,target.target_name)]+[str(i) for i in input_],check=False)
    elif target.name == "schedule":
        subprocess.run(args=[os.path.join(exefilepath,target.target_name)]+[str(i) for i in input_],check=False)
    elif target.target_name == "schedule2":
        subprocess.run(args=[os.path.join(exefilepath,target.target_name)]+[str(i) for i in input_],check=False)
    else:
        color.error(f"wrong target name:{target.target_name}")


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