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


def start():
    return 1, 2, 3

def end(x, y, z):
    return x + 1, y * 2, z ** 3

a, b, c = start()

print a, b, c

aa, bb, cc = end(a, b, c)

print aa, bb, cc
