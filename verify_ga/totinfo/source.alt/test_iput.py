from re import T
import angr
import subprocess
import os
from angr import SimFileStream
import claripy
import itertools
import logging
logging.getLogger('angr.manager').setLevel(logging.INFO) #用来记录日志


target_name = "./tot_info"
project = angr.Project(target_name)

c = claripy.BVS('c', 8)
r = claripy.BVS('r', 8)  #  int  <-->  0~100

#  claripy.BVV('#',8)
# ,r,claripy.BVV(32,8),c,claripy.BVS("matrix",128),claripy.BVV('\n')
# flag_chars1 =[claripy.BVV(b'+6+853\n223\n232')]
# flag_chars1 = [r.concat(claripy.BVV(b' ',8)),c,b'\n',b'1\n']
# flag_chars1 = r.concat(claripy.BVV('+'),c,claripy.BVV('\n'),claripy.BVV('1+2+3+4+5+6+\n'))
# bytes_list = [r.concat(claripy.BVV(b'+',8),c,b'\n'),b'+1+2+3+4+5+6+7+8+9+10+11+12\n']

# print(flag_chars1)
# all = [claripy.BVS("argv{}".format(i),   1 * 8) for i in range(1,20)]
# exit(0)
flag_chars2 = [claripy.BVS('num_%d'%i, 8) for i in range(10)]
# flag_chars2 = [claripy.BVV(b'4') for i in range(4)]

flag_space = [claripy.BVV(b'+') for i in range(10)]
flag_chars3 = list(itertools.chain.from_iterable(zip(flag_chars2,flag_space)))
bytes_list = [r.concat(claripy.BVV(b'+',8),c,b'\n'),claripy.Concat(*flag_chars3+[claripy.BVV(b'\n')])]
# flag = flag_chars1  + flag_chars2
# flag = claripy.Concat(*all+[claripy.BVV(b'\n')])
# flag = claripy.Concat(*flag_chars1)
# print(flag.ast)
# flag = flag_chars1.concat()
# print(type(flag))
# exit(0)
simFile = angr.SimPackets(name='mypackets',content=bytes_list)
print(simFile.content)
# bytes_list = [claripy.BVS('byte_%d' % i, 8) for i in range(32)]
# bytes_ast = claripy.Concat(*bytes_list)
initial_state = project.factory.entry_state(
    stdin=simFile,

    )
# for byte in bytes_list:
#      initial_state.solver.add(byte >= 0x20)
#      initial_state.solver.add(byte <= 0x7e)
# initial_state = project.factory.entry_state(
#     args=[target_name], 
#     # add_options=angr.options.unicorn,
#     # stdin=flag
#     stdin=SimFileStream(name='stdin', content=flag, has_end=False),
   
#     )
# initial_state = project.factory.full_init_state(args=[target_name],stdin=)  
# for k in all:
#     initial_state.solver.add(k < 58)
#     initial_state.solver.add(k > 47)
initial_state.solver.add(r>48,r<58)
# initial_state.solver.add(r<58)
initial_state.solver.add(c>48,c<58)
# initial_state.solver.add(c<58)

simulation = project.factory.simgr(initial_state)
# simulation.run()

#grab all finished states, that have the win function output in stdout
# y = []
# print(simulation.deadended)
# for x in simulation.deadended:
#     print(x.posix.dumps(1))
    

# def tmp(state):
#     print(state.posix.dumps(0))
#     out = state.posix.dumps(1)
#     ans = b""
#     for flag in flag_chars:
#         ans+=state.solver.eval(flag,cast_to=bytes)
#     print(ans)
#     print(out)
#     return b'total 2info =' in out
# def avoid(state):
#     out = state.posix.dumps(1)
#     return b'* invalid row/column line *' in out or b'* table too large *' in out or b'EOF in table' in out or b'no information accumulated' in out
# simulation.explore(find=tmp)

# print(simulation.stashes)

# if simulation.found:
#     print("found!")
#     print(simulation.found[0].posix.dumps(0))
#     print(simulation.found[0].posix.dumps(1))
# else:
#     print("no found!")

while len(simulation.stashes['active'])>0 :
    print("active length:",len(simulation.stashes['active']))
    
    for st in simulation.active:
        print("dead state input:  ",st.posix.dumps(0))
        print("dead state output:  ",st.posix.dumps(1))
        # ans = b""
        # for flaga in flag_chars1:
        # res = st.solver.eval(r,cast_to=bytes)
        # ans+=res
        # res = st.solver.eval(c,cast_to=bytes)
        # ans+=res
        # for flaga in flag_chars2:
        #     res = st.solver.eval(flaga,cast_to=bytes)
        #     ans+=res
        # print(ans)
    simulation.step()

    print(simulation.stashes)
    # input()
print(simulation.stashes)


if simulation.stashes['unsat']:
    print(simulation.stashes['unsat'][0].solver.constraints)