import module.config as ini ## https://wiki.python.org/moin/ConfigParserExamples
import module.decision as dec
import module.getOptions as opt
import module.tools as tls
import module.netTool as ntt
import module.freyr.csvBuffer as bfr
import module.read.pi as rpi
import os

print "CPU TMP", tls.mean([rpi.getCPUtemperature(), rpi.get_cpu_temperature()])
print "CPU %", rpi.cpu_percent()
print "NOW", tls.now()
print "UTC", tls.utcnow() 
