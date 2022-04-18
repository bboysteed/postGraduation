"""
defaultdict(<class 'list'>, {
    'active': [
        <SimState @ 0x401a22>, 
        <SimState @ 0x40174d>,
        <SimState @ 0x401766>,
        <SimState @ 0x4016f2>, 
        <SimState @ 0x4016eb>, 
        <SimState @ 0x401766>, 
        <SimState @ 0x40172e>
      ],
       'stashed': [], 'pruned': [], 'unsat': [], 'errored': [], 'deadended': [], 'unconstrained': []})


"""
import datetime
from os import lseek
import sys
import angr
import claripy
import subprocess
import os
argv = sys.argv
from utils.pycui import *
color = pycui()


def format_cases(chrom):
    return [[str(i) for i in case] for case in chrom]
def pass_cases_to_DSE_and_get_new_case_back_to_GA(pass_cases_,target,visited_addr):
    cases = format_cases(pass_cases_)
    path_to_binary = os.path.join(target.target_exe_path,target.target_name)
    project = angr.Project(path_to_binary) 
    for case in cases:
        initial_state = project.factory.entry_state(args=[path_to_binary]+case)  
        simulation = project.factory.simgr(initial_state)
        while simulation.active:
            for active_state in simulation.stashes['active']:
                if active_state not in visited_addr:
                    visited_addr.append(active_state.addr)

        # a = input("go on?")
            simulation.step()
            # print(simulation.stashes)
    print("all visited addr:\n",visited_addr,len(visited_addr))
    # while(a=="1"):
    #     a = input("go on?")
    #     simulation.strp()
    print(simulation.stashes)


    args = [claripy.BVS("argv{}".format(i),   4 * 8) for i in range(1,13)]+[claripy.BVV(b'\n')]
    # args = claripy.Concat(*args)
    initial_state = project.factory.entry_state(args=[path_to_binary]+args)  
    simulation = project.factory.simgr(initial_state)
    new_state = []
    new_state_addr = []
    while simulation.active:
        for active_state in simulation.stashes['active']:
            if active_state.addr not in visited_addr:
                visited_addr.append(active_state.addr)
                color.success(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")}DSE found the new state!')
                new_state.append(active_state)
        simulation.step()
    if not new_state:
        color.warning("no more new state found !")
    print("new cases addr:\n",new_state,len(new_state))
    all_cases = []
    for state in new_state:
        new_case = []
        for arg in args[:len(args)-1]:
            res = state.solver.eval(arg, cast_to=bytes).replace(b'\x0c',b'').replace(b'\n',b'')#去掉换行符
            # print(res)
            ans_ = bytes.decode(res,errors='ignore').replace('\x00','')
            # print(ans_)
            ret = subprocess.check_output(args=["./test_atoi",ans_])
            new_case.append(ret.decode())
        if new_case not in all_cases:
            all_cases.append(new_case)
    print(all_cases)
    return all_cases

    # import os
    # for case in all_cases:
    #     ret = os.system("./tcas/source.alt/tcas "+" ".join(case))