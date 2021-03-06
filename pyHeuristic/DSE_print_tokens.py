from calendar import c
import random
from re import A, T
import datetime
import numpy as np
from sympy import im
from pycui import pycui
import angr
import subprocess
import os
from angr import SimFileStream
import claripy
import itertools
import random
import logging
from main_print_tokens import Target

from pip import main
logging.getLogger('angr.manager').setLevel(logging.INFO) #用来记录日志

color = pycui()
random_scanf_num = []
import string
def format_cases(cases):
    # print(cases)
    printables_str = string.printable[:95]
    new_cases = []
    for case in cases:
        input_data = "".join([printables_str[i] for i in case]).encode()
        new_cases.append(input_data)
    return new_cases


# from angr.procedures.stubs.format_parser import ScanfFormatParser

def pass_cases_to_DSE_and_get_new_case_back_to_GA(pass_cases_,target,visited_addr):
    path_to_binary = os.path.join(target.target_exe_path,target.target_name)
    project = angr.Project(path_to_binary)

    cases = format_cases(pass_cases_)
    # 1.进行具体执行
    print(cases)
    visited_state_addr = visited_addr
    visited_state = []
    for case in cases:
        color.info(f"concrect case is: {case}")
        initial_state = project.factory.full_init_state(
            args=[path_to_binary],
            # input = SimFileStream(name='stdin',content=case[2]+b'\n',has_end=True)
            stdin = case
        )
        simulation = project.factory.simgr(initial_state)
        # initial_state.globals['case'] = case
        # initial_state.globals['idx'] = 3
        # initial_state.globals['concrect'] = 1
    
        while simulation.active:
            simulation.step()

            print("active length:",len(simulation.active))
            for state in simulation.active:
                print(case)
                print("constrains length is",len(state.solver.constraints))
                # color.info(f"this state's idx is: {state.globals['idx']}")
                if state.addr not in visited_state_addr:
                    visited_state_addr.append(state.addr)
                    visited_state.append(state)
                # def dd(state):
                #     # color.error(f"随机数长度-->{len(random_scanf_num)}")
                #     return len(state.solver.constraints) > 80
                # simulation.drop(filter_func=dd)
                # print("active state input:  ",state.posix.dumps(0))
                print("active state output:  ",state.posix.dumps(1))
                print("visited length:  ",len(visited_addr))
            #  print(simulation.stashes)
                print("active length is",len(simulation.active))
        color.warning(f"visited addr length is:{len(visited_state_addr)}")

    color.success(f"DSE store all visited state address:{visited_state_addr}")
    color.success(f"all visited state address length is:{len(visited_state_addr)}")
    # # print(simulation.deadended[0].posix.dumps(0))
    # # print(simulation.deadended[0].posix.dumps(1))
    # # 
    # exit(0)

    # 2.进行符号执行，获取新的状态地址
    stdin = [claripy.BVS(f'stdin_{i}', 8)for i in range(40)] 
    # v2 = claripy.BVS('v2', 24)
    # v3 = claripy.BVS('v3', 8)
    
    initial_state = project.factory.entry_state(
        args=[path_to_binary],
        # input=claripy.Concat(*flags+[claripy.BVV(b'\n')])
        stdin=SimFileStream('stdin',content=claripy.Concat(*stdin+[b'\n']),has_end=True)
    )
    for i in stdin:
        initial_state.solver.add(i>=0x20,i<0x7e)
    simulation = project.factory.simgr(initial_state)
    # initial_state.globals['concrect'] = 0
    # initial_state.globals['scanf_solutions'] = []
    new_states = []
    while simulation.active:
        for state in simulation.active:
            print("constrains length is",len(state.solver.constraints))
            print("active state input:  ",state.posix.dumps(0))
            # ans3 = b""
            # for i in stdin:
                # ans3 += state.solver.eval(i,cast_to=bytes)
            # print("ans3:",ans3)
            # color.error(f"长度-->{len(state.globals['scanf_solutions'])}")
            # def dd(state):
            #     # color.error(f"长度-->{len(state.globals['scanf_solutions'])}")
            #     return len(state.solver.constraints) > 100
            # simulation.drop(filter_func=dd)
            print("active state output:  ",state.posix.dumps(1))
            if state.addr not in visited_state_addr:
                color.success(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")}DSE found the new state!')
                new_states.append(state)
                visited_state_addr.append(state.addr)
        simulation.step()

        if len(new_states)>0:
            break
    # exit(0)
    print(simulation.stashes)
    if simulation.unsat:
        print(simulation.unsat[0].solver.constraints)
    if not new_states:
        color.warning("no more state found!!!")
        import time
        time.sleep(3)
    new_DSE_cases = []
    for new_st in new_states:
        color.success(f"active state input:  {new_st.posix.dumps(0)}")
        color.success(f"active state input:  {new_st.posix.dumps(1)}")
        new_DSE_cases.append([new_st.posix.dumps(0)])
    # exit(0)    
    return new_DSE_cases
    # def tmp(state):
    #     color.info(f"active length is:{len(simulation.active)}")
    #     color.info(f"constraint length is:{len(state.solver.constraints)}")
    #     print("active state input:  ",state.posix.dumps(0))
    #     print("active state output:  ",state.posix.dumps(1))

    #     ans = ""
    #     for i in [v1,v2,v3]:
    #         ans += str(state.solver.eval(i))+" "
    #     # for i in flags1:
    #         # ans += str(state.solver.eval(i))+" "
    #     print(ans)
    #     print(random_scanf_num)
    #     scanf_stored_solution = state.globals['scanf_solutions']
    #     if scanf_stored_solution:
    #         tmp = list(map(str, map(state.solver.eval, scanf_stored_solution)))
    #         print(tmp)
    #     out = state.posix.dumps(1)
    #     return b'arrive2' in out
    
    # simulation.explore(find=tmp)
    # print("finished simulation:",simulation.stashes)
    # print(len(simulation.found))
    # if simulation.found:
        # state = simulation.found[0]
    #     color.success("[x]found!!!!!!!!")
    #     print("found state input:  ",state.posix.dumps(0))
    #     print("found state input:  ",state.posix.dumps(1))
    #     ans = ""
    #     for i in [v1,v2,v3]:
    #         ans += str(state.solver.eval(i,cast_to=bytes))+" "
    #     # for i in flags1:
    #         # ans += str(state.solver.eval(i))+" "
    #     print(ans)
    #     print(random_scanf_num)
    #     scanf_stored_solution = state.globals['scanf_solutions']
    #     if scanf_stored_solution:
    #         tmp = list(map(str, map(state.solver.eval, scanf_stored_solution)))
    #         print(tmp)
    # else:
    #     color.error("no found!")


    # initial_state.globals['concrect'] = 0
    # initial_state.globals['scanf_solutions'] = []
    # initial_state.globals['sscanf_solutions'] = []
    # new_states = []
    # while simulation.active:
        # for state in simulation.active:
            # print("active state input:  ",state.posix.dumps(0))
            # print("active state output:  ",state.posix.dumps(1))
            # if state.addr not in visited_state_addr:
                # color.success(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")}DSE found the new state!')
                # new_states.append(state)
        # simulation.step()
        # if len(new_states)>3:
            # break
    # if simulation.unsat:
    #     print(simulation.unsat[0].solver.constraints)

   
if __name__ == "__main__":
    target = Target(num_points_=32,exe_path_=os.path.join(os.path.abspath(os.path.dirname(__file__)),"schedule2","source.alt"),target_name_="schedule2")   
    cases = [
[ "4","5","7","2","6","1","9","6","8","4","3","1","8","1","5","8","9","2","4","3","1","8","2","1","4","8","8","5","6","3","1","8","8","7","6","6","7","8","8","9","5","4","7","3","2","4","6","1","3","7","7","1","7","5","8","9","8","3","7","6","6","5","6","6","5","7","2","9","6","3","6","3","4","1","3","9","2","1","5","9","5","7","2","9","6","1","3","6","8","3","1","2","5","4","1","5","2","8","5","2","3","4","4" ],
    ]
    visited= []
    pass_cases_to_DSE_and_get_new_case_back_to_GA(cases,target,visited)