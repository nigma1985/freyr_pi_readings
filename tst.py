#!/usr/bin/python3

import re
## from module import *
## import module.netTools as ntt
## from module.read.pi import *
import module.config as ini ## https://wiki.python.org/moin/ConfigParserExamples
from module.freyr import findConfig
from module import *

## y = "u'Icb bin der \\u2103. Mein Name ist \\u2103 ich weiß von nix.'"
configFile = "freyr_config.ini"
config = ini.getConfig(configFile)

def cleanUnicodeX(var = None):
    print("start")
    if var is not None and isinstance(var, str):
        print("step1")
        if re.search(r"^u[\"|\'](.*?)[\"|\']$", var):
            print("step2")
            mirror = None
            pic = var
            while mirror != pic:
                mirror = pic
                try:
                    print("try")
                    exec("pic = bytes(" + pic[2:-1] + ").decode('utf-8')")
                    print("exec:", var, mirror, pic)
                except:
                    print("except", pic)
            var = pic
    print("end")
    return(var)

## x = findConfig(sysKey = "cpu_temp_measure_sign", confSection = 'tmp_celsius', confOption = 'measure_sign', confFile = config)
## x = "u'\\u2103'"
x = "u'Ich bin der \\u2103, mein Name ist \\u2301!'"

#exec("y = " + x)
#print(x, y)

print("x = ", x)
print("clean x = ", cleanUnicode(x))

##exec("a = bytes('" + x[2:-1] + "').decode('utf-8')")
##print(a)

exec("z = " + x)
print(x, z)

# print(y, cleanUnicode(y))
print(x[2:-1])

print("_____")

print(cleanUnicode(var = x))
