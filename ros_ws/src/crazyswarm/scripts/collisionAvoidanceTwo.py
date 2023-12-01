#!/usr/bin/env python

import numpy as np
from pycrazyswarm.crazyswarm_py import Crazyswarm 

Z = 0.8  # Takeoff altitude.

def main():
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs
    cfs =  allcfs.crazyflies

    swarm.allcfs
    cf_one = cfs[0]
    cf_two = cfs[1]

    cf_one.enableCollisionAvoidance([cf_two], np.array([0.2, 0.2, 0.4]))
    cf_two.enableCollisionAvoidance([cf_one], np.array([0.2, 0.2, 0.4]))

    allcfs.takeoff(targetHeight=Z, duration=2.0)

    timeHelper.sleep(4)
    
    cf_one.goTo(cf_two.position(), 0, 6)
    cf_two.goTo(cf_one.position(), 0, 6)

    timeHelper.sleep(7)

    cf_one.goTo(cf_two.position(), 0, 6)
    cf_two.goTo(cf_one.position(), 0, 6)

    timeHelper.sleep(7)

    allcfs.land(targetHeight=0.06, duration=2.0)

    timeHelper.sleep(3)


if __name__ == "__main__":
    main()