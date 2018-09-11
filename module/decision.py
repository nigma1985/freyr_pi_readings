from random import random
from module.getOptions import findItm
from module import cleanType

def decision(onSwitch = None, offSwitch = None, numChance = None, numInterval = None, capChance = None, capInterval = None):
    print(onSwitch, type(onSwitch))
    print(offSwitch, type(offSwitch))
    print(numChance, type(numChance))
    print(numInterval, type(numInterval))
    print(capChance, type(capChance))
    print(capInterval, type(capInterval))

    if onSwitch is None:
        onSwitch = ["ALLON"]
    if offSwitch is None:
        offSwitch = ["ALLOFF"]

    def _item(i):
        # if bool, take as is
        # if str use getOptions
        # if None then None
        if (type(i) == bool) or (i is None):
            return i
        elif type(i) == str:
            return findItm(item = i)
        else:
            return None

    def _list(_input):
        items = []

        # if list then
        ## for all items in list check items
        ## otherwise check single item
        if type(_input) == list:
            for _in in _input:
                items.append(_item(i = _in))
        else:
            items.append(_item(_input))

        return items

    on = _list(_input = onSwitch)
    off = _list(_input = offSwitch)

    if capChance is None:
        capChance = 0
    if capInterval is None:
        capInterval = 60

    if any(off):
        print("OFF")
        return False
    elif any(on):
        print("ON")
        return True
    elif (numInterval is not None) and (numChance is not None):
        print("capped Chance/Interval")
        return any((random() <= 1 / (numChance - capChance)), (numInterval < capInterval))
    elif numInterval is not None:
        print("capped Interval")
        return numInterval < capInterval
    elif (numChance is None) or (numChance - capChance == 0):
        print("no chance")
        return True
    else:
        print("random", random(), 1 / (numChance - capChance))
        random() <= 1 / (numChance - capChance)
