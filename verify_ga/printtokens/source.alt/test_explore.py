import imp
from sympy import im
# from import *
import angr
import claripy
from angr import SimFileStream
from pycui import *
import logging

from pandas import options
color = pycui()
logging.getLogger('angr.manager').setLevel(logging.DEBUG) #用来记录日志

project = angr.Project("./print_tokens",load_options={'auto_load_libs':False})


# 2.进行符号执行，获取新的状态地址
# arg1 = [claripy.BVS(f'ch_{i}', 8) for i in range(10)] 
# arg2 = [claripy.BVS(f'ch_{i}', 8) for i in range(10)] 
stdin = [claripy.BVS(f'stdin_{i}', 8)for i in range(40)] 
# v2 = claripy.BVS('v2', 24)
# v3 = claripy.BVS('v3', 8)

initial_state = project.factory.entry_state(
    args=["./replace"],
    # input=claripy.Concat(*flags+[claripy.BVV(b'\n')])
    stdin=SimFileStream('stdin',content=claripy.Concat(*stdin+[b'\n']),has_end=True)
)
for i in stdin:
    initial_state.solver.add(i>=0x20,i<0x7e)
# for i in arg1:
#     initial_state.solver.add(i>=0x20,i<0x7e)
simulation = project.factory.simgr(initial_state)

# loopseer = angr.exploration_techniques.LoopSeer()
# simulation.use_technique(loopseer)
def need(state):
    print("active state input: ",state.posix.dumps(0))
    print("active state input: ",state.posix.dumps(1))

    out = state.posix.dumps(1)
    return b"ARRIVE1" in out
simulation.explore(find=need)

if simulation.found:
    color.success("found!!!")
    state = simulation.found[0]
    print(state.posix.dumps(0))
    print(state.posix.dumps(1))
else:
    color.error("no found!")
# initial_state.globals['concrect'] = 0
# initial_state.globals['scanf_solutions'] = []
# new_states = []
# while simulation.active:
#     for state in simulation.active:
#         print("constrains length is",len(state.solver.constraints))
#         print("active state input:  ",state.posix.dumps(0))
#         ans1 = b""
#         for i in arg1:
#             ans1 += state.solver.eval(i,cast_to=bytes)
#         print("ans1:",ans1)
#         ans2 = b""
#         for i in arg2:
#             ans2 += state.solver.eval(i,cast_to=bytes)
#         print("ans2:",ans2)
#         ans3 = b""
#         for i in stdin:
#             ans3 += state.solver.eval(i,cast_to=bytes)
#         print("ans3:",ans3)
#         # color.error(f"长度-->{len(state.globals['scanf_solutions'])}")
#         # def dd(state):
#         #     # color.error(f"长度-->{len(state.globals['scanf_solutions'])}")
#         #     return len(state.solver.constraints) > 100
#         # simulation.drop(filter_func=dd)
#         print("active state output:  ",state.posix.dumps(1))
#     simulation.step()