import os
import subprocess
from xml.dom.minidom import parse

from sko.GA import GA_TSP

from utils.pycui import pycui


class GenerateCases:
    def __init__(self, pro_name, genlength=5, size_pop=4, max_iter=6, prob_mut=1):
        # 定义全局变量
        self.color = pycui()
        self.project_name = pro_name
        self.geneLength = genlength
        self.size_pop = size_pop
        self.max_iter = max_iter
        self.prob_mut = prob_mut
        self.cases_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "tmpFile/cases"))
        self.data_in_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "tmpFile/data.in"))
        self.cases_file = open(self.cases_path, "w+")

        self.intro_class_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../IntroClass"))
        self.module_base_path = os.path.join(self.intro_class_dir, self.project_name)
        self.module_benchFile_path = os.path.join(self.module_base_path, "tests")
        self.makeFile_path = os.path.join(self.module_base_path, "Makefile")
        self.bench_execu_file_path = os.path.join(self.module_benchFile_path, self.project_name)
        self.cov_xml_path = os.path.join(self.module_benchFile_path, "cov.xml")
        self.cov_json_path = os.path.join(self.module_benchFile_path, "cov.json")

        self.register_func()

    #     self.make_engin()
    # def make_engin(self):
    #     if self.project_name == "grade":

    def make_bench_file_clean(self):
        self.color.success("清除编译痕迹...")
        os.system("make -C {} clean".format(self.module_benchFile_path))

    # def make_test_file(self):
    #     self.color.success("编译被测可执行文件...")
    #     os.system("make -C {} all".format(self.module_testFile_path))

    def rewrite_makefile(self):
        self.color.success("重写MakeFile...")
        makeFile = open(os.path.join(self.module_benchFile_path, "Makefile"), "w")
        makeFile.write(
            f"CFLAGS = -lm -ftest-coverage -fprofile-arcs -fPIC\nall: {self.project_name}\nclean:\n\trm -f {self.project_name} {self.project_name}.gcda\n\trm -f {self.project_name}.gcno cov.xml")
        makeFile.close()

    # def make_clean_test_file(self):
    #     color.success("清除被测文件的编译痕迹...")
    #     os.system("make -C {} clean".format(self))

    def make_bench_file(self):
        self.color.success("编译标准可执行文件...")
        os.system("make -C {} all".format(self.module_benchFile_path))

    def run_bench_file(self, inp_b_data):
        ret = subprocess.check_output(self.bench_execu_file_path, stdin=inp_b_data, timeout=2).decode()
        inp_b_data.seek(0)
        # color.info("bench file running result is:{}".format(ret))

    # def run_genprog_tests(self,test_exec_file_path, inp_data, inp_data_str):
    #     refer_res = subprocess.check_output(self.bench_execu_file_path, stdin=inp_data, timeout=3, shell=True).decode()
    #     inp_data.seek(0)  # 这真的是让人咂舌
    #     test_res = subprocess.check_output(test_exec_file_path, stdin=inp_data, timeout=3, shell=True).decode()
    #     color.info("refer_res:{}\n test_res:{}\n".format(refer_res, test_res))
    #     test_passed = check_grade(test_output=test_res, truth_output=refer_res)
    #     color.warning(test_passed)
    #     color.info("Test {}.".format("passed" if test_passed else "failed"))
    #     return True if test_passed else False

    def gcovr_save_xml(self):
        os.system(
            "gcovr -r {} --xml-pretty -o {}/cov.xml".format(self.module_benchFile_path, self.module_benchFile_path))

    # def gcovr_save_test_xml(test_file_path):
    #     os.system("gcovr -r {} --xml-pretty -o {}/test_cov.xml".format(test_file_path, test_file_path))
    #
    # def gcovr_save_json():
    #     os.system("gcovr -r {} --json-pretty -o {}/cov.json".format(module_testFile_path, module_testFile_path))

    def parse_xml_and_get_rate(self):
        rootNode = parse(self.cov_xml_path).documentElement
        line_rate = rootNode.getAttribute("line-rate")  # 行覆盖率
        branch_rate = rootNode.getAttribute("branch-rate")  # 分支覆盖率
        lines_covered = rootNode.getAttribute("lines-covered")  # 覆盖行数
        branches_covered = rootNode.getAttribute("branches-covered")  # 覆盖分支数
        self.color.success("line_rate: {}".format(line_rate))
        return line_rate

    def register_func(self):
        def get_conv_rate(serial):
            for j in range(0, len(serial), self.geneLength):
                tem_ipf = open(self.data_in_path, "w+")
                a_case = list(serial[j:j + self.geneLength])
                sorted_data = sorted(a_case[:-1], reverse=True)
                a_case[:-1] = sorted_data
                bench_input_data = ''
                if self.project_name in ["grade","median","smallest"]:
                    bench_input_data = " ".join([str(ii) for ii in a_case]) + "\n"
                elif self.project_name in ["digits","syllables","checksum"]:
                    bench_input_data = "".join([str(ii) for ii in a_case]) + "\n"


                self.color.info("a case is: {}".format(bench_input_data.rstrip()))
                self.cases_file.write(bench_input_data)
                tem_ipf.write(bench_input_data)
                tem_ipf.seek(0)
                # cui.success("a case has been added to data sets...")
                # cui.info("data:{}".format(tem_ipf.readline()))
                # tem_ipf.seek(0)
                self.run_bench_file(inp_b_data=tem_ipf)  # 运行程序
                tem_ipf.close()
            self.gcovr_save_xml()
            cover_rate = self.parse_xml_and_get_rate()
            return cover_rate

        self.gen_engin = GA_TSP(func=get_conv_rate,
                                n_dim=self.geneLength,
                                size_pop=self.size_pop,
                                max_iter=self.max_iter,
                                prob_mut=self.prob_mut,
                                case_type=self.project_name)

    def run(self, chan):
        best_case, best_covrate = self.gen_engin.run()
        self.color.success("best_points:{}\nbest_distance:{}\n".format(best_case, best_covrate))
        self.cases_file.close()

        message = "genCases ok"
        chan.basic_publish(exchange='',
                           routing_key='goQueue',
                           body=message)
        print(f" python [x] Sent:  {message}")
