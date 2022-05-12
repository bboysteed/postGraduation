import os
import subprocess
import pipes
for name in os.listdir("./out/queue"):
    file = os.path.join(os.path.dirname(__file__), "out", "queue", name)
    # os.system()
    # print(pipes.quote(file))
    # for sample in [":", ","]:
    # file = file.replace(sample, "\\"+sample)
    print(file)

    command = "cat " + file + " | ./schedule 1 2 3"
    print(command)
    subprocess.run(command, shell=True)
