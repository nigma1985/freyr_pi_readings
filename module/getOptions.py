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

def findItm(item = "", options = sys.argv):
   if type(options) == list:
       for opt in options:
           if checkArgv(opt, item):
              return True
   else:
       if checkArgv(options, item):
           return True
   return False
