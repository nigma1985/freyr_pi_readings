#!/usr/bin/python

# This script develops a python script to read and write envirophat data
# -*- coding: utf-8 -*-

from envirophat import light, motion, weather, analog, leds
import os
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
import configparser ## https://wiki.python.org/moin/ConfigParserExamples

import shutil
#import pyping


#################################################
### do not forget to get ssh-key :
###
###  > ssh-keygen -t rsa
###
### ... and share ssh-key!
#################################################

import module.config as ini ## https://wiki.python.org/moin/ConfigParserExamples
import module.decision as dec
import module.getOptions as opt
import module.timeTools as ttl
import module.netTools as ntt
import module.freyr.csvBuffer as bfr
from module.freyr import findConfig
from module import *
import glob, math
## import os

# csv_name = sys.argv[1]
refference = "Sys"
## reading 'freyr_config.ini'

## configFile = "freyr_config_cp.ini"
configFile = "freyr_config_cp.ini" ## tst
config = ini.getConfig(configFile)
# ini = "freyr_config.ini"
# config = ConfigParser.SafeConfigParser()
# config.read(ini)


me = findConfig(sysKey = "me", confSection = "Sys", confOption = 'source_name', confFile = config)
my_user = findConfig(sysKey = "my_user", confSection = "Sys", confOption = 'user', confFile = config)
mothership = findConfig(sysKey = "mothership", confSection = "Sys", confOption = 'db_host', confFile = config)
hosts = findConfig(sysKey = "hosts", confSection = "Sys", confOption = 'ping', confFile = config)
router = findConfig(sysKey = "router", confSection = "Sys", confOption = 'router', confFile = config)


# _input = sys.argv
# csv_name = _csvName(_input, me)
all_on = opt.findItm("ALLON")
all_off = opt.findItm("ALLOFF")


# ## reading 'freyr_config.ini'
# ini = "freyr_config.ini"
# config = configparser.SafeConfigParser()
# config.read(ini)

# def def_counter(sec = 'Sys', opt = 'offline_counter', x = ""):
#     change = config.set(sec, opt, str(x))
#     with open(ini, 'wb') as change:
#         # change = config.set(sec, opt, str(x))
#         config.write(change)


#################################################
#################################################

# print "me " + me

# 1.  Is mothership available?
stml = findConfig(sysKey = "STML", confSection = refference, confOption = 'short_time_memory_loss', confFile = config)# Short time memory loss (SMTL) in minutes for moving files into archive
### test f_age
# print "File : " + str(f_age("/home/pi/out/FREYR_2018-05-05_1230_" + me + ".csv"))

clean_out = dec.decision(
    onSwitch = [all_on, "MAINTON"],
    offSwitch = [all_off, "MAINTOFF"],
    numChance = findConfig(sysKey = "MAINT", confSection = refference, confOption = 'clean_out', confFile = config))

#################################################
#################################################
#################################################

## Start process ##
now1, utc1, nowsecs = ttl.start()

#################################################

## Ping hosts ##

online = None
if me == mothership:
    online = -1
elif ntt.ping_host(mothership):
    ### is mothership available ?
    print("online: mothership")
    online = 0
else:
    if ntt.ping_host(hosts.split(',')) == True:
        ### is web available ?
        print("online: WWW")
        online = 1
    else:
        if ntt.ping_host(router) == True:
            ### is router available ?
            print("online: router")
            online = 2
        else:
            print("network down!")
            online = 3

# 2.  If mothership is available then check FILES
reg = None
files = []
destination = None
if online < 1 and clean_out == True:
    # reg = "/home/*/out/FREYR_2018-05-12_08*_" + me + ".csv" ## for testing
    reg = "/home/*/out/FREYR_20*-*-*_*_" + me + ".csv"
    files.extend( glob.glob(reg) )
    # if me == mothership:
    #     reg = "/home/*/in/FREYR_20*-*-*_*_" + me + ".csv"
    #     files.extend( glob.glob(reg) )
    destination = "/home/" + my_user + "/in/"

# 3a. If there are FILES transmit FILES & write EVENT-LOG & clear COUNTER & DONE
n = None # number of files processed
s = None # size of files to be processed
ts = None # size of files successfully processed
if islist(files):
  if len(files) > 0:
    err = None
    target_user = findConfig(sysKey = "target_user", confSection = refference, confOption = 'db_user', confFile = config)
    direc = findConfig(sysKey = "db_path", confSection = refference, confOption = 'db_path', confFile = config)
    n = 0 # number of files processed
    s = 0 # size of files to be processed
    ts = 0 # size of files successfully processed
    for f in files:
        try:
            s1 = f_size(f) #
            ts = ts + s1
            # try transmit
            if ntt.scp(file = f, user = target_user, host = mothership, path = direc):
                # n = n + 1
                # catch readings
                err = False
                s = s + s1
        except:
            err = True

        if (err == False):
            if (nowsecs - f_age(f)) >= (stml * 60) and f != csv_name:
                destination = "/home/" + my_user + "/archive/" + f_name(f)
                mv(f, destination)
            n = n + 1
        print(n, ("(" + str(math.ceil(100.0 * n / len(files) * 100)/100.0 ) + "%)"))
    ini.writeConfig(section = refference, option = 'offline_counter', iniFile = configFile, iniConfig = config, value = 0.0) # set counter to 0

    # 3b. If there are no FILES write EVENT-LOG & clear COUNTER & DONE
  elif len(files) == 0:
    n = 0 # number of files processed
    s = 0 # size of files to be processed
    ts = 0 # size of files successfully processed
    ini.writeConfig(section = refference, option = 'offline_counter', iniFile = configFile, iniConfig = config, value = 0.0) # set counter to 0

con_cnt = None


# 5b. If mothership & WWW are unavailable check COUNTER
if online > 0:
    con_cnt = None
    try:
        con_cnt = findConfig(sysKey = "offline_counter", confSection = refference, confOption = 'offline_counter', confFile = config)
        ini.writeConfig(section = refference, option = 'offline_counter', iniFile = configFile, iniConfig = config, value = con_cnt + (3.0 / online))
    except:
        ini.writeConfig(section = refference, option = 'offline_counter', iniFile = configFile, iniConfig = config, value = 1.0)
        ## con_cnt = 1.0


print(me, mothership, clean_out, online, reg, files, destination)
print(n, s, ts, con_cnt)
exit()

utc2, offset_utc, duration, duration2 = ttl.end(now1, utc1)

def _stdLine(
    value = 0.0,
    pin = findConfig(sysKey = "pin", readVar = None, confSection = refference, confOption = 'pin', confFile = config),
    # time
    utc_1 = utc1,
    utc_2 = utc2,
    offsetutc = offset_utc,
    duration_sec = duration2,
    # location
    outdoors_name = findConfig(sysKey = "outdoors_name", confSection = refference, confOption = 'outdoors_name', confFile = config),
    loc_lat = findConfig(sysKey = "loc_lat", confSection = refference, confOption = 'loc_lat', confFile = config),
    loc_long = findConfig(sysKey = "loc_long", confSection = refference, confOption = 'loc_long', confFile = config),
    loc_description = findConfig(sysKey = "loc_description", confSection = refference, confOption = 'loc_description', confFile = config),
    # source / provider
    provider_type = findConfig(sysKey = "provider_type", confSection = refference, confOption = 'provider_type', confFile = config),
    source_name = me,
    source_description = findConfig(sysKey = "source_description", confSection = refference, confOption = 'source_description', confFile = config),
    # periphery
    periphery_name = findConfig(sysKey = "periphery_name", confSection = refference, confOption = 'periphery_name', confFile = config),
    periphery_type = findConfig(sysKey = "periphery_type", confSection = refference, confOption = 'periphery_type', confFile = config),
    periphery_description = findConfig(sysKey = "periphery_description", confSection = refference, confOption = 'periphery_description', confFile = config),
    periphery_device_description = findConfig(sysKey = "periphery_device_description", confSection = refference, confOption = 'periphery_device_description', confFile = config),
    # measure
    measure_name = None,
    measure_sign = None,
    measure_type_full = None,
    measure_type_abbr = None,
    measure_absolute_min = None,
    measure_absolute_max = None,
    measure_target_type = None,
    measure_target_name = None,
    measure_target_description = None,
    # QA
    data_quality = findConfig(sysKey = "data_quality", confSection = refference, confOption = 'data_quality', confFile = config)
):
    return bfr.headLine(
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

csv_name = bfr.csvName(me)
bfr.initiateFile(csv_name)
if s is not None and ts is not None:
    bfr.writeRow(row = _stdLine(
        value = s,
        # measure
        measure_name = findConfig(sysKey = "cpu_temp_measure_name", confSection = 'Byte', confOption = 'measure_name', confFile = config),
        measure_sign = findConfig(sysKey = "cpu_temp_measure_sign", confSection = 'Byte', confOption = 'measure_sign', confFile = config),
        measure_type_full = findConfig(sysKey = "cpu_temp_measure_type_full", confSection = 'Byte', confOption = 'measure_type_full', confFile = config),
        measure_type_abbr = findConfig(sysKey = "cpu_temp_measure_type_abbr", confSection = 'Byte', confOption = 'measure_type_abbr', confFile = config),
        measure_absolute_min = findConfig(sysKey = "cpu_temp_measure_absolute_min", confSection = 'Byte', confOption = 'measure_absolute_min', confFile = config),
        measure_absolute_max = findConfig(readVar = ts, sysKey = "cpu_temp_measure_absolute_max", confSection = 'Byte', confOption = 'measure_absolute_max', confFile = config),
        measure_target_type = findConfig(sysKey = "cpu_temp_measure_target_type", confSection = refference, confOption = 'cpu_measure_target_type', confFile = config),
        measure_target_name = findConfig(sysKey = "trns_measure_target_name", confSection = refference, confOption = 'trns_measure_target_name', confFile = config),
        measure_target_description = findConfig(sysKey = "trns_measure_target_description", confSection = refference, confOption = 'trns_measure_target_description')
        ), csvFile = csv_name)
if n is not None and len(files) is not None: ## number of files
    bfr.writeRow(row = _stdLine(
        value = n,
        # measure
        measure_name = findConfig(sysKey = "cpu_temp_measure_name", confSection = 'counter', confOption = 'measure_name', confFile = config),
        measure_sign = findConfig(sysKey = "cpu_temp_measure_sign", confSection = 'counter', confOption = 'measure_sign', confFile = config),
        measure_type_full = findConfig(sysKey = "cpu_temp_measure_type_full", confSection = 'counter', confOption = 'measure_type_full', confFile = config),
        measure_type_abbr = findConfig(sysKey = "cpu_temp_measure_type_abbr", confSection = 'counter', confOption = 'measure_type_abbr', confFile = config),
        measure_absolute_min = findConfig(sysKey = "cpu_temp_measure_absolute_min", confSection = 'counter', confOption = 'measure_absolute_min', confFile = config),
        measure_absolute_max = findConfig(readVar = len(files), sysKey = "cpu_temp_measure_absolute_max", confSection = 'counter', confOption = 'measure_absolute_max', confFile = config),
        measure_target_type = findConfig(sysKey = "cpu_temp_measure_target_type", confSection = refference, confOption = 'trns_measure_target_type', confFile = config),
        measure_target_name = findConfig(sysKey = "trns_measure_target_name", confSection = refference, confOption = 'trns_measure_target_name', confFile = config),
        measure_target_description = findConfig(sysKey = "trns_measure_target_description", confSection = refference, confOption = 'trns_measure_target_description')
        ), csvFile = csv_name)

try:
    ntt.scPush(
        scpFile = findConfig(sysKey = "csvFile", readVar = csv_name, confSection = "Sys", confOption = 'csvFile', confFile = config),
        scpUser = findConfig(sysKey = "db_user", confSection = "Sys", confOption = 'db_user', confFile = config),
        scpHost = findConfig(sysKey = "db_host", confSection = "Sys", confOption = 'db_host', confFile = config),
        scpPath = findConfig(sysKey = "db_path", confSection = "Sys", confOption = 'db_path', confFile = config))
    #print "tst"
except:
    raise exception("ERROR @ transfer")

if online == 3:
    if con_cnt > ConfigSectionMapAdv(refference,'min2restart'):
        # print "gonna restart!"
        print("reboot")
    else:
        # print "let's fix it"
        if random() <= (1/4):
            print("wlan0")
        else:
            print("err")
else:
    print("ok")
