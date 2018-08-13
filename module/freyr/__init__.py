import sys, re
from module.config import ConfigSectionMapAdv
import module.getOptions as opt
from module import cleanType

def findConfig(sysOptions = sys.argv, sysKey = None, readVar = None, confSection = None, confOption = None, confFile = None):
    ## looks for options handed over by sys.argv and returns it
    buffer = None
    if sysKey is not None:
        buffer = opt.getItm(item = (sysKey + "="), options = sysOptions)
    if buffer is not None:
        buffer = buffer[-(len(buffer)-(len(sysKey)+1)):]
        return cleanType(buffer)
    elif readVar is not None:
        ## if no argument has been passed a value from the script can be passed
        return cleanType(readVar)
    else:
        ## if no argument or value has been passed, the config.ini is read
        buffer = ConfigSectionMapAdv(section = confSection, option = confOption, iniConfig = confFile)
        return cleanType(buffer)
