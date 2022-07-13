'''
Author: bboysteed 18811603538@163.com
Date: 2022-06-26 12:58:34
LastEditors: bboysteed 18811603538@163.com
LastEditTime: 2022-06-27 17:39:07
FilePath: /verify_ga/onlyDSE.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''

import datetime
import random
from utils.pycui import *
import subprocess
import claripy
import angr
import sys
import os
import sys
import threading
from angr import SimFileStream

from utils.runfile import gcovr_save_xml, parse_xml_and_get_rate

args = sys.argv
name = args[1]
color = pycui()


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


rate = 0


def marker(file_name):

    count = 1
    if os.path.exists(file_name):
        os.remove(file_name)

    def write_cov_rate(count):
        count += 1
        with open(file_name, "a") as f:
            f.write(str(rate)+"\n")
            f.close()
        if count > 600:
            color.warning("times up!")
            exit(0)
        threading.Timer(interval=10, function=write_cov_rate,
                        args=(count,)).start()

    th = threading.Timer(
        interval=10, function=write_cov_rate, args=(count,))
    th.start()


def dse_tcas():
    ta = Target(
        0, "/home/t5/mywork/postGraduation/verify_ga/tcas/source.alt/", "tcas")
    marker()
    p = "/home/t5/mywork/postGraduation/verify_ga/tcas/source.alt/tcas"
    project = angr.Project(p)
    args = [claripy.BVS("argv{}".format(i),   4*8)
            for i in range(1, 13)]+[claripy.BVV(b'\n')]
    # args = claripy.Concat(*args)
    initial_state = project.factory.entry_state(args=[p]+args)
    simulation = project.factory.simgr(initial_state)
    new_state = []
    visited_addr = []
    while simulation.active:
        for active_state in simulation.stashes['active']:
            if active_state.addr not in visited_addr:
                visited_addr.append(active_state.addr)
                color.success(
                    f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")}DSE found the new state!')
                new_case = []
                for arg in args[:len(args)-1]:
                    res = active_state.solver.eval(arg, cast_to=bytes).replace(
                        b'\x0c', b'').replace(b'\n', b'')  # 去掉换行符
            # print(res)
                    ans_ = bytes.decode(
                        res, errors='ignore').replace('\x00', '')
            # print(ans_)
                    ret = subprocess.check_output(args=["./test_atoi", ans_])
                    new_case.append(ret.decode())
                subprocess.run(args=[os.path.join(
                    ta.target_exe_path, ta.target_name)]+[str(i) for i in new_case], check=False)
                print("case->", [str(i) for i in new_case])
                gcovr_save_xml(target_=ta)
                covr_rate = parse_xml_and_get_rate(target_=ta)
                global rate
                rate = round(float(covr_rate), 3)
        simulation.step()


def dse_tot_info():
    ta = Target(
        0, "/home/t5/mywork/postGraduation/verify_ga/totinfo/source.alt/", "tot_info")
    marker(f"{ta.target_name}-rate.txt")
    project = angr.Project(
        "/home/t5/mywork/postGraduation/verify_ga/totinfo/source.alt/tot_info")
    flag_chars = [claripy.BVS('num_%d' % i, 8) for i in range(30)]

    flag = claripy.Concat(*flag_chars)
    initial_state = project.factory.entry_state(
        stdin=flag
    )
    for byte in flag_chars:
        initial_state.solver.add(byte >= 0x20)
        initial_state.solver.add(byte <= 0x7e)
    simulation = project.factory.simgr(initial_state)
    # initial_state.globals['concrect'] = 0
    # initial_state.globals['scanf_solutions'] = []
    # initial_state.globals['sscanf_solutions'] = []
    new_states = []
    visited_addr = []
    while simulation.active:
        for state in simulation.active:
            color.success(f"visited len:{len(visited_addr)}")
            print("约束长度为：", len(state.solver.constraints))
            if len(state.solver.constraints) > 200:
                color.success("削减约束")
                for i in range((len(state.solver.constraints)//90)**2*12):
                    state.solver.constraints.pop()
                state.solver.reload_solver()

            if state.addr not in visited_addr:
                color.success(
                    f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")}DSE found the new state!')
                new_states.append(state)
                visited_addr.append(state.addr)
                new_states.append(state)
            # visited_addr.append(state.addr)
                color.success(f"【符号执行】【{state.posix.dumps(0)}】")
                subprocess.run(args=[os.path.join(
                    ta.target_exe_path, ta.target_name)], input=state.posix.dumps(0), check=False)
                gcovr_save_xml(target_=ta)
                covr_rate = parse_xml_and_get_rate(target_=ta)
                color.success(f"cur rate:{covr_rate}")
                global rate
                rate = round(float(covr_rate), 3)

                color.success(f"active state output:  {state.posix.dumps(1)}")

            # print("约束长度：", len(state.solver.constraints))
        simulation.step()


def dse_schedule():
    ta = Target(
        0, "/home/t5/mywork/postGraduation/verify_ga/schedule/source.alt", "schedule")
    marker(f"{ta.target_name}-rate.txt")
    project = angr.Project(
        "/home/t5/mywork/postGraduation/verify_ga/schedule/source.alt/schedule")
    v1 = claripy.BVS('v1', 8)
    v2 = claripy.BVS('v2', 8)
    v3 = claripy.BVS('v3', 8)
    args_ = [claripy.BVS("argv{}".format(i),   8)
             for i in range(1, 4)]
    args2_ = [claripy.BVS("argv{}".format(i),   8)
              for i in range(30)]
    initial_state = project.factory.entry_state(
        args=[
            "/home/t5/mywork/postGraduation/verify_ga/schedule/source.alt/schedule"] + args_,
        # input=claripy.Concat(*flags+[claripy.BVV(b'\n')])
        stdin=SimFileStream(
            'stdin', content=claripy.Concat(*args2_), has_end=True)
    )
    for i in args_+args2_:
        initial_state.solver.add(i >= 0x20, i <= 0x7f)

    simulation = project.factory.simgr(initial_state)
    # initial_state.globals['concrect'] = 0
    # initial_state.globals['scanf_solutions'] = []
    new_states = []
    visited_state_addr = []
    while simulation.active:
        for state in simulation.active:
            print("active len:", len(simulation.active))
            print("constraints len:", len(state.solver.constraints))

            def dd(state):
                a = random.random()
                return a < 0.7
            if len(simulation.active) > 200:
                simulation.drop(filter_func=dd)

            if state.addr not in visited_state_addr:
                color.success(
                    f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")}DSE found the new state!')
                new_states.append(state)
                visited_state_addr.append(state.addr)
                inp = state.posix.dumps(0)
                print("active state output:  ", inp)
                color.success(f"【符号执行】【{inp}】")
                subprocess.run(args=[os.path.join(
                    ta.target_exe_path, ta.target_name)]+[state.solver.eval(i, cast_to=bytes).decode() for i in args_], input=state.posix.dumps(0), check=False)
                gcovr_save_xml(target_=ta)
                covr_rate = parse_xml_and_get_rate(target_=ta)
                color.success(f"cur rate:{covr_rate}")
                global rate
                rate = round(float(covr_rate), 3)

                color.success(f"active state output:  {state.posix.dumps(1)}")

        simulation.step()


def dse_schedule2():

    ta = Target(
        0, "/home/t5/mywork/postGraduation/verify_ga/schedule2/source.alt", "schedule2")
    marker(f"{ta.target_name}-rate.txt")
    project = angr.Project(
        "/home/t5/mywork/postGraduation/verify_ga/schedule2/source.alt/schedule2")
    v1 = claripy.BVS('v1', 8)
    v2 = claripy.BVS('v2', 8)
    v3 = claripy.BVS('v3', 8)
    args_ = [claripy.BVS("argv{}".format(i),   8)
             for i in range(1, 4)]
    args2_ = [claripy.BVS("argv{}".format(i),   8)
              for i in range(30)]

    initial_state = project.factory.entry_state(
        args=[
            "/home/t5/mywork/postGraduation/verify_ga/schedule2/source.alt/schedule2"] + args_,
        # input=claripy.Concat(*flags+[claripy.BVV(b'\n')])
        stdin=SimFileStream(
            'stdin', content=claripy.Concat(*args2_), has_end=True)
    )
    for i in args_+args2_:
        initial_state.solver.add(i >= 0x20, i <= 0x7f)
    simulation = project.factory.simgr(initial_state)
    # initial_state.globals['concrect'] = 0
    # initial_state.globals['scanf_solutions'] = []
    new_states = []
    visited_state_addr = []
    while simulation.active:
        for state in simulation.active:
            print("active len:", len(simulation.active))
            print("constraints len:", len(state.solver.constraints))

            def dd(state):
                a = random.random()
                return a < 0.7
            if len(simulation.active) > 200:
                simulation.drop(filter_func=dd)

            if state.addr not in visited_state_addr:
                color.success(
                    f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")}DSE found the new state!')
                new_states.append(state)
                visited_state_addr.append(state.addr)
                inp = state.posix.dumps(0)
                print("active state output:  ", inp)
                color.success(f"【符号执行】【{inp}】")
                subprocess.run(args=[os.path.join(
                    ta.target_exe_path, ta.target_name)]+[state.solver.eval(i, cast_to=bytes).decode() for i in args_], input=state.posix.dumps(0), check=False)
                gcovr_save_xml(target_=ta)
                covr_rate = parse_xml_and_get_rate(target_=ta)
                color.success(f"cur rate:{covr_rate}")
                global rate
                rate = round(float(covr_rate), 3)

                color.success(f"active state output:  {state.posix.dumps(1)}")

        simulation.step()


def dse_replace():
    ta = Target(
        0, "/home/t5/mywork/postGraduation/verify_ga/replace/source.alt", "replace")
    marker(f"{ta.target_name}-rate.txt")
    project = angr.Project(
        "/home/t5/mywork/postGraduation/verify_ga/replace/source.alt/replace")
    arg1 = [claripy.BVS(f'ch_{i}', 8) for i in range(5)]
    arg2 = [claripy.BVS(f'ch_{i}', 8) for i in range(5)]
    stdin = [claripy.BVS(f'stdin_{i}', 8)for i in range(20)]
    # v2 = claripy.BVS('v2', 24)
    # v3 = claripy.BVS('v3', 8)

    initial_state = project.factory.entry_state(
        args=["/home/t5/mywork/postGraduation/verify_ga/replace/source.alt/replace",
              claripy.Concat(*arg1), claripy.Concat(*arg2)],
        # input=claripy.Concat(*flags+[claripy.BVV(b'\n')])
        stdin=claripy.Concat(*stdin)
    )
    for i in stdin:
        initial_state.solver.add(i >= 0x20, i < 0x7e)
    for i in arg1+arg2:
        initial_state.solver.add(i >= 0x20, i < 0x7e)
    simulation = project.factory.simgr(initial_state,)

    # initial_state.globals['concrect'] = 0
    # initial_state.globals['scanf_solutions'] = []
    new_states = []
    visited_state_addr = []
    while simulation.active:
        for state in simulation.active:
            print("constrains length is", len(state.solver.constraints))
            print("active state input:  ", state.posix.dumps(0))
            ans1 = b""
            for i in arg1:
                ans1 += state.solver.eval(i, cast_to=bytes)
            print("ans1:", ans1)
            ans2 = b""
            for i in arg2:
                ans2 += state.solver.eval(i, cast_to=bytes)
            print("ans2:", ans2)
            ans3 = b""
            # for i in stdin:
            # ans3 += state.solver.eval(i, cast_to=bytes)
            # print("ans3:", ans3)
            # color.error(f"长度-->{len(state.globals['scanf_solutions'])}")
            # def dd(state):
            #     # color.error(f"长度-->{len(state.globals['scanf_solutions'])}")
            #     return len(state.solver.constraints) > 100
            # simulation.drop(filter_func=dd)
            print("active state output:  ", state.posix.dumps(1))
            if state.addr not in visited_state_addr:
                color.success(
                    f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")}DSE found the new state!')
                new_states.append(state)
                visited_state_addr.append(state.addr)
                subprocess.run(args=[os.path.join(
                    ta.target_exe_path, ta.target_name)]+[ans1.decode(), ans2.decode()], input=state.posix.dumps(0), check=False)
                gcovr_save_xml(target_=ta)
                covr_rate = parse_xml_and_get_rate(target_=ta)
                color.success(f"cur rate:{covr_rate}")
                global rate
                rate = round(float(covr_rate), 3)
        simulation.step()


def dse_print_tokens():
    ta = Target(
        0, "/home/t5/mywork/postGraduation/verify_ga/printtokens/source.alt", "print_tokens")
    marker(f"{ta.target_name}-rate.txt")
    project = angr.Project(
        "/home/t5/mywork/postGraduation/verify_ga/printtokens/source.alt/print_tokens")
    stdin = [claripy.BVS(f'stdin_{i}', 8)for i in range(40)]
  # v2 = claripy.BVS('v2', 24)
  # v3 = claripy.BVS('v3', 8)

    initial_state = project.factory.entry_state(
        args=[
            "/home/t5/mywork/postGraduation/verify_ga/printtokens/source.alt/print_tokens"],
        # input=claripy.Concat(*flags+[claripy.BVV(b'\n')])
        stdin=SimFileStream('stdin', content=claripy.Concat(
            *stdin+[b'\n']), has_end=True)
    )
    for i in stdin:
        initial_state.solver.add(i >= 0x20, i < 0x7e)

    simulation = project.factory.simgr(initial_state)
    # initial_state.globals['concrect'] = 0
    # initial_state.globals['scanf_solutions'] = []
    new_states = []
    visited_state_addr = []
    while simulation.active:
        for state in simulation.active:
            print("constrains length is", len(state.solver.constraints))
            print("active state input:  ", state.posix.dumps(0))
            print("active state output:  ", state.posix.dumps(1))
            if state.addr not in visited_state_addr:
                color.success(
                    f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")}DSE found the new state!')
                new_states.append(state)
                visited_state_addr.append(state.addr)
                color.success(f"active state input:  {state.posix.dumps(0)}")
                subprocess.run(args=[
                    "/home/t5/mywork/postGraduation/verify_ga/printtokens/source.alt/print_tokens"], input=state.posix.dumps(0), check=False)
                gcovr_save_xml(target_=ta)
                covr_rate = parse_xml_and_get_rate(target_=ta)
                color.success(f"cur rate:{covr_rate}")
                global rate
                rate = round(float(covr_rate), 3)
                color.success(f"active state input:  {state.posix.dumps(1)}")

        simulation.step()


if __name__ == "__main__":
    if name == "tcas":
        dse_tcas()
    elif name == "tot_info":
        dse_tot_info()
    elif name == "schedule":
        dse_schedule()
    elif name == "schedule2":
        dse_schedule2()
    elif name == "replace":
        dse_replace()
    elif name == "print_tokens":
        dse_print_tokens()
