import random
import datetime
import subprocess
from xml.dom.minidom import parse
from utils.pycui import pycui
import angr
import os
import claripy
import random
import logging

from utils.runfile import gcovr_save_xml, parse_xml_and_get_rate, run_bench_file


# logging.getLogger('angr.manager').setLevel(logging.INFO)  # 用来记录日志

color = pycui()
random_scanf_num = []


def format_cases(cases):
    # print(cases)
    new_cases = []
    for case in cases:
        r, c = case[0], case[1]
        # print(r,c)
        # print(case)
        new_cases.append(list(case[:2]) + list(case[10:10 + r * c]))
    return new_cases


def tmp(state):
    print("active state input:  ", state.posix.dumps(0))
    print("active state output:  ", state.posix.dumps(1))
    out = state.posix.dumps(1)
    return b'total 2info =' in out


def pass_cases_to_DSE_and_get_new_case_back_to_GA(pass_cases_, target, visited_addr):
    path_to_binary = os.path.join(target.target_exe_path, target.target_name)
    project = angr.Project(path_to_binary)

    class ReplacementScanf(angr.SimProcedure):
        def run(self, format_string, param0):
            # scanf0 = claripy.BVS('scanf', 24)
            # self.state.solver.add(scanf0>0,scanf0<10)
            # scanf1 = claripy.BVS('scanf1', 32)
            # self.state.add_constraints(
            #     claripy.Or(
            #         claripy.And(scanf0>=0,scanf0<99),
            #         claripy.And(-scanf0>=0,-scanf0<99)
            #         )
            # )
            scanf0_address = param0
            # self.state.memory.store(scanf0_address, random.ranint(0,20), endness=project.arch.memory_endness)

            if self.state.globals['concrect'] == 1:
                passed_num = self.state.globals['case'][self.state.globals['idx']]
                # color.info(f"[x] scanf get num: {passed_num}")
                self.state.memory.store(scanf0_address, int(passed_num), endness=project.arch.memory_endness)
                self.state.globals['idx'] += 1
            else:
                num = random.randint(-10, 30)
                random_scanf_num.append(num)
                self.state.memory.store(scanf0_address, num, endness=project.arch.memory_endness)

                # self.state.memory.store(scanf0_address,scanf0, endness=project.arch.memory_endness)
                # sscanf_push.append(scanf0)
                # color.error(self.state.globals['scanf_solutions'])
                if not self.state.globals['scanf_solutions']:
                    self.state.globals['scanf_solutions'] = [num]
                else:
                    self.state.globals['scanf_solutions'].append(num)
            # scanf1_address = param1
            # self.state.memory.store(scanf1_address, scanf1, endness=project.arch.memory_endness)

            return 1

    class ReplacementSscanf(angr.SimProcedure):
        def run(self, address, format_string, param0, param1):
            scanf0 = claripy.BVS('sscanf0', 8)
            scanf1 = claripy.BVS('sscanf1', 8)
            self.state.solver.add(scanf0 > 1, scanf0 < 3)
            self.state.solver.add(scanf1 > 1, scanf1 < 3)
            scanf0_address = param0
            scanf1_address = param1
            if self.state.globals['concrect'] == 1:
                print(self.state.globals['case'])
                print(self.state.globals['idx'])
                passed_num1 = self.state.globals['case'][self.state.globals['idx']]
                # color.info(f"[x]sscanf get num1:{passed_num1}")
                self.state.memory.store(scanf0_address, int(passed_num1), endness=project.arch.memory_endness)
                self.state.globals['idx'] += 1
                passed_num2 = self.state.globals['case'][self.state.globals['idx']]
                # color.info(f"[x]sscanf get num2:{passed_num2}")
                self.state.memory.store(scanf1_address, int(passed_num2), endness=project.arch.memory_endness)
                self.state.globals['idx'] += 1
            else:
                self.state.memory.store(scanf0_address, scanf0, endness=project.arch.memory_endness)
                self.state.memory.store(scanf1_address, scanf1, endness=project.arch.memory_endness)
                self.state.globals['sscanf_solutions'] = [scanf0, scanf1]
            return 2

    class ReplacementFgets(angr.SimProcedure):
        # Finish the parameters to the scanf function. Hint: 'scanf("%u %u", ...)'.
        # (!)
        def run(self, address, size, file_dp):
            # scanf0 = claripy.BVS('scanf0', 8)
            # scanf1 = claripy.BVS('scanf1', 8)
            # self.state.solver.add(scanf0>48,scanf0<58)
            # self.state.solver.add(scanf1>48,scanf1<58)
            # scanf0_address = param0
            self.state.memory.store(address, 'xxxxx', endness=project.arch.memory_endness)
            # self.state.memory.store(address, scanf0.concat(b' ',scanf1,b'\n'), endness=project.arch.memory_endness)
            # scanf1_address = param1
            # self.state.memory.store(scanf1_address, scanf1, endness=project.arch.memory_endness)

            # return 1

    # project.hook_symbol('__isoc99_scanf', ReplacementScanf())
    # project.hook_symbol('__isoc99_sscanf', ReplacementSscanf())
    # project.hook_symbol('fgets', ReplacementFgets())

    # cases = format_cases(pass_cases_)
    # print(cases)
    # visited_state_addr = visited_addr
    # visited_state = []
    # for case in cases:
    #     inp = " ".join([str(i) for i in case[:2]]) + "\n" + " ".join(
    #         [str(i) for i in case[10:10+case[0]*case[1]]]) + "\n"
    #     color.success(f"[具体执行][{inp.encode()}]")

    #     initial_state = project.factory.entry_state(
    #         stdin=inp

    #     )
    #     simulation = project.factory.simgr(initial_state)
    #     # initial_state.globals['case'] = case
    #     # initial_state.globals['idx'] = 0
    #     # initial_state.globals['concrect'] = 1

    #     while len(simulation.stashes['active']) > 0:
    #         # print("active length:",len(simulation.stashes['active']))
    #         for state in simulation.active:
    #             if state.addr not in visited_state_addr:
    #                 visited_state_addr.append(state.addr)
    #                 # visited_state.append(state)
    #         # print("active state input:  ",state.posix.dumps(0))
    #         # print("active state output:  ",state.posix.dumps(1))
    #         # print(simulation.stashes)
    #         simulation.step()
    # # color.success(f"DSE store all visited state address:{visited_state_addr}")
    # color.success(f"all visited state address length is:{len(visited_state_addr)}")
    # print(simulation.deadended[0].posix.dumps(0))
    # print(simulation.deadended[0].posix.dumps(1))
    # 

    # 进行符号执行，获取新的状态地址
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
                    target.target_exe_path, target.target_name)], input=state.posix.dumps(0), check=False)
                gcovr_save_xml(target_=target)
                covr_rate = parse_xml_and_get_rate(target_=target)
                color.success(f"cur rate:{covr_rate}")
                color.success(f"active state output:  {state.posix.dumps(1)}")

            # print("约束长度：", len(state.solver.constraints))
        simulation.step()
        # print("活跃长度：", len(simulation.active))

        if len(new_states) > 1:
            return
    # if simulation.unsat:
        # print(simulation.unsat[0].solver.constraints)

    if not new_states:
        color.warning("no more new state found!")
    new_DSE_cases = []
    for new_st in new_states:
        color.success(f"【符号执行】【{new_st.posix.dumps(0)}】")
        subprocess.run(args=[os.path.join(
            target.target_exe_path, target.target_name)], input=new_st.posix.dumps(0), check=False)
        gcovr_save_xml(target_=target)
        covr_rate = parse_xml_and_get_rate(target_=target)
        color.success(f"cur rate:{covr_rate}")
        color.success(f"active state output:  {new_st.posix.dumps(1)}")
        # sscanf_stored_solution = new_st.globals['sscanf_solutions']
        # scanf_stored_solution = new_st.globals['scanf_solutions']
        # print(scanf_stored_solution)
        # print(sscanf_stored_solution)
        # if sscanf_stored_solution:
        # tmp = list(map(str, map(new_st.solver.eval, sscanf_stored_solution)))
        # sscanf0 = tmp[0]
        # sscanf1 = tmp[1]
        # print("r&c->", sscanf0, sscanf1)
        # print(random_scanf_num)
        # random_scanf_num = []
        # print(scanf_stored_solution)
        # if scanf_stored_solution:
        #     solution_scanf = ' '.join(map(str, map(new_st.solver.eval, scanf_stored_solution)))
        #     print(solution_scanf)
        # print(random_scanf_num)

        # new_DSE_cases.append([int(sscanf0), int(sscanf1)] + [1] * 8 + [int(i) for i in random_scanf_num] + [2] * (
        # 81 - len(random_scanf_num)))
    print("new_DSE_cases:", new_DSE_cases)
    return new_DSE_cases


if __name__ == "__main__":
    from main_totinfo import Target

    target = Target(num_points_=166,
                    exe_path_=os.path.join(os.path.abspath(os.path.dirname(__file__)), "totinfo", "source.alt"),
                    target_name_="tot_info")
    cases = [
        [8, 3, 1, 8, 9, 4, 5, 7, 1, 5, 4, 90, 47, 41, 99, 91, 46, 48, 29, 61, 26, 33, 6, 40, 63, 1, 27, 78, 73, 93, 52,
         2, 23, 26, 44, 40, 35, 65, 59, 15, 79, 34, 60, 99, 93, 25, 61, 21, 61, 24, 24, 27, 79, 77, 88, 92, 70, 90, 12,
         26, 98, 14, 0, 61, 43, 71, 22, 72, 85, 13, 60, 58, 26, 23, 40, 43, 92, 50, 67, 2, 45, 58, 29, 33, 20, 23, 73,
         98, 37, 66, 20],
        [8, 7, 2, 7, 4, 2, 5, 6, 3, 7, 73, 34, 15, 25, 95, 68, 95, 86, 46, 41, 82, 62, 9, 57, 1, 8, 10, 52, 75, 30, 99,
         33, 18, 5, 91, 11, 11, 95, 1, 48, 0, 10, 95, 60, 72, 5, 81, 1, 53, 26, 98, 77, 9, 14, 25, 64, 98, 17, 62, 93,
         9, 33, 31, 98, 58, 8, 37, 98, 25, 67, 29, 8, 44, 73, 23, 68, 82, 63, 28, 47, 58, 25, 75, 27, 79, 60, 96, 53,
         91, 40, 81],
        [4, 9, 1, 9, 8, 2, 2, 9, 6, 4, 64, 54, 72, 35, 55, 37, 65, 68, 44, 59, 55, 96, 19, 80, 84, 41, 95, 15, 84, 45,
         65, 36, 84, 23, 32, 89, 52, 21, 12, 73, 88, 90, 30, 44, 56, 70, 18, 60, 21, 65, 23, 98, 32, 11, 54, 36, 45, 91,
         82, 98, 0, 38, 53, 75, 79, 75, 37, 95, 92, 46, 18, 58, 71, 40, 98, 67, 43, 10, 88, 11, 41, 18, 59, 90, 40, 83,
         56, 62, 18, 60, 23],
        [8, 1, 7, 2, 1, 2, 4, 4, 7, 3, 99, 50, 66, 46, 80, 54, 47, 45, 77, 77, 31, 64, 49, 28, 60, 5, 18, 81, 50, 92,
         63, 19, 93, 66, 98, 71, 73, 77, 34, 18, 74, 26, 25, 24, 81, 8, 56, 63, 55, 17, 83, 30, 27, 37, 51, 62, 26, 82,
         96, 29, 17, 94, 36, 88, 67, 51, 41, 33, 40, 22, 14, 88, 6, 14, 22, 43, 69, 13, 68, 46, 58, 26, 12, 78, 25, 22,
         83, 87, 28, 99, 10],
        # [8,3,1,8,9,4,5,6,1,5,4,90,47,41,99,91,46,48,29,61,26,-43,6,40,63,1,3,-94,73,93,52,2,23,26,44,40,35,65,59,15,-34,34,60,99,93,25,-91,21,61,24,24,27,79,77,88,92,70,90,12,26,98,14,0,61,43,71,22,72,85,-22,60,58,26,23,40,43,35,50,67,2,45,58,29,19,20,23,73,98,37,66,20],
        # [8,7,2,7,4,2,5,6,3,7,73,34,15,25,95,68,95,86,46,41,82,62,9,57,1,8,10,52,75,30,99,33,18,5,91,11,11,95,1,48,0,10,95,60,72,5,81,1,53,26,98,77,9,14,25,64,98,17,62,93,9,33,31,98,58,8,37,98,25,67,29,8,44,73,23,68,82,63,28,47,58,25,75,27,79,60,96,53,91,40,81],
        # [4,9,1,9,8,2,6,9,6,4,64,33,-85,35,55,37,83,68,44,59,31,64,49,28,60,5,18,81,50,92,63,19,93,66,98,71,73,77,34,-28,74,26,25,24,81,8,56,63,55,17,83,30,27,37,51,62,26,82,96,29,17,94,36,88,67,80,41,33,40,22,14,88,6,14,22,43,69,13,68,46,58,6,12,78,25,5,83,87,28,99,10],
        # [8,1,7,2,1,2,4,4,7,3,99,50,66,46,80,54,47,45,77,77,55,96,19,80,84,41,95,15,84,45,65,36,84,23,32,89,52,21,12,73,88,90,30,44,56,70,18,60,21,65,23,98,32,11,54,36,45,91,82,98,0,38,53,75,79,75,37,95,92,46,18,58,71,40,98,67,43,10,88,11,41,18,59,90,40,83,56,62,18,60,23]
    ]
    pass_cases_to_DSE_and_get_new_case_back_to_GA(cases, target)
