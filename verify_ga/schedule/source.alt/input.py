import subprocess
import numpy as np

if __name__ == "__main__":
    input_data = " ".join([str(i) for i in np.random.randint(1,5,100)])
    print(input_data)
    # subprocess.run(args=['./schedule']+["1","2","3"],input=input_data.encode(),check=False)
    inp_ = [1, 2, 3, 2, 2, 0.5498716521613273, 1, 1, 1, 1, 1, 2, 3, 1, 3, 2, 1, 0.5320328317216059]
    inp_ = " ".join([str(i) for i in inp_]).encode()
    subprocess.run(args=['./schedule']+["0","0","0"],input=inp_,check=False)
    
    pass