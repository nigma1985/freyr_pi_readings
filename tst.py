import module.config as ini ## https://wiki.python.org/moin/ConfigParserExamples
import module.decision as dec
import module.getOptions as opt
from module.tools import mean
import module.timeTool as ttl
import module.netTool as ntt
import module.freyr.csvBuffer as bfr
#import module.read.pi as rpi
import os

import time
#
# now1 = ttl.now()
# utc1 = ttl.utcnow()
# nowsecs = ttl.mktime(now1)
# #nowsecs = time.mktime(now1.timetuple())
#
# # cpu_tempA = rpi.getCPUtemperature()
# # print "CPU %", rpi.cpu_percent()
# #
# # ram = rpi.virtual_memory()
# # print "RAM", ram.total / 2**20       # MiB.
# # print "RAM%", ram.percent
# #
# # disk = rpi.disk_usage('/')
# # print "Disk", disk.total / 2**30     # GiB.
# # print "Disk%", disk.percent
# #
# # cpu_tempB = rpi.get_cpu_temperature()
# # print "CPU TMP", mean([float(cpu_tempA), cpu_tempB])
#
# utc2 = ttl.utcnow()
# print "OffSet", str(ttl.roundTime(now1,roundTo=30*60) - ttl.roundTime(utc1,roundTo=30*60))
# duration = (utc2-utc1)
# print "duration", (float(duration.microseconds) / 10**6) + duration.seconds + (((duration.days * 24) * 60) * 60)

print bfr.writeRow()
