import module.config as ini ## https://wiki.python.org/moin/ConfigParserExamples
import module.decision as dec
import module.getOptions as opt
import module.tools as tls
import module.netTool as ntt
import module.freyr.csvBuffer as bfr
import module.read.pi as rpi
import os

import time

now1 = tls.now()
utc1 = tls.utcnow()
#nowsecs = tls.mktime(now1.timetuple())
nowsecs = time.mktime(now1.timetuple())

cpu_tempA = rpi.getCPUtemperature()
print "CPU %", rpi.cpu_percent()

ram = rpi.virtual_memory()
print "RAM", ram.total / 2**20       # MiB.
print "RAM%", ram.percent

disk = rpi.disk_usage('/')
print "Disk", disk.total / 2**30     # GiB.
print "Disk%", disk.percent

cpu_tempB = rpi.get_cpu_temperature()
print "CPU TMP", mean([float(cpu_tempA), cpu_tempB])

utc2 = tls.utcnow()
offset_utc = str(tls.roundTime(now1,roundTo=30*60) - tls.roundTime(utc1,roundTo=30*60))
duration = (utc2-utc1)
duration2 = (float(duration.microseconds) / 10**6) + duration.seconds + (((duration.days * 24) * 60) * 60)
