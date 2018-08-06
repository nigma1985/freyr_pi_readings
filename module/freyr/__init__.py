import sys, re
from module.config import ConfigSectionMapAdv
import module.getOptions as opt
from module import cleanType

def findConfig(sysOptions = sys.argv, sysKey = None, readVar = None, confSection = None, confOption = None, confFile = None):
    ## looks for options handed over by sys.argv and returns it
    sysConfig = None
    if sysKey is not None:
        sysConfig = opt.getItm(item = (sysKey + "="), options = sysOptions)
    if sysConfig is not None:
        sysConfig = sysConfig[-(len(sysConfig)-(len(sysKey)+1)):]
        return cleanType(sysConfig)
    elif readVar is not None:
        return readVar
    ## if no argument has been passed, the config.ini is read
    else:
        return ConfigSectionMapAdv(section = confSection, option = confOption, iniConfig = confFile)
