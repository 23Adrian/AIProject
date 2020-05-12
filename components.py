def trafficComponent(traffic):
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
def speedComponent(speed, distance):
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


def accidentComponent(accident):
    # no accident
    if accident == 0:
        return 0
    return 50


def tollsComponent(toll, avoidTolls):
    # has toll and the user want to avoid tolls
    if (toll == 1 and avoidTolls == True):
        return False
    return True