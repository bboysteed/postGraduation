'''
Author: bboysteed 18811603538@163.com
Date: 2022-04-11 21:18:49
LastEditors: bboysteed 18811603538@163.com
LastEditTime: 2022-06-26 20:12:18
FilePath: /verify_ga/utils/runfile.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import subprocess
import os
from xml.dom.minidom import parse
from utils.pycui import pycui
import random
import string


color = pycui()
    
strprintable = string.printable[:100]

def run_bench_file(input_,target):
    exefilepath = target.target_exe_path

    if target.target_name == "tcas":
        color.info(f'input a case :{" ".join([str(i) for i in input_])}')
        subprocess.run(args=[os.path.join(exefilepath,target.target_name)]+[str(i) for i in input_],check=False)

    elif target.target_name == "tot_info":
        input_data = " ".join([str(i) for i in input_[:2]]) + "\n" + " ".join([str(i) for i in input_[10:10+input_[0]*input_[1] ] ] ) + "\n"
        color.info("a case is: {}".format(input_data.encode()))
        subprocess.run(args=[os.path.join(exefilepath,target.target_name)],input=input_data.encode(),check=False)

    elif target.target_name == "schedule":
        input_data = " ".join([str(i) for i in input_[3:]]).encode()
        color.info(f"case->  {input_data}")
        subprocess.run(args=[os.path.join(exefilepath,target.target_name)]+[str(i) for i in input_[:3]],input=input_data,check=False)

    elif target.target_name == "schedule2":
        input_data = " ".join([str(i) for i in input_[3:]]).encode()
        color.info(f"case->  {input_data}")
        subprocess.run(args=[os.path.join(exefilepath,target.target_name)]+[str(i) for i in input_[:3]],input=input_data,check=False)
    elif target.target_name == "replace":

        # random_split_idx = random.randint(0,9)
        random_split_idx = 5
        arg1 = "".join([strprintable[i] for i in input_[:random_split_idx]])
        arg2 = "".join([strprintable[i] for i in input_[random_split_idx:10]])
        inp_data = "".join([strprintable[i] for i in input_[10:]]).encode()
        args=[os.path.join(exefilepath,target.target_name),arg1,arg2]
        
        subprocess.run(args=args,input=inp_data,check=False)    

    elif target.target_name == "print_tokens":
        inp_data = "".join([strprintable[i] for i in input_]).encode()
        args=[os.path.join(exefilepath,target.target_name)]
        color.info(f"case->  {inp_data}")

        subprocess.run(args=args,input=inp_data,check=False)    

    elif target.target_name == "print_tokens2":
        inp_data = "".join([strprintable[i] for i in input_]).encode()
        args=[os.path.join(exefilepath,target.target_name)]
        subprocess.run(args=args,input=inp_data,check=False) 
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