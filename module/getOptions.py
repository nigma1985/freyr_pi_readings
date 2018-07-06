import ConfigSectionMapAdv from config
import sys
import re

def _tstfile(_input, _str):
    if type(_input) == str:
        if re.search(_str, _input): # if re.search("out/FREYR_20*-*-*_*_" + u + ".csv", x):
            return True
        else:
            return False
    else:
        return False
    return False

def _csvName(options = sys.argv, user = ConfigSectionMapAdv("Sys",'source_name')):
   if type(options) == list:
       for opt in options:
           if _tstfile(opt, "^(out\/FREYR\_20..-..-..\_....\_" + user + "\.csv)"):
              return opt
   else:
       if _tstfile(options, "^(out\/FREYR\_20..-..-..\_....\_" + user + "\.csv)"):
           return options
   return "out/FREYR_YYYY-MM-DD_HHMM_" + user + ".csv"

def _findItm(options = sys.argv, item = ""):
   if type(options) == list:
       for opt in options:
           if _tstfile(opt, item):
              return True
   else:
       if _tstfile(options, item):
           return True
   return False

csv_name = _csvName(_input, ConfigSectionMapAdv("Sys",'source_name'))

all_on = _findItm(_input, "ALLON")
all_off = _findItm(_input, "ALLOFF")
