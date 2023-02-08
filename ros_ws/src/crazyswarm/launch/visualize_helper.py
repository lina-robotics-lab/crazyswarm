import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
from scripts.uav_trajectory import Trajectory

traj1 = Trajectory()
traj1.loadcsv('../scripts/circle0.csv')
df = pd.read_csv('../scripts/circle0.csv')
# # plt.ion()
fig, ax = plt.subplots()
for i in range(5):
    t = np.linspace(0, df.iloc[i, 0],100)
    poly_x = traj1.polynomials[i].px.p
    poly_y = traj1.polynomials[i].py.p
    waypoints_x = np.zeros_like(t)
    waypoints_y = np.zeros_like(t)
    for j in range(8):
        waypoints_x = waypoints_x + poly_x[j] * t ** j
        waypoints_y = waypoints_y + poly_y[j] * t ** j
    # for i in range(7):
    #     ax.plot(df['x^{}'.format(i)].values, df['y^{}'.format(i)].values)
    ax.scatter(waypoints_x, waypoints_y)

plt.show()