import sys, re

def checkArgv(_input, _str):
    if _input is None:
        _input = sys.argv
    if type(_input) == str:
        if re.search(_str, _input): # if re.search("out/FREYR_20*-*-*_*_" + u + ".csv", x):
            return True
        else:
            return False
    else:
        return False
    return False

def csvName(options = sys.argv, user = me):
   if type(options) == list:
       for opt in options:
           if checkArgv(opt, "^(out\/FREYR\_20..-..-..\_....\_" + user + "\.csv)"):
              return opt
   else:
       if checkArgv(options, "^(out\/FREYR\_20..-..-..\_....\_" + user + "\.csv)"):
           return options
   return "out/FREYR_YYYY-MM-DD_HHMM_" + user + ".csv"

def findItm(options = sys.argv, item = ""):
   if type(options) == list:
       for opt in options:
           if checkArgv(opt, item):
              return True
   else:
       if checkArgv(options, item):
           return True
   return False
