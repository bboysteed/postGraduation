import sys

import matplotlib.pyplot as plt
from sko.GA import GA_TSP
# from pyRabbitMQ.rabbitmq_comsumer import py_mq_send
import os

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from grade.getcovrate import *
# from pyRabbitMQ.rabbitmq_comsumer import py_mq_send
from utils.pycui import *

cui = pycui()
num_points = 5

cases_path = os.path.abspath(os.path.join(os.path.dirname(__file__),"tmpFile/cases"))
datain_path = os.path.abspath(os.path.join(os.path.dirname(__file__),"tmpFile/data.in"))
cases_file = None

make_bench_file_clean()
make_bench_file()

"""
    @一个序列长度为20,一共4个用例，每次输入4个用例后记录一次累计覆盖情况
"""


def get_conv_rate(serial):
    # cui.info("A serial is : {}".format(serial))
    for j in range(0, len(serial), num_points):
        tem_ipf = open(datain_path, "w+")
        a_case = list(serial[j:j + num_points])
        sorted_data = sorted(a_case[:-1], reverse=True)
        a_case[:-1] = sorted_data
        bench_input_data = " ".join([str(ii) for ii in a_case]) + "\n"
        cui.info("a case is: {}".format(bench_input_data.rstrip()))
        cases_file.write(bench_input_data)
        tem_ipf.write(bench_input_data)
        tem_ipf.seek(0)
        # cui.success("a case has been added to data sets...")
        # cui.info("data:{}".format(tem_ipf.readline()))
        # tem_ipf.seek(0)
        run_bench_file(inp_b_data=tem_ipf)  # 运行程序
        tem_ipf.close()
    gcovr_save_xml()
    covr_rate = parse_xml_and_get_rate()

    return covr_rate


def gen_loop(chan):
    global cases_file
    cases_file = open(cases_path, "w+")
    ga_tsp = GA_TSP(func=get_conv_rate, n_dim=num_points, size_pop=4, max_iter=6, prob_mut=1, case_type=module_name)
    best_case, best_covrate = ga_tsp.run()


    # mission is over
    message = "genCases ok"
    chan.basic_publish(exchange='',
                       routing_key='goQueue',
                       body=message)
    print(f" python [x] Sent:  {message}")

# # %% plot
# scatter_x = []
# scatter_y = []
# for i in range(0, len(ga_tsp.all_history_Y)):
#     scatter_x.extend([i + 1] * len(ga_tsp.all_history_Y[i]))
#     scatter_y.extend(list(ga_tsp.all_history_Y[i]))
# fig, ax = plt.subplots(   1, 2)
# ax[0].scatter(scatter_x, scatter_y, s=10, alpha=0.5)
# ax[1].plot(ga_tsp.generation_best_Y)
# plt.show()
