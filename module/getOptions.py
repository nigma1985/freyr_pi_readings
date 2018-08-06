import sys, re

def checkArgv(_input, _str):
    if _input is None:
        _input = sys.argv
    if type(_input) == str:
        if re.search(_str, _input):
            return True
        else:
            return False
    else:
        return False
    return False

def findItm(item = "", options = sys.argv, mode = None):
    ## find item in list and return "True" if found. Otherwise "False"
    if mode is None:
        ## default is strict and basic
        return item in options
    else:
        ## otherwise the more open approach of checkArgv is chosen
        ## items will also be found if it is a substrings
        if type(options) == list:
           for o in options:
               if checkArgv(o, item):
                  return True
        else:
           if checkArgv(options, item):
               return True
    return False

def getItm(item = "", options = sys.argv):
    ## find item as substring in list and return string
    if type(options) == list:
       for o in options:
           if checkArgv(o, item):
              return o
    else:
       if checkArgv(options, item):
           return options
    return None
