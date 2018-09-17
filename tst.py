import module.config as ini ## https://wiki.python.org/moin/ConfigParserExamples
import module.decision as dec
import module.getOptions as opt
import module.timeTools as ttl
import module.netTools as ntt
import module.freyr.csvBuffer as bfr
from module.freyr import findConfig
from module import *
import glob, math
## import os

# csv_name = sys.argv[1]
refference = "Sys"
## reading 'freyr_config.ini'

## configFile = "freyr_config_cp.ini"
configFile = "freyr_config_cp.ini" ## tst
config = ini.getConfig(configFile)

print(findConfig(confSection = refference, confOption = 'offline_counter', confFile = config))
ini.writeConfig(section = refference, option = 'offline_counter', value = 999, iniFile = configFile, iniConfig = config)
print(findConfig(confSection = refference, confOption = 'offline_counter', confFile = config))
