import subprocess
from tabnanny import check

# inp = b'1 1\n 1 1 1 1 1\n 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 '
# inp = "2 2\n 1 1 6 7\n".encode()
# inp = b"2+4\n1+1+1+1+1+1+3+2+5+"
inp = b"2 2\n1 1 6 7\n"
ret = subprocess.run(args=["./tot_info"],input=inp,stderr=subprocess.PIPE,check=False)
# print(ret.stdout)