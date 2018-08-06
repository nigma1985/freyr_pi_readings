# import module.config as ini ## https://wiki.python.org/moin/ConfigParserExamples
# import module.decision as dec
# import module.getOptions as opt
# from module.tools import mean
# import module.timeTools as ttl
# import module.netTool as ntt
# import module.freyr.csvBuffer as bfr
# import module.freyr as fry
# #import module.read.pi as rpi
# import os, sys, time
#
# bfr.csvName(user = "byangoma", options = sys.argv)



x = ["Konrad", None, "x", "10", "10.1", "123", "Konrad1.0", "1.Konrad", "None", "Ende"]

for i in x:
    print i, type(i)
    a = recode(i)
    print a, type(a)
