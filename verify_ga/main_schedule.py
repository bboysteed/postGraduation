#!/home/steed/.virtualenvs/ga_env/bin/python
from mimetypes import init
from re import T
import numpy as np
import pyecharts.options as opts
from pyecharts.charts import Line
from schedule_sko.GA import GA_TSP
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



target = Target(num_points_=23,exe_path_=os.path.join(os.path.abspath(os.path.dirname(__file__)),"schedule","source.alt"),target_name_="schedule")   
# target = Target(num_points_=12,exe_path_=os.path.join(os.path.abspath(os.path.dirname(__file__)),"tcas","source.alt"),target_name_="tcas")   


def get_conv_rate(serial):
    run_bench_file(input_=list(serial),target=target)  # 运行程序
    gcovr_save_xml(target_=target)
    covr_rate = parse_xml_and_get_rate(target_=target)
    global rate
    rate = round(float(covr_rate), 2)
    return covr_rate   




def println(chrom):
    print("[")
    for item in chrom:
        print("[",",".join(["\"{}\"".format(str(i)) for i in item]),"],")
    print("]")
# %% do GA
def createPopulation(self):
    # create the population
    print(self.size_pop, self.len_chrom)
    tmp1 = np.random.randint(0,10,[self.size_pop, 3])
    tmp2 = np.random.randint(1,8,[self.size_pop, 20])
    self.Chrom = np.concatenate([tmp1,tmp2],axis=1)

    # self.allChrom += self.Chrom
    return self.Chrom


#gcovr -r . --html --html-details -o coverage.html
rate = 0


def main():

    ga_tsp = GA_TSP(func=get_conv_rate, n_dim=target.num_points,
                    crtp=createPopulation, size_pop=10, max_iter=200, prob_mut=0.5)

    import threading

    count = 1
    if os.path.exists(f"{target.target_name}_cov_rate.txt"):
        os.remove(f"{target.target_name}_cov_rate.txt")

    def write_cov_rate(count):
        count += 1
        with open(f"{target.target_name}_cov_rate.txt", "a") as f:
            f.write(str(rate)+"\n")
            f.close()
        if count > 60:
            color.warning("times up!")
            exit(0)
        threading.Timer(interval=10, function=write_cov_rate,
                        args=(count,)).start()

    th = threading.Timer(
        interval=10, function=write_cov_rate, args=(count,))
    th.start()

    visited_state_addr = []
    best_points, best_distance = ga_tsp.run(target_ = target,visited_addr = visited_state_addr)
    print(best_points,best_distance)
    println(ga_tsp.all_old_chrom)
    print(len(ga_tsp.all_old_chrom))

    y_data = [round(float(i),3) for i in ga_tsp.generation_best_Y]
    x_data = np.linspace(1,len(y_data),len(y_data))

    import pandas as pd
    df = pd.DataFrame(index=x_data, data=y_data, columns=["GA"])
    df.to_excel(os.path.join(target.target_exe_path,
                f"{target.target_name}_GA.xlsx"))
    (
        Line()
        .set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=True),
            xaxis_opts=opts.AxisOpts(type_="category"),
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
        .render(os.path.join(target.target_exe_path,f"results_{target.target_name}1.html"))
    )

if __name__ == '__main__':
    main()