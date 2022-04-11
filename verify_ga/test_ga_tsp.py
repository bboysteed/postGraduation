#!/home/steed/.virtualenvs/ga_env/bin/python
import numpy as np
import pyecharts.options as opts
from pyecharts.charts import Line
# from scipy import spatial
# import matplotlib.pyplot as plt


num_points = 24

# points_coordinate = np.random.rand(num_points, 2)  # generate coordinate of points
# distance_matrix = spatial.distance.cdist(points_coordinate, points_coordinate, metric='euclidean')


def cal_total_distance(routine):
    '''The objective function. input routine, return total distance.
    cal_total_distance(np.arange(num_points))
    '''
    ar1 = np.array([0,1,1,0,1,0,2,1,0,1,0,1,0,0,1,0,1,1,0,1,0,1,0,1])  #  ,1,1,0,0,1,0,1,1,1,0,0,1,0,1,0
    print(routine, np.linalg.norm(ar1-routine))
    return np.linalg.norm(ar1-routine)
    # num_points, = routine.shape
    # return sum([distance_matrix[routine[i % num_points], routine[(i + 1) % num_points]] for i in range(num_points)])


# %% do GA


def createPopulation(self):
    # create the population
    print(self.size_pop, self.len_chrom)
    tmp = np.random.randint(0,2,[self.size_pop, self.len_chrom])
    self.Chrom = tmp
    print(self.Chrom)
    return self.Chrom
from tcas_sko.GA import GA_TSP

ga_tsp = GA_TSP(func=cal_total_distance, n_dim=num_points, crtp=createPopulation,size_pop=40, max_iter=100, prob_mut=0.5)
best_points, best_distance = ga_tsp.run()

print(best_points,best_distance)


# x_data = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
# print(ga_tsp.generation_best_X)
y_data = ga_tsp.generation_best_Y
x_data = np.linspace(1,len(y_data),len(y_data))


(
    Line()
    .set_global_opts(
        tooltip_opts=opts.TooltipOpts(is_show=False),
        xaxis_opts=opts.AxisOpts(type_="category"),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
    )
    .add_xaxis(xaxis_data=x_data)
    .add_yaxis(
        series_name="",
        y_axis=y_data,
        symbol="emptyCircle",
        is_symbol_show=True,
        label_opts=opts.LabelOpts(is_show=False),
    )
    .render(,"results.html")
)


# %% plot
# fig, ax = plt.subplots(1, 2)
# best_points_ = np.concatenate([best_points, [best_points[0]]])
# best_points_coordinate = points_coordinate[best_points_, :]
# ax[0].plot(best_points_coordinate[:, 0], best_points_coordinate[:, 1], 'o-r')
# ax[1].plot(ga_tsp.generation_best_Y)
# plt.show()