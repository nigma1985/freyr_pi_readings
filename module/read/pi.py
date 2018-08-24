
import os
#from subprocess import PIPE, Popen
import subprocess #, platform
import psutil ## install python-psutil
from module import cleanType, cleanList
#import sys


# Return CPU temperature as a character string
def getCPUtemperature():
    buffer = os.popen('vcgencmd measure_temp').readline()
    buffer = buffer.replace("temp=","").replace("'C\n","")
    return(cleanList(string = buffer))

def get_cpu_temperature():
    process = subprocess.Popen(['vcgencmd', 'measure_temp'], stdout=subprocess.PIPE)
    output, _error = process.communicate()
    buffer = str(output)
    buffer = buffer[buffer.index('=') + 1:buffer.rindex("'")]
    return(cleanList(string = buffer))

# Return RAM information (unit=kb) in a list
# Index 0: total RAM
# Index 1: used RAM
# Index 2: free RAM
def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return(line.split()[1:4])

def cpu_percent():
    return(psutil.cpu_percent())

def virtual_memory():
    return(psutil.virtual_memory())

def disk_usage(x):
    return(psutil.disk_usage(x))
