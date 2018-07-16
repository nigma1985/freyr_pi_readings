#!/usr/bin/python

# This script delivers functions to read and write ini-configurations

import ConfigParser ## https://wiki.python.org/moin/ConfigParserExamples
import re

## reading 'freyr_config.ini'
def config(iniFile = "freyr_config.ini"):
    ini = ConfigParser.SafeConfigParser()
    return ini.read(iniFile)

default = 'default'

## basic reading of lines
def ConfigSectionMap(section = 'default', ini = _config()):
     dict1 = {}
     options = ini.options(section)
     for option in options:
         try:
             dict1[option] = ini.get(section, option)
             if dict1[option] == -1:
                 DebugPrint("skip: %s" % option)
         except:
             print("exception on %s!" % option)
             dict1[option] = None
     return dict1

## advanced reading of lines
## turning result into format included
def ConfigSectionMapAdv(section = 'default', option = None, ini = _config()):
     dict1 = {}
     if option is None:
         return dict1
     try:
         dict1 = ConfigSectionMap(section)[option]
     except:
         dict1 = ConfigSectionMap("defaults")[option]
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
