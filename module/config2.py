#!/usr/bin/python

# This script delivers functions to read and write ini-configurations

import ConfigParser ## https://wiki.python.org/moin/ConfigParserExamples
import re, os


## reading 'freyr_config.ini'
def getConfig(iniFile = "freyr_config.ini"):
    cnfg = ConfigParser.SafeConfigParser()
    return cnfg.read(iniFile)

## basic reading of lines
def ConfigSectionMap(_section = 'defaults', _ini = None):
     dict1 = {}
     if _ini is None:
        return dict1
     options = _ini.options(_section)
     for option in options:
         try:
             dict1[option] = _ini.get(_section, option)
             if dict1[option] == -1:
                 DebugPrint("skip: %s" % option)
         except:
             print("exception on %s!" % option)
             dict1[option] = None
     return dict1

## advanced reading of lines
## turning result into format included
def ConfigSectionMapAdv(section = 'defaults', option = None, ini = None):
     dict1 = {}
     if option is None or ini is None:
         return dict1
     try:
          dict2 = {}
          options = ini.options(section)
          for option in options:
              try:
                  dict2[option] = ini.get(section, option)
                  if dict2[option] == -1:
                      DebugPrint("skip: %s" % option)
              except:
                  print("exception on %s!" % option)
                  dict2[option] = None
          dict1 = dict2
     except:
          dict2 = {}
          options = ini.options('defaults')
          for option in options:
              try:
                  dict2[option] = ini.get('defaults', option)
                  if dict2[option] == -1:
                      DebugPrint("skip: %s" % option)
              except:
                  print("exception on %s!" % option)
                  dict2[option] = None
          dict1 = dict2
     if dict1 == 'None' or dict1 == '':
         dict1 = None
     else:
         try:
             dict1 = int(dict1)
         except:
             try:
                 dict1 = float(dict1)
             except:
                 dict1 = str(dict1)
     if isinstance(dict1, str):
         if dict1[:3] == "u'\\" or dict1[:3] == 'u"\\':
             ## find unicode and make into uni-string
             x = re.search(r"u[\"|\'](\\.+)[\"|\']", dict1)
             x = x.group(1)
             dict1 = x.decode('unicode-escape')
     return dict1

#os.chdir("C:/Users/Konrad/Documents/GitHub/fryer_pi_readings/")

#tstini = "freyr_config.ini"
#tstconfig = ConfigParser.SafeConfigParser()
#print tstconfig.read(tstini)

#tstini = config('freyr_config.ini')
#print os.path.isfile("freyr_config.ini")
#print ConfigSectionMapAdv(section = 'defaults', option = 'source_name', ini = tstconfig)
