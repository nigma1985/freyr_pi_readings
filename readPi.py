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
import module.getOptions as opt
import module.freyr.csvBuffer as csv
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


####################
####################
####################
####################

csv_name = opt.csvName(_input, me)

all_on = opt.findItm(_input, "ALLON")
all_off = opt.findItm(_input, "ALLOFF")

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
if (opt.findItm(_input, "CPUUSEOFF") or all_off):
    print "CPU use off"
elif (opt.findItm(_input, "CPUUSEON") or all_on):
    cpu_use = psutil.cpu_percent()
    print "CPU use on"
else:
    cpu_use = psutil.cpu_percent()

ram = psutil.virtual_memory()
ram_total = None
ram_used = None
ram_free = None
ram_percent_used = None
if (opt.findItm(_input, "RAMBITOFF") or all_off):
    print "RAM use in bits off"
elif (opt.findItm(_input, "RAMBITON") or all_on):
    ram_total = ram.total / 2**20       # MiB.
    ram_used = ram.used / 2**20
    ram_free = ram.free / 2**20
    print "RAM use in bit on"
elif (ram_time <= 60) or (cpu_use > 80.0) or (cpu_tempA > 57.5):
    ram_total = ram.total / 2**20       # MiB.
    ram_used = ram.used / 2**20
    ram_free = ram.free / 2**20

if (opt.findItm(_input, "RAMUSEOFF") or all_off):
    print "RAM use in % off"
elif (opt.findItm(_input, "RAMUSEON") or all_on):
    ram_percent_used = ram.percent
    print "RAM use in % on"
elif ram_time_percent <= 60:
    ram_percent_used = ram.percent

disk = psutil.disk_usage('/')
disk_total = None
disk_used = None
disk_remaining = None
disk_percentage = None
if (opt.findItm(_input, "DSKBITOFF") or all_off):
    print "Disk use in bits off"
elif (opt.findItm(_input, "DSKBITON") or all_on):
    disk_total = disk.total / 2**30     # GiB.
    disk_used = disk.used / 2**30
    disk_remaining = disk.free / 2**30
    print "Disk use in bit on"
elif disk_time <= 60:
    disk_total = disk.total / 2**30     # GiB.
    disk_used = disk.used / 2**30
    disk_remaining = disk.free / 2**30

if (opt.findItm(_input, "DSKUSEOFF") or all_off):
    print "Disk use in % off"
elif (opt.findItm(_input, "DSKUSEON") or all_on):
    disk_percentage = disk.percent
    print "Disk use in % on"
elif disk_time_percent <= 60:
    disk_percentage = disk.percent

cpu_tempB = get_cpu_temperature()
cpu_temp = None
if (opt.findItm(_input, "CPUTMPOFF") or all_off):
    print "CPU Temp off"
elif (opt.findItm(_input, "CPUTMPON") or all_on):
    cpu_temp = mean([float(cpu_tempA), cpu_tempB])
    print "CPU Temp on"
else:
    cpu_temp = mean([float(cpu_tempA), cpu_tempB])

utc2 = datetime.utcnow()
offset_utc = str(roundTime(now1,roundTo=30*60) - roundTime(utc1,roundTo=30*60))
duration = (utc2-utc1)
duration2 = (float(duration.microseconds) / 10**6) + duration.seconds + (((duration.days * 24) * 60) * 60)

def _stdLine(
    value = 0.0,
    pin = None,
    # time
    utc_1 = utc1,
    utc_2 = utc2,
    offsetutc = offset_utc,
    duration_sec = duration2,
    # location
    outdoors_name = ini.ConfigSectionMapAdv(section = refference, option ='outdoors_name', iniConfig = config),  ##'no'  ## 'yes' 'none' 'other'
    loc_lat = float(ini.ConfigSectionMapAdv(section = refference, option ='loc_lat', iniConfig = config)),  ##53.304130
    loc_long = float(ini.ConfigSectionMapAdv(section = refference, option ='loc_long', iniConfig = config)),  ##9.706472
    loc_description = ini.ConfigSectionMapAdv(section = refference, option ='loc_description', iniConfig = config),  ##'test indoor'
    # source / provider
    provider_type = ini.ConfigSectionMapAdv(section = refference, option ='provider_type', iniConfig = config),  ##'RPi3'   ## 'REST API'
    source_name = ini.ConfigSectionMapAdv(section = refference, option ='source_name', iniConfig = config), ##'FreyrTST 1'
    source_description = ini.ConfigSectionMapAdv(section = refference, option ='source_description', iniConfig = config),  ##'Test RPi3 -
    # periphery
    periphery_name = ini.ConfigSectionMapAdv(section = refference, option ='periphery_name', iniConfig = config),  ##'Raspberry Pi 3'
    periphery_type = ini.ConfigSectionMapAdv(section = refference, option ='periphery_type', iniConfig = config),  ##'System'
    periphery_description = ini.ConfigSectionMapAdv(section = refference, option ='periphery_description', iniConfig = config),  ##'Hardware'
    periphery_device_description = ini.ConfigSectionMapAdv(section = refference, option ='periphery_device_description', iniConfig = config),  ##'tst'
    # measure
    measure_name = None,
    measure_sign = None,
    measure_type_full = None,
    measure_type_abbr = None,
    measure_absolute_min = None,
    measure_absolute_max = None,
    measure_target_type = None,
    measure_target_name = ini.ConfigSectionMapAdv(section = refference, option = 'measure_target_name', iniConfig = config),  ##'System' ## 'yes' 'none' 'other'
    measure_target_description = iniConfigSectionMapAdv(section = refference, option = 'measure_target_description', iniConfig = config),  ##'Monitoring Hardware'
    # QA
    data_quality = int(ConfigSectionMapAdv(section = refference, option = 'data_quality', iniConfig = config))  ##99
):
    return csv.headLine(
        _value = value, _pin = pin,
        _utc_1 = utc_1, _utc_2 = utc_2, _offsetutc = offsetutc, _duration_sec = duration_sec,
        _outdoors_name = outdoors_name, _loc_lat = loc_lat, _loc_long = loc_long, _loc_description = loc_description,
        _provider_type = provider_type, _source_name = source_name, _source_description = source_description,
        _periphery_name = periphery_name, _periphery_type = periphery_type, _periphery_description = periphery_description, _periphery_device_description = periphery_device_description,
        _measure_name = measure_name, _measure_sign = measure_sign, _measure_type_full = measure_type_full, _measure_type_abbr = measure_type_abbr, _measure_absolute_min = measure_absolute_min,
        _measure_absolute_max = measure_absolute_max, _measure_target_type = measure_target_type, _measure_target_name = measure_target_name,
        _measure_target_description = measure_target_description,
        _data_quality = data_quality
        )

with open(csv_name, 'ab') as csvfile:
   tst = csv.writer(csvfile, delimiter='|', quoting=csv.QUOTE_NONNUMERIC)
   # print "cpu_temp"
   if cpu_temp is not None:
       cpu_temp_line = _stdLine(
           value = cpu_temp,
           # measure
           measure_name = ini.ConfigSectionMapAdv(section = 'tmp_celsius', option = 'measure_name', iniConfig = config),
           measure_sign = ini.ConfigSectionMapAdv(section = 'tmp_celsius', option = 'measure_sign', iniConfig = config),
           measure_type_full = ini.ConfigSectionMapAdv(section = 'tmp_celsius', option = 'measure_type_full', iniConfig = config),
           measure_type_abbr = ini.ConfigSectionMapAdv(section = 'tmp_celsius', option = 'measure_type_abbr', iniConfig = config),
           measure_absolute_min = float(ini.ConfigSectionMapAdv(section = 'tmp_celsius', option = 'measure_absolute_min', iniConfig = config)),
           measure_absolute_max = None, #float(ini.ConfigSectionMapAdv(section = 'tmp_celsius',option = 'measure_absolute_max', iniConfig = config)),
           measure_target_type = ini.ConfigSectionMapAdv(section = refference, option = 'cpu_measure_target_type', iniConfig = config))
       tst.writerow(cpu_temp_line)
   # print "cpu_use"
   if cpu_use is not None:
       cpu_use_line = _stdLine(
           value = cpu_use,
           # measure
           measure_name = ini.ConfigSectionMapAdv(section = 'percent_used', option = 'measure_name', iniConfig = config),
           measure_sign = ini.ConfigSectionMapAdv(section = 'percent_used', option = 'measure_sign', iniConfig = config),
           measure_type_full = ini.ConfigSectionMapAdv(section = 'percent_used', option = 'measure_type_full', iniConfig = config),
           measure_type_abbr = ini.ConfigSectionMapAdv(section = 'percent_used', option = 'measure_type_abbr', iniConfig = config),
           measure_absolute_min = float(ini.ConfigSectionMapAdv(section = 'percent_used', option = 'measure_absolute_min', iniConfig = config)),
           measure_absolute_max = float(ini.ConfigSectionMapAdv(section = 'percent_used', option = 'measure_absolute_max', iniConfig = config)),
           measure_target_type = ini.ConfigSectionMapAdv(section = refference, option = 'cpu_measure_target_type', iniConfig = config))
       tst.writerow(cpu_use_line)
   # print "disk_percentage"
   if disk_percentage is not None:
       disk_percentage_line = _stdLine(
           value = disk_percentage,
           # measure
           measure_name = ini.ConfigSectionMapAdv(section = 'percent_used', option = 'measure_name', iniConfig = config),
           measure_sign = ini.ConfigSectionMapAdv(section = 'percent_used', option = 'measure_sign', iniConfig = config),
           measure_type_full = ini.ConfigSectionMapAdv(section = 'percent_used', option = 'measure_type_full', iniConfig = config),
           measure_type_abbr = ini.ConfigSectionMapAdv(section = 'percent_used', option = 'measure_type_abbr', iniConfig = config),
           measure_absolute_min = float(ini.ConfigSectionMapAdv(section = 'percent_used', option = 'measure_absolute_min', iniConfig = config)),
           measure_absolute_max = float(ini.ConfigSectionMapAdv(section = 'percent_used', option = 'measure_absolute_max', iniConfig = config)),
           measure_target_type = ini.ConfigSectionMapAdv(section = refference, option = 'disk_measure_target_type', iniConfig = config))
       tst.writerow(disk_percentage_line)
   # print "ram use"
   if ram_used is not None and ram_total is not None:
       ram_used_line = _stdLine(
           value = ram_used,
           # measure
           measure_name = ini.ConfigSectionMapAdv(section = 'MegaByte', option = 'measure_name', iniConfig = config),
           measure_sign = ini.ConfigSectionMapAdv(section = 'MegaByte', option = 'measure_sign', iniConfig = config),
           measure_type_full = ini.ConfigSectionMapAdv(section = refference, option = 'ram_measure_type_full', iniConfig = config),
           measure_type_abbr = ini.ConfigSectionMapAdv(section = refference, option = 'ram_measure_type_abbr', iniConfig = config),
           measure_absolute_min = float(ini.ConfigSectionMapAdv(section = 'MegaByte', option = 'measure_absolute_min', iniConfig = config)),
           measure_absolute_max = ram_total,
           measure_target_type = ini.ConfigSectionMapAdv(section = refference, option = 'ram_measure_target_type', iniConfig = config))
       tst.writerow(ram_used_line)
   # print "ram percent"
   if ram_percent_used is not None:
       ram_percent_used_line = _stdLine(
           value = ram_percent_used,
           # measure
           measure_name = ini.ConfigSectionMapAdv(section = 'percent_used', option = 'measure_name', iniConfig = config),
           measure_sign = ini.ConfigSectionMapAdv(section = 'percent_used', option = 'measure_sign', iniConfig = config),
           measure_type_full = ini.ConfigSectionMapAdv(section = 'percent_used', option = 'measure_type_full', iniConfig = config),
           measure_type_abbr = ini.ConfigSectionMapAdv(section = 'percent_used', option = 'measure_type_abbr', iniConfig = config),
           measure_absolute_min = float(ini.ConfigSectionMapAdv(section = 'percent_used', option = 'measure_absolute_min', iniConfig = config)),
           measure_absolute_max = float(ini.ConfigSectionMapAdv(section = 'percent_used', option = 'measure_absolute_max', iniConfig = config)),
           measure_target_type = ini.ConfigSectionMapAdv(section = refference, option = 'ram_measure_target_type', iniConfig = config))
       tst.writerow(ram_percent_used_line)
   # print "disk use"
   if disk_used is not None and disk_total is not None:
       disk_used_line = _stdLine(
           value = disk_used,
           # measure
           measure_name = ini.ConfigSectionMapAdv(section = 'GigaByte', option = 'measure_name', iniConfig = config),
           measure_sign = ini.ConfigSectionMapAdv(section = 'GigaByte', option = 'measure_sign', iniConfig = config),
           measure_type_full = ini.ConfigSectionMapAdv(section = refference, option = 'disk_measure_type_full', iniConfig = config),
           measure_type_abbr = ini.ConfigSectionMapAdv(section = refference, option = 'disk_measure_type_abbr', iniConfig = config),
           measure_absolute_min = float(ini.ConfigSectionMapAdv(section = 'GigaByte', option = 'measure_absolute_min', iniConfig = config)),
           measure_absolute_max = disk_total,
           measure_target_type = ini.ConfigSectionMapAdv(section = refference, option = 'disk_measure_target_type', iniConfig = config))
       tst.writerow(disk_used_line)


# print "SCP"
def scp(file = "", user = "pi", host = me, path = "~/in/"):
    cmd = "scp {} {}@{}:{}".format(file, user, host, path)
    response = subprocess.call(cmd, shell=True)
    return response == 0

target_user = ini.ConfigSectionMapAdv(section = "Sys", option = 'db_user', iniConfig = config)
mothership = ini.ConfigSectionMapAdv(section = "Sys", option = 'db_host', iniConfig = config)
direc = ini.ConfigSectionMapAdv(section = "Sys", option = 'db_path', iniConfig = config)

try:
    scp(file = csv_name, user = target_user, host = mothership, path = direc)
    #print "tst"
except:
    print "ERROR @ transfer"
