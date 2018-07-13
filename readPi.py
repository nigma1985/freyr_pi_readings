#!/usr/bin/python

# This script develops a python script to read and write envirophat data
# -*- coding: utf-8 -*-
from __future__ import division
from envirophat import light, motion, weather, analog, leds

#from subprocess import PIPE, Popen
import subprocess, platform
import psutil ## install python-psutil
import sys
#import Adafruit_DHT
#import datetime
from datetime import datetime
from datetime import timedelta
import time
import re
import sqlite3 as lite
#import csv
import unicodecsv as csv
from random import *
# import ConfigParser ## https://wiki.python.org/moin/ConfigParserExamples
import glob
import shutil
#import pyping
import math

################################################################################

import module.config as ini ## https://wiki.python.org/moin/ConfigParserExamples
import os

refference = "Sys"

## reading 'freyr_config.ini'
configFile = "freyr_config.ini"
config = ini.getConfig(configFile)
# ini.ConfigSectionMapAdv(section = 'defaults', option = 'source_name', iniConfig = config)


#################################################
#################################################

def roundTime(dt=None, roundTo=60):
   """Round a datetime object to any time laps in seconds
   dt : datetime object, default now.
   roundTo : Closest number of seconds to round to, default 1 minute.
   Author: Thierry Husson 2012 - Use it as you want but don't blame me.
   """
   if dt == None : dt = datetime.now()
   seconds = (dt - dt.min).seconds
   # // is a floor division, not a comment on following line:
   rounding = (seconds+roundTo/2) // roundTo * roundTo
   return dt + timedelta(0,rounding-seconds,-dt.microsecond)

#################################################
#################################################

# Return CPU temperature as a character string
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

def get_cpu_temperature():
    process = subprocess.Popen(['vcgencmd', 'measure_temp'], stdout=subprocess.PIPE)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])

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

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

me = ini.ConfigSectionMapAdv(section = refference, option = 'source_name', iniConfig = config)
my_user = ini.ConfigSectionMapAdv(section = refference, option = 'user', iniConfig = config)

# print me, my_user
# sys.exit(0)

def _tstfile(_input, _str):
    if type(_input) == str:
        if re.search(_str, _input): # if re.search("out/FREYR_20*-*-*_*_" + u + ".csv", x):
            return True
        else:
            return False
    else:
        return False
    return False

def _csvName(options = sys.argv, user = me):
   if type(options) == list:
       for opt in options:
           if _tstfile(opt, "^(out\/FREYR\_20..-..-..\_....\_" + user + "\.csv)"):
              return opt
   else:
       if _tstfile(options, "^(out\/FREYR\_20..-..-..\_....\_" + user + "\.csv)"):
           return options
   return "out/FREYR_YYYY-MM-DD_HHMM_" + user + ".csv"

def _findItm(options = sys.argv, item = ""):
   if type(options) == list:
       for opt in options:
           if _tstfile(opt, item):
              return True
   else:
       if _tstfile(options, item):
           return True
   return False

_input = sys.argv

csv_name = _csvName(_input, me)

all_on = _findItm(_input, "ALLON")
all_off = _findItm(_input, "ALLOFF")

# sensor = Adafruit_DHT.DHT22
# pin = ConfigSectionMap(refference)['pin']

# Try to grab a sensor reading.  Use the read_retry method which will retry up
now1 = datetime.now()
utc1 = datetime.utcnow()
nowsecs = time.mktime(now1.timetuple())
ram_time = nowsecs % (1.001 * (60 * 3))
ram_time_percent = nowsecs % (0.999 * (60 * 12))
disk_time = nowsecs % (1.001 * (60 * 60 * 12))
disk_time_percent = nowsecs % (0.999 * (60 * 60 * 24 * 7))
cpu_tempA = getCPUtemperature()
cpu_use = None
if (_findItm(_input, "CPUUSEOFF") or all_off):
    print "CPU use off"
elif (_findItm(_input, "CPUUSEON") or all_on):
    cpu_use = psutil.cpu_percent()
    print "CPU use on"
else:
    cpu_use = psutil.cpu_percent()

ram = psutil.virtual_memory()
ram_total = None
ram_used = None
ram_free = None
ram_percent_used = None
if (_findItm(_input, "RAMBITOFF") or all_off):
    print "RAM use in bits off"
elif (_findItm(_input, "RAMBITON") or all_on):
    ram_total = ram.total / 2**20       # MiB.
    ram_used = ram.used / 2**20
    ram_free = ram.free / 2**20
    print "RAM use in bit on"
elif (ram_time <= 60) or (cpu_use > 80.0) or (cpu_tempA > 57.5):
    ram_total = ram.total / 2**20       # MiB.
    ram_used = ram.used / 2**20
    ram_free = ram.free / 2**20

if (_findItm(_input, "RAMUSEOFF") or all_off):
    print "RAM use in % off"
elif (_findItm(_input, "RAMUSEON") or all_on):
    ram_percent_used = ram.percent
    print "RAM use in % on"
elif ram_time_percent <= 60:
    ram_percent_used = ram.percent

disk = psutil.disk_usage('/')
disk_total = None
disk_used = None
disk_remaining = None
disk_percentage = None
if (_findItm(_input, "DSKBITOFF") or all_off):
    print "Disk use in bits off"
elif (_findItm(_input, "DSKBITON") or all_on):
    disk_total = disk.total / 2**30     # GiB.
    disk_used = disk.used / 2**30
    disk_remaining = disk.free / 2**30
    print "Disk use in bit on"
elif disk_time <= 60:
    disk_total = disk.total / 2**30     # GiB.
    disk_used = disk.used / 2**30
    disk_remaining = disk.free / 2**30

if (_findItm(_input, "DSKUSEOFF") or all_off):
    print "Disk use in % off"
elif (_findItm(_input, "DSKUSEON") or all_on):
    disk_percentage = disk.percent
    print "Disk use in % on"
elif disk_time_percent <= 60:
    disk_percentage = disk.percent

cpu_tempB = get_cpu_temperature()
cpu_temp = None
if (_findItm(_input, "CPUTMPOFF") or all_off):
    print "CPU Temp off"
elif (_findItm(_input, "CPUTMPON") or all_on):
    cpu_temp = mean([float(cpu_tempA), cpu_tempB])
    print "CPU Temp on"
else:
    cpu_temp = mean([float(cpu_tempA), cpu_tempB])

utc2 = datetime.utcnow()
offset_utc = str(roundTime(now1,roundTo=30*60) - roundTime(utc1,roundTo=30*60))
duration = (utc2-utc1)
duration2 = (float(duration.microseconds) / 10**6) + duration.seconds + (((duration.days * 24) * 60) * 60)

def std_line(
    value = 0.0,
    pin = None,
    # time
    utc_1 = utc1,
    utc_2 = utc2,
    offsetutc = offset_utc,
    duration_sec = duration2,
    # location
    outdoors_name = ConfigSectionMapAdv(refference,'outdoors_name'),  ##'no'  ## 'yes' 'none' 'other'
    loc_lat = float(ConfigSectionMapAdv(refference,'loc_lat')),  ##53.304130
    loc_long = float(ConfigSectionMapAdv(refference,'loc_long')),  ##9.706472
    loc_description = ConfigSectionMapAdv(refference,'loc_description'),  ##'test indoor'
    # source / provider
    provider_type = ConfigSectionMapAdv(refference,'provider_type'),  ##'RPi3'   ## 'REST API'
    source_name = ConfigSectionMapAdv(refference,'source_name'), ##'FreyrTST 1'
    source_description = ConfigSectionMapAdv(refference,'source_description'),  ##'Test RPi3 -
    # periphery
    periphery_name = ConfigSectionMapAdv(refference,'periphery_name'),  ##'Raspberry Pi 3'
    periphery_type = ConfigSectionMapAdv(refference,'periphery_type'),  ##'System'
    periphery_description = ConfigSectionMapAdv(refference,'periphery_description'),  ##'Hardware'
    periphery_device_description = ConfigSectionMapAdv(refference,'periphery_device_description'),  ##'tst'
    # measure
    measure_name = None,
    measure_sign = None,
    measure_type_full = None,
    measure_type_abbr = None,
    measure_absolute_min = None,
    measure_absolute_max = None,
    measure_target_type = None,
    measure_target_name = ConfigSectionMapAdv(refference,'measure_target_name'),  ##'System' ## 'yes' 'none' 'other'
    measure_target_description = ConfigSectionMapAdv(refference,'measure_target_description'),  ##'Monitoring Hardware'
    # QA
    data_quality = int(ConfigSectionMapAdv(refference,'data_quality'))  ##99
):
    return [value, pin, utc_1, utc_2, offsetutc, duration_sec,outdoors_name, loc_lat, loc_long, loc_description, provider_type, source_name, source_description, periphery_type, periphery_name, periphery_description, periphery_device_description, measure_name, measure_sign, measure_type_full, measure_type_abbr, measure_absolute_min, measure_absolute_max, measure_target_type, measure_target_name, measure_target_description, data_quality]

with open(csv_name, 'ab') as csvfile:
   tst = csv.writer(csvfile, delimiter='|', quoting=csv.QUOTE_NONNUMERIC)
   # print "cpu_temp"
   if cpu_temp is not None:
       cpu_temp_line = std_line(
           value = cpu_temp,
           # measure
           measure_name = ConfigSectionMapAdv('tmp_celsius','measure_name'),
           measure_sign = ConfigSectionMapAdv('tmp_celsius','measure_sign'),
           measure_type_full = ConfigSectionMapAdv('tmp_celsius','measure_type_full'),
           measure_type_abbr = ConfigSectionMapAdv('tmp_celsius','measure_type_abbr'),
           measure_absolute_min = float(ConfigSectionMapAdv('tmp_celsius','measure_absolute_min')),
           measure_absolute_max = None, #float(ConfigSectionMapAdv('tmp_celsius','measure_absolute_max')),
           measure_target_type = ConfigSectionMapAdv(refference,'cpu_measure_target_type'))
       tst.writerow(cpu_temp_line)
   # print "cpu_use"
   if cpu_use is not None:
       cpu_use_line = std_line(
           value = cpu_use,
           # measure
           measure_name = ConfigSectionMapAdv('percent_used','measure_name'),
           measure_sign = ConfigSectionMapAdv('percent_used','measure_sign'),
           measure_type_full = ConfigSectionMapAdv('percent_used','measure_type_full'),
           measure_type_abbr = ConfigSectionMapAdv('percent_used','measure_type_abbr'),
           measure_absolute_min = float(ConfigSectionMapAdv('percent_used','measure_absolute_min')),
           measure_absolute_max = float(ConfigSectionMapAdv('percent_used','measure_absolute_max')),
           measure_target_type = ConfigSectionMapAdv(refference,'cpu_measure_target_type'))
       tst.writerow(cpu_use_line)
   # print "disk_percentage"
   if disk_percentage is not None:
       disk_percentage_line = std_line(
           value = disk_percentage,
           # measure
           measure_name = ConfigSectionMapAdv('percent_used','measure_name'),
           measure_sign = ConfigSectionMapAdv('percent_used','measure_sign'),
           measure_type_full = ConfigSectionMapAdv('percent_used','measure_type_full'),
           measure_type_abbr = ConfigSectionMapAdv('percent_used','measure_type_abbr'),
           measure_absolute_min = float(ConfigSectionMapAdv('percent_used','measure_absolute_min')),
           measure_absolute_max = float(ConfigSectionMapAdv('percent_used','measure_absolute_max')),
           measure_target_type = ConfigSectionMapAdv(refference,'disk_measure_target_type'))
       tst.writerow(disk_percentage_line)
   # print "ram use"
   if ram_used is not None and ram_total is not None:
       ram_used_line = std_line(
           value = ram_used,
           # measure
           measure_name = ConfigSectionMapAdv('MegaByte','measure_name'),
           measure_sign = ConfigSectionMapAdv('MegaByte','measure_sign'),
           measure_type_full = ConfigSectionMapAdv(refference,'ram_measure_type_full'),
           measure_type_abbr = ConfigSectionMapAdv(refference,'ram_measure_type_abbr'),
           measure_absolute_min = float(ConfigSectionMapAdv('MegaByte','measure_absolute_min')),
           measure_absolute_max = ram_total,
           measure_target_type = ConfigSectionMapAdv(refference,'ram_measure_target_type'))
       tst.writerow(ram_used_line)
   # print "ram percent"
   if ram_percent_used is not None:
       ram_percent_used_line = std_line(
           value = ram_percent_used,
           # measure
           measure_name = ConfigSectionMapAdv('percent_used','measure_name'),
           measure_sign = ConfigSectionMapAdv('percent_used','measure_sign'),
           measure_type_full = ConfigSectionMapAdv('percent_used','measure_type_full'),
           measure_type_abbr = ConfigSectionMapAdv('percent_used','measure_type_abbr'),
           measure_absolute_min = float(ConfigSectionMapAdv('percent_used','measure_absolute_min')),
           measure_absolute_max = float(ConfigSectionMapAdv('percent_used','measure_absolute_max')),
           measure_target_type = ConfigSectionMapAdv(refference,'ram_measure_target_type'))
       tst.writerow(ram_percent_used_line)
   # print "disk use"
   if disk_used is not None and disk_total is not None:
       disk_used_line = std_line(
           value = disk_used,
           # measure
           measure_name = ConfigSectionMapAdv('GigaByte','measure_name'),
           measure_sign = ConfigSectionMapAdv('GigaByte','measure_sign'),
           measure_type_full = ConfigSectionMapAdv(refference,'disk_measure_type_full'),
           measure_type_abbr = ConfigSectionMapAdv(refference,'disk_measure_type_abbr'),
           measure_absolute_min = float(ConfigSectionMapAdv('GigaByte','measure_absolute_min')),
           measure_absolute_max = disk_total,
           measure_target_type = ConfigSectionMapAdv(refference,'disk_measure_target_type'))
       tst.writerow(disk_used_line)


# print "SCP"
def scp(file = "", user = "pi", host = me, path = "~/in/"):
    cmd = "scp {} {}@{}:{}".format(file, user, host, path)
    response = subprocess.call(cmd, shell=True)
    return response == 0

target_user = ConfigSectionMapAdv("Sys",'db_user')
mothership = ConfigSectionMapAdv("Sys",'db_host')
direc = ConfigSectionMapAdv("Sys",'db_path')

try:
    scp(file = csv_name, user = target_user, host = mothership, path = direc)
    #print "tst"
except:
    print "ERROR @ transfer"
