import sys, re
from os.path import isfile
from module.config import ConfigSectionMapAdv
import module.freyr.csvBuffer as head
import unicodecsv as csv

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

def csvName(user = None, options = sys.argv):
   if user is None:
       user = ConfigSectionMapAdv(option = 'source_name')
   file = None
   if type(options) == list:
       for opt in options:
           if checkArgv(opt, "^(out\/FREYR\_20..-..-..\_....\_" + user + "\.csv)"):
              file = opt
   else:
       if checkArgv(options, "^(out\/FREYR\_20..-..-..\_....\_" + user + "\.csv)"):
           file = options
   file = "out/FREYR_YYYY-MM-DD_HHMM_" + user + ".csv"
   initiateFile(file)
       ###################################
   return file

def findItm(item = "", options = sys.argv):
   if type(options) == list:
       for opt in options:
           if checkArgv(opt, item):
              return True
   else:
       if checkArgv(options, item):
           return True
   return False

def initiateFile(x = None):
    if x is None:
        raise "ERROR: No file!"
    elif not isfile(x):
        with open(x, 'ab') as csvfile:
           y = csv.writer(csvfile, delimiter='|', quoting=csv.QUOTE_NONNUMERIC)
           y.writerow(head.headLine())
    return
