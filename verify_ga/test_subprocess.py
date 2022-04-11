import subprocess

# cases = ["+781", "+52", "0*2", "+989", "Z86", "016:", "-0|0", "0508", "992&", "<000", ":00:", "896"]
cases = [b'0*\x002']
new_cases = []
for case in cases:
    case = case.decode(encoding='utf-8',errors='ignore')
    print("{}".format(case))
    ret = subprocess.check_output(args=["./test_atoi",case])
    print(ret)
    new_cases.append(ret.decode())