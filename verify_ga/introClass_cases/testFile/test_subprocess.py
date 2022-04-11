import subprocess

if __name__ == '__main__':
    ret = subprocess.run("ls", check=False, shell=True, stdout=subprocess.PIPE)
    print(ret.stdout.decode())
