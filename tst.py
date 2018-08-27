#!/usr/bin/python3

## from module import *
## import module.netTools as ntt
## from module.read.pi import *
## import module.config as ini ## https://wiki.python.org/moin/ConfigParserExamples
## from module.freyr import findConfig
from module import cleanUnicode

y = "u'Icb bin der \\u2103. Mein Name ist \\u2103 ich weiß von nix.'"
# configFile = "freyr_config.ini"
# config = ini.getConfig(configFile)

# x = findConfig(sysKey = "cpu_temp_measure_sign", confSection = 'tmp_celsius', confOption = 'measure_sign', confFile = config)

# print(x)

# print(y, cleanUnicode(y))

print
a = 2103
b = str(a)
c = "\\"
d = "u"
print(a, b, c, d)

x = d + c + b
z = c + b

print(x, z)

#print(y, bytes(y), bytes(y).decode('utf-8', "replace"))
print("first", y)
## y = eval(y[2:8])
## exec("y = " + y[2:8].encode('utf-8').decode('ascii'))
try:
    exec("u = " + y)
except:
    exec("u = '" + y + "'")

print("second", u, x, y, z)
##exec("y = " + y)
##print("thrid", y)
