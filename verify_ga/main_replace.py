#!/home/steed/.virtualenvs/ga_env/bin/python
from mimetypes import init
import pandas as pd
import numpy as np
import pyecharts.options as opts
from pyecharts.charts import Line
from replace_sko.GA import GA_TSP
from utils.pycui import *
from utils.runfile import *
import os
cui = pycui()

class Target:
    def __init__(self,num_points_,exe_path_,target_name_) -> None:
        self.num_points = num_points_
        self.target_exe_path = exe_path_
        self.target_name = target_name_
        self.makefile()
    def makefile(self):
        if not os.path.exists(os.path.join(self.target_exe_path, "Makefile")):
            makeFile = open(os.path.join(self.target_exe_path, "Makefile"), "w")
            module_name = self.target_name
            makeFile.write(
                f"CFLAGS = -lm -ftest-coverage -fprofile-arcs -fPIC\nall:\n\t$(CC) $(CFLAGS) {module_name}.c -lm -o {module_name}\nclean:\n\trm -f {module_name} {module_name}.gcda\n\trm -f {module_name}.gcno cov.xml\nhtml:\n\tgcovr -r . --html --html-details -o coverage.html")
            makeFile.close()
        #清除痕迹
        os.system("make -C {} clean".format(self.target_exe_path))
        #重新编译
        os.system("make -C {} all".format(self.target_exe_path))



target = Target(num_points_=23,exe_path_=os.path.join(os.path.abspath(os.path.dirname(__file__)),"replace","source.alt"),target_name_="replace")   
# target = Target(num_points_=12,exe_path_=os.path.join(os.path.abspath(os.path.dirname(__file__)),"tcas","source.alt"),target_name_="tcas")   


def get_conv_rate(serial):
    run_bench_file(input_=list(serial),target=target)  # 运行程序
    gcovr_save_xml(target_=target)
    covr_rate = parse_xml_and_get_rate(target_=target)
    return covr_rate   




def println(chrom):
    print("[")
    for item in chrom:
        print("[",",".join(["\"{}\"".format(str(i)) for i in item]),"],")
    print("]")
# %% do GA
def createPopulation(self):
    # 传入的参数仅仅为两个可打印的字符串，第一个表示正则的pattern，第二个表示需要替换为的字符串，
    # 这里设计种群基因的话设计为1-95索引的列表进行交叉变异来模拟传入的两个字符串
    # create the population
    print(self.size_pop, self.len_chrom)
    # 前10位表示arg1 arg2的索引，随机拆分；
    # 后90位表示输入的内容的索引
    tmp1 = np.random.randint(0,95,[self.size_pop, 30])
    # tmp2 = np.random.randint(1,8,[self.size_pop, 20])
    self.Chrom = tmp1

    # self.allChrom += self.Chrom
    return self.Chrom
#gcovr -r . --html --html-details -o coverage.html



def plot_chart(x_data,y_data):

    (
        Line()
        .set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=True),
            xaxis_opts=opts.AxisOpts(type_="value"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
        )
        .add_xaxis(xaxis_data=x_data)
        .add_yaxis(
            series_name="",
            y_axis=y_data,
            symbol="emptyCircle",
            is_symbol_show=True,
            label_opts=opts.LabelOpts(is_show=True),
        )
        .render(os.path.join(target.target_exe_path,f"results_{target.target_name}.html"))
    )

def main():    

    ga_tsp = GA_TSP(func=get_conv_rate, n_dim=target.num_points, crtp=createPopulation, size_pop=4, max_iter=40, prob_mut=0.5)
    visited_state_addr = []
    best_points, best_distance = ga_tsp.run(target_ = target,visited_addr = visited_state_addr)
    print(best_points,best_distance)
    println(ga_tsp.all_old_chrom)
    print(len(ga_tsp.all_old_chrom))


    y_data = [round(float(i),2) for i in ga_tsp.generation_best_Y]
    x_data = np.linspace(1,len(y_data),len(y_data))
    
    df = pd.DataFrame(index=x_data,data=y_data,columns=["代码行覆盖率"])
    df.to_excel(os.path.join(target.target_exe_path,f"{target.target_name}.xlsx"))
    plot_chart(x_data=x_data,y_data=y_data)

   
if __name__ == '__main__':
    main()