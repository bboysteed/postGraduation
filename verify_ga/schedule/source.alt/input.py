import subprocess
import numpy as np

if __name__ == "__main__":
    input_data = " ".join([str(i) for i in np.random.randint(1,5,100)])
    print(input_data)
    # subprocess.run(args=['./schedule']+["1","2","3"],input=input_data.encode(),check=False)
    inp_ = [2, 2, 3, 2, 2, 0.5176042429157668, 1, 1, 1, 3, 2, 1, 0.731651050492776, 1, 2, 3, 1, 2, 2, 1, 0.8848334343338776, 3, 3, 1, 2, 1, 2, 2, 1, 0.018305451770533443, 3, 2, 2, 0.834221141803318, 1, 3, 2, 2, 0.9747523326274525, 1, 2, 1, 3, 1, 1, 1, 3, 1, 1, 1, 3, 2, 3, 0.36960060862991684, 1, 3, 1, 2, 1, 1, 3, 2, 2, 0.7159502630272551, 2, 2, 0.4012198849445938, 3, 1, 3, 3, 1, 2, 2, 1, 0.3118289275414633, 2, 2, 0.11679308923100806, 2, 3, 0.0848303205236498, 2, 3, 0.6256638069496985, 3, 2, 3, 0.16522678432610882, 1, 1, 1, 1, 2, 2, 0.9127330711312089, 3, 1, 2, 2, 3, 0.319373312565881, 3, 1, 1, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 3, 2, 3, 0.1645992763708891, 3, 3, 2, 3, 0.8018057861021222, 2, 1, 0.6904572601421686, 2, 3, 0.17212432511262632, 3, 1, 1, 3, 1, 3, 2, 2, 0.6141702424521698, 3, 3, 2, 3, 0.8157241681987907, 2, 3, 0.03116111067941585, 3, 2, 1, 0.6970247343051579, 2, 3, 0.4254646945802789, 3, 2, 3, 0.0972638519241873, 2, 2, 0.09719740618711781, 1, 3, 2, 3, 0.5301488927954163, 3, 2, 3, 0.01600276430871672, 1, 2, 2, 3, 0.14921378958992126, 3, 2, 2, 0.3583925854954372, 2, 2, 0.3538354205172898, 3, 1, 1, 1, 2, 3, 3, 2, 2, 0.2568146479755826, 3, 3, 2, 1, 0.8246053926167135, 1, 2, 3, 2, 1, 0.9507261090228227, 3, 3, 2, 1, 0.2322676371170167, 1, 2, 2, 1, 0.08141821098227708, 3, 2, 1, 0.09781344005097825, 1, 1, 2, 2, 0.4157845289837354, 2, 3, 0.1331708367317057, 2, 2, 0.8852653517295493, 2, 1, 0.7263040213287165, 3, 2, 2, 0.07229423743122088, 1, 3, 2, 2, 0.6005249279507223, 1, 1, 1, 3, 3, 3, 2, 2, 0.10822764605927548, 3, 1, 1, 2, 1, 0.07834572885590829, 1, 2, 1, 3, 1, 3, 2, 3, 0.45975019806642503, 2, 2, 0.27944017367489915, 2, 3, 0.6487155434092908, 3, 3, 2, 2, 0.6304342335598148, 2, 3, 0.09950188234224644, 3, 1, 2, 3, 2, 3, 0.6020230862472463, 2, 3, 0.6627354691522108, 1, 1, 1, 3, 1, 2, 2, 3, 0.3946080897558636, 1, 2, 2, 3, 0.9516648547685841, 3, 2, 2, 0.35500448638591275, 3, 2, 1, 0.9522166183577834, 2, 2, 0.7452297254694877, 2, 1, 0.4443714622706769, 1, 1, 1, 1, 1, 3, 1, 2, 3, 2, 3, 0.4913749540621395, 1, 3, 2, 1, 0.814761013072658, 1, 1, 1, 2, 1, 3, 2, 2, 0.33129350705312965, 2, 1, 0.8503453374689702, 3, 2, 3, 0.6355771598524056, 1, 2, 3, 1, 2, 3, 1, 3, 1, 3, 3, 1, 3, 3, 3, 1, 3, 3, 2, 3, 0.10623001449563019, 2, 3, 0.4195669626612799, 3, 1, 2, 1, 3, 1, 2, 2, 3, 0.8253198031170494, 2, 3, 0.546290821296297, 3, 2, 2, 0.554128684262942, 1, 3, 3, 3, 1, 1, 3, 2, 2, 0.36027947519770764, 1, 2, 1, 3, 1, 2, 1, 2, 1, 1, 1, 1, 1, 3, 3, 1, 3, 1, 2, 1, 2, 1, 3, 2, 2, 0.7111376293947848, 3, 2, 3, 0.6465815172339233, 2, 1, 0.7891336797979206, 3, 1, 3, 2, 3, 0.011000763832674787, 3, 3, 2, 2, 0.1017212795932666, 2, 2, 0.46245869468957423, 3, 3, 2, 1, 0.18990743709826408, 2, 1, 0.5016548776904411, 1, 2, 2, 2, 0.212917491912743, 3, 3, 3, 1, 3, 3, 2, 1, 0.14533636875042466, 1, 1, 1, 1, 3, 2, 1, 0.7161502670497585, 2, 3, 0.8790315001095532, 1, 2, 3, 1, 3, 3, 1, 3, 1, 3, 1, 3, 3, 1, 3, 1, 2, 3, 1, 3, 1, 2, 2, 2, 0.28050287659622675, 2, 2, 0.5266833440317166, 1, 2, 2, 3, 0.7230649445598083, 1, 1, 3, 3, 3, 3, 3, 1, 3, 2, 3, 0.06698867116751694, 3, 2, 1, 0.5504824895019874, 1, 3, 1, 1, 2, 1, 0.1563073869199949, 3, 1, 1, 1, 1, 2, 1, 0.45951654574459067, 1, 3, 2, 1, 0.8178614051209385, 2, 2, 0.916284411755001, 2, 1, 0.32793391299023344, 3, 1, 1, 3, 3, 3, 3, 2, 1, 0.9688209783679708, 2, 2, 0.8955562262728932, 1, 2, 2, 2, 0.08450413479292196, 1, 1, 1, 1, 2, 3, 0.5301920752435085, 1, 2, 3, 2, 1, 0.6304587204843519, 2, 2, 0.4681340764110097]
    inp_ = " ".join([str(i) for i in inp_]).encode()
    subprocess.run(args=['./schedule']+["8","8","8"],input=inp_,check=False)
    
    pass