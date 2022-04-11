import os
import re
import subprocess
import sys
from xml.dom.minidom import parse
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from utils.pycui import *

"""
    @module_name      全局路径设定
"""

"""
    @color      颜色输出模块
"""
color = pycui()


def check_grade(test_output, truth_output):
    def get_ans(output):
        pat = re.compile('Student has an ([A-D]) grade',re.IGNORECASE)
        m = pat.search(output)
        if m is None:
            p2 = re.compile('Student has (failed) the course',re.IGNORECASE)
            m2 = p2.search(output)
            if m2 is None:
                raise Exception("GRADE: no answer found")
            return m2.group(1)
        return m.group(1)
    truth_answer = get_ans(truth_output)
    grades = set(['A','B','C','D'])
    grade_patterns = {g: re.compile("Student has an {} grade".format(g),
                                    re.IGNORECASE)
                      for g in grades}
    if truth_answer in grades:
        no_neg_match = all([rgx.search(test_output) is None
                            for g, rgx in grade_patterns.items()
                            if g != truth_answer])
        pos_match = grade_patterns[truth_answer].search(test_output)
    elif truth_answer == 'failed':
        failure_rgx = re.compile("Student has failed the course",
                                 re.IGNORECASE)
        no_neg_match = all([rgx.search(test_output) is None
                            for g, rgx in grade_patterns.items()])
        pos_match = failure_rgx.search(test_output)
    else:
        raise ValueError("Unknown grades truth {}".format(truth_answer))
    return pos_match is not None and no_neg_match


def make_bench_file_clean():
    color.success("清除编译痕迹...")
    os.system("make -C {} clean".format(module_testFile_path))


def make_test_file(test_file_path):
    color.success("编译被测可执行文件...")
    os.system("make -C {} all".format(test_file_path))


def rewrite_makefile(test_file_path):
    color.success("重写MakeFile...")
    makeFile = open(os.path.join(test_file_path, "Makefile"), "w")
    makeFile.write(
        f"CFLAGS = -lm -ftest-coverage -fprofile-arcs -fPIC\nall: {module_name}\nclean:\n\trm -f {module_name} {module_name}.gcda\n\trm -f {module_name}.gcno cov.xml")
    makeFile.close()


def make_clean_test_file(test_file_path):
    color.success("清除被测文件的编译痕迹...")
    os.system("make -C {} clean".format(test_file_path))


def make_bench_file():
    color.success("编译标准可执行文件...")
    os.system("make -C {} all".format(module_testFile_path))


def run_bench_file(inp_b_data):
    ret = subprocess.check_output(bench_execu_file_path, stdin=inp_b_data, timeout=2).decode()
    inp_b_data.seek(0)
    # color.info("bench file running result is:{}".format(ret))


def run_genprog_tests(test_exec_file_path, inp_data, inp_data_str):
    refer_res = subprocess.check_output(bench_execu_file_path, stdin=inp_data, timeout=3, shell=True).decode()
    inp_data.seek(0)  # 这真的是让人咂舌
    test_res = subprocess.check_output(test_exec_file_path, stdin=inp_data, timeout=3, shell=True).decode()
    color.info("refer_res:{}\n test_res:{}\n".format(refer_res, test_res))
    test_passed = check_grade(test_output=test_res, truth_output=refer_res)
    color.warning(test_passed)
    color.info("Test {}.".format("passed" if test_passed else "failed"))
    return True if test_passed else False


def gcovr_save_xml():
    os.system("gcovr -r {} --xml-pretty -o {}/cov.xml".format(module_testFile_path, module_testFile_path))


def gcovr_save_test_xml(test_file_path):
    os.system("gcovr -r {} --xml-pretty -o {}/test_cov.xml".format(test_file_path, test_file_path))


def gcovr_save_json():
    os.system("gcovr -r {} --json-pretty -o {}/cov.json".format(module_testFile_path, module_testFile_path))


def parse_xml_and_get_rate():
    rootNode = parse(cov_xml_path).documentElement
    line_rate = rootNode.getAttribute("line-rate")  # 行覆盖率
    branch_rate = rootNode.getAttribute("branch-rate")  # 分支覆盖率
    lines_covered = rootNode.getAttribute("lines-covered")  # 覆盖行数
    branches_covered = rootNode.getAttribute("branches-covered")  # 覆盖分支数
    color.success("line_rate: {}".format(line_rate))
    return line_rate


if __name__ == '__main__':
    pass
