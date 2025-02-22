from HashMap import *
from Packages import *
from Truck import *
from csvreader import *
truck1 = Truck(0, [1, 2, 3], '', '',   0, True)
print(truck1)
### Package Requirements ###
'''
Package 1: Deadline: 10:30am
Package 3: Must be on truck 2
Package 6: Delayed on flight: wll not arrive to depot until 905 am (will need to have a truck leave at 905) | Deadline: 1030am
Package 9: Wrong address (get the time it changes from requirements, cant deliver til fixed)
Package 13: Deadline: 10:30am
Package 14: Must be delivered with package 15 and 19 | Deadline: 10:30am
Package 15: Deadline: 9:00am
Package 16: Must be delivered with package 13 and 19 | Deadline: 10:30am
Package 18: Must be on truck 2
Package 20: Must be delivered with package 13 and 15 | Deadline: 10:30am
Package 25: Delayed on flight: will not arrive to depot until 905 am (load on same truck as package 6) | Deadline: 10:30am
Package 28: Delayed on flight: will not arrive to depot until 905 am (load on same truck as packages 6 and 25)
Package 29: Deadline: 10:30am
Package 30: Deadline: 10:30am
Package 31: Deadline: 10:30am
Package 32: Delayed on flight: will not arrive to depot until 905 am (load on same truck as packages 6, 25, and 28)
Package 34: Deadline: 10:30am
Package 36: Must be on truck 2
Package 37: Deadline: 10:30am
Package 38: Must be on truck 2
Package 40: Deadline: 10:30am
'''