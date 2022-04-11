#!/home/steed/.virtualenvs/ga_env/bin/python
import angr
import sys
import claripy
import subprocess
def main(argv):
    if len(argv) == 1:
        path_to_binary = "/home/steed/verify_ga/tcas/source.alt/tcas"
    else:
        path_to_binary = argv[1]  # :string
    
    project = angr.Project(path_to_binary)
    #初始状态
    #initial_state = project.factory.entry_state()
    #输入命令行参数后状态
    args = [claripy.BVS("argv{}".format(i),   8 * 8) for i in range(1,13)]+[claripy.BVV('\n')]
    # args = claripy.Concat(*args)
    initial_state = project.factory.entry_state(args=["/home/steed/verify_ga/tcas/source.alt/tcas"]+args)  

    simulation = project.factory.simgr(initial_state)

    #地址寻找法
    # print_good_address = 0x804867d  # :integer (probably in hexadecimal)
    # simulation.explore(find=print_good_address)

    #检查点寻找法（有源码直接插装）
    def arrive_at_check_point(state):
        std_out = state.posix.dumps(sys.stdout.fileno())
        # solution = state.solver.eval(argv1, cast_to=bytes)
        # print(solution)
        return b"arrive2" in std_out
    #print_good_address = 0x804867d  # :integer (probably in hexadecimal)
    simulation.explore(find=arrive_at_check_point)
  # Check that we have found a solution. The simulation.explore() method will
  # set simulation.found to a list of the states that it could find that reach
  # the instruction we asked it to search for. Remember, in Python, if a list
  # is empty, it will be evaluated as false, otherwise true.
    if simulation.found:
    # The explore method stops after it finds a single state that arrives at the
    # target address.
        solution_state = simulation.found[0]

    # Print the string that Angr wrote to stdin to follow solution_state. This 
    # is our solution.
        print('[x]find!!!!_____________________')
        
        new_cases = []
        for arg in args[:len(args)-1]:
            res = solution_state.solver.eval(arg, cast_to=bytes).replace(b'\x0c',b'').replace(b'\n',b'')#去掉换行符
            print(res)
            ans_ = bytes.decode(res,errors='ignore').replace('\x00','')
            print(ans_)
            ret = subprocess.check_output(args=["./test_atoi",ans_])
            new_cases.append(ret.decode())
            print(new_cases)

        print("angr's new case is--> ", " ".join(new_cases))
        print("stdout-->  ",solution_state.posix.dumps(1))

    else:
    # If Angr could not find a path that reaches print_good_address, throw an
    # error. Perhaps you mistyped the print_good_address?
        raise Exception('Could not find the solution')

if __name__ == '__main__':
  main(sys.argv)
