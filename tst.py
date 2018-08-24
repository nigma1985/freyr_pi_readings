from module import *
import module.netTools as ntt
from module.read.pi import *
from module.freyr import findConfig

configFile = "freyr_config.ini"
config = ini.getConfig(configFile)

x = findConfig(sysKey = "cpu_temp_measure_sign", confSection = 'tmp_celsius', confOption = 'measure_sign', confFile = config)

print(x)
