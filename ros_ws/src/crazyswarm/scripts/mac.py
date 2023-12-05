import numpy as np
import yaml
import pandas as pd
from pycrazyswarm import *

TAKEOFF_DURATION = 2.5

def grid(world_shape, step_size, start_loc):
    """
    Creates grids of coordinates and indices of state space
    Parameters
    ----------
    world_shape: tuple
        Size of the grid world (rows, columns)
    step_size: tuple
        Phyiscal step size in the grid world
    Returns
    -------
    states_ind: np.array
        (n*m) x 2 array containing the indices of the states
    states_coord: np.array
        (n*m) x 2 array containing the coordinates of the states
    """
    nodes = np.arange(0, world_shape["x"] * world_shape["y"])
    return nodes_to_states(nodes, world_shape, step_size) + start_loc


def nodes_to_states(nodes, world_shape, step_size):
    """Convert node numbers to physical states.
    Parameters
    ----------
    nodes: np.array
        Node indices of the grid world
    world_shape: tuple
        The size of the grid_world
    step_size: np.array
        The step size of the grid world
    Returns
    -------
    states: np.array
        The states in physical coordinates
    """
    # nodes = torch.as_tensor(nodes)
    # step_size = torch.as_tensor(step_size)
    return (
        np.vstack(
            ((nodes // world_shape["y"]), (nodes % world_shape["y"]))).T
        * step_size
    )

def replay_trajectory(agent_num = 3):
    with open("/home/mht/csw_ws/crazyswarm/ros_ws/src/crazyswarm/traj_data/real_base_double/params.yaml") as file:
        env_params = yaml.load(file, Loader=yaml.FullLoader)["env"]
    grid_V = grid(
            env_params["shape"], env_params["step_size"], np.array([env_params["start"]["x"], env_params["start"]["y"]])
        )
    traj_data = pd.read_csv('/home/mht/csw_ws/crazyswarm/ros_ws/src/crazyswarm/traj_data/real_base_double/data.csv')
    stop_iter = 10

    # take off
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs
    take_off_height = [0.4, 0.6, 0.8] # fix different height for taking off
    for i, cf in enumerate(allcfs.crazyflies):
        cf.takeoff(take_off_height[i], TAKEOFF_DURATION)
    timeHelper.sleep(TAKEOFF_DURATION + 1.0)

    for step in range(stop_iter):
        current_step_data = traj_data[traj_data["iter"] == step]
        # if step == 0:
        #     target_loc_3d = np.append(target_loc, take_off_height[i])
        for i in range(agent_num):
            key = 'idx_agent{}'.format(str(i))
            idx = current_step_data[key].values
            # print(idx, type(idx))
            target_loc = grid_V[idx[0]]
            print(key, idx, target_loc)
            target_loc_3d = np.append(target_loc, take_off_height[i])
            print(target_loc_3d)
            t = 5.0 if step == 0 else 1.0
            allcfs.crazyflies[i].goTo(target_loc_3d, 0, t)
        timeHelper.sleep(t + 0.5)

    allcfs.land(targetHeight= 0.04, duration=2.5)
        


if __name__ == "__main__":
    replay_trajectory(agent_num=1)