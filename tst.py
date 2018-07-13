import module.config as ini
#from module.tst_module import eins
#from module.tst_module import zwei
#import module.config as tst

import os

config = ini.getConfig('freyr_config.ini')
#os.chdir("C:/Users/Konrad/Documents/GitHub/fryer_pi_readings/")

# tstconfig = ini.getConfig('freyr_config.ini')
# print ini.ConfigSectionMapAdv(section = 'default', option = 'source_name', ini = _ini)

# print ini.ConfigSectionMap(_ini = ini)

# print os.path.isfile("freyr_config.ini")

# print tst.ConfigSectionMap()

# print ini.ConfigSectionMapAdv()
# print ini.ConfigSectionMapAdv(section = 'defaults', option = 'source_name', iniConfig = tstconfig)

# print eins(a = 'my text')
# print zwei()

# print tstconfig.options()

print ini.ConfigSectionMapAdv(section = 'defaults', option = 'source_name', iniConfig = config)

# print ini.ConfigSectionMapAdv(section = 'defaults', option = 'source_name', iniFile = 'freyr_config.ini')
