from module import *
import module.netTools as ntt
from module.read.pi import *

#str = "139.130.4.5,    ferienhauskeck.de,google.com,8.8.4.4  ,8.8.8.8,0.0.0.0, wikipedia.org ,heise.de,raspberrypi.org"
#print(ntt.ping_host(hosts = cleanList(string = str)))

x = getCPUtemperature()
print "getCPUtemperature", x, type(x)

x = get_cpu_temperature()
print "get_cpu_temperature", x, type(x)

x = getRAMinfo()
print "getRAMinfo", x, type(x)

x = cpu_percent()
print "cpu_percent", x, type(x)

x = virtual_memory()
print "virtual_memory", x, type(x)

x = disk_usage()
print "disk_usage", x, type(x)
