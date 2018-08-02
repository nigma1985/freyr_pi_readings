import module.config as ini ## https://wiki.python.org/moin/ConfigParserExamples
import module.decision as dec
import module.getOptions as opt
from module.tools import mean
import module.timeTool as ttl
import module.netTool as ntt
import module.freyr.csvBuffer as bfr
#import module.read.pi as rpi
import os, sys, time

bfr.csvName(user = byangoma, options = sys.argv)
