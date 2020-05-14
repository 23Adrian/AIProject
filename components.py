import main
import math


def _trafficComponent(traffic):
    # no traffic
    if traffic == 0:
        return 0
    # little traffic
    if traffic == 1:
        return 20
    # light traffic
    if traffic == 2:
        return 30
    # medium traffic
    if traffic == 3:
        return 60
    # big traffic
    if traffic == 4:
        return 120
    # heavy traffic
    return 200


# heuristic based on speed limit
def _speedComponent(speed, distance):
    # 60mph base case
    if speed == 0:
        return 0
    # 30mph
    if speed == 1:
        return distance * 2
    # 15mph
    if speed == 2:
        return distance * 4
    # 45mph
    if speed == 3:
        return int(distance * 1.333)
    # 75mph
    return int(distance * .80)


def _accidentComponent(accident):
    # no accident
    if accident == 0:
        return 0
    return 50


def componentAdjustments(rand, distance):
    return _trafficComponent(rand.randint(0, 5)) + \
            _speedComponent(rand.randint(0, 4), distance) + \
            _accidentComponent(rand.randint(0, 1))


def heuristicFunction(current, goal):
    x1, y1 = (main.romania_map.locations.get(current))

    x2, y2 = (main.romania_map.locations.get(goal))

    x = int(x2) - int(x1)
    y = int(y2) - int(y1)
    return int(math.sqrt((x ** 2) + (y ** 2)))