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
from module import mv
import glob, math
## import os

# csv_name = sys.argv[1]
refference = "Sys"
## reading 'freyr_config.ini'

configFile = "freyr_config.ini"
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


## reading 'freyr_config.ini'
ini = "freyr_config.ini"
config = configparser.SafeConfigParser()
config.read(ini)

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
if ntt.ping_host(mothership):
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

print(stml, clean_out, online)
exit()

# 2.  If mothership is available then check FILES
reg = []
files = None
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
    target_user = ConfigSectionMapAdv(refference,'db_user')
    direc = ConfigSectionMapAdv(refference,'db_path')
    n = 0 # number of files processed
    s = 0 # size of files to be processed
    ts = 0 # size of files successfully processed
    for f in files:
        try:
            s1 = f_size(f) #
            ts = ts + s1
            # try transmit
            if scp(file = f, user = target_user, host = mothership, path = direc):
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
        print(str(n) + " (" + str(math.ceil(100.0 * n / len(files) * 100)/100.0 ) + "%)")
    def_counter(refference, 'offline_counter', 0.0) # set counter to 0

    # 3b. If there are no FILES write EVENT-LOG & clear COUNTER & DONE
  elif len(files) == 0:
    n = 0 # number of files processed
    s = 0 # size of files to be processed
    ts = 0 # size of files successfully processed
    def_counter(refference, 'offline_counter', 0.0) # set counter to 0

con_cnt = None

# 5b. If mothership & WWW are unavailable check COUNTER
if online > 0:
    con_cnt = None
    try:
        con_cnt = ConfigSectionMapAdv(refference,'offline_counter')
        def_counter(refference, 'offline_counter', con_cnt + (3.0 / online))
    except:
        def_counter(refference, 'offline_counter', 1.0)
        ## con_cnt = 1.0

    # get COUNTER.ini
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
    measure_target_name = None,  ##'System' ## 'yes' 'none' 'other'
    measure_target_description = None,  ##'Monitoring Hardware'
    # QA
    data_quality = int(ConfigSectionMapAdv(refference,'data_quality'))  ##99
):
    return [value, pin, utc_1, utc_2, offsetutc, duration_sec,outdoors_name, loc_lat, loc_long, loc_description, provider_type, source_name, source_description, periphery_type, periphery_name, periphery_description, periphery_device_description, measure_name, measure_sign, measure_type_full, measure_type_abbr, measure_absolute_min, measure_absolute_max, measure_target_type, measure_target_name, measure_target_description, data_quality]

off_light = None

with open(csv_name, 'ab') as csvfile:
   tst = csv.writer(csvfile, delimiter='|', quoting=csv.QUOTE_NONNUMERIC)
   if s is not None and ts is not None: ## size of files
       bytes_transmitted = std_line(
           value = s,
           measure_name = ConfigSectionMapAdv('Byte','measure_name'),
           measure_sign = ConfigSectionMapAdv('Byte','measure_sign'),
           measure_type_full = ConfigSectionMapAdv('Byte','measure_type_full'),
           measure_type_abbr = ConfigSectionMapAdv('Byte','measure_type_abbr'),
           measure_absolute_min = ConfigSectionMapAdv('Byte','measure_absolute_min'),
           measure_absolute_max = ts,
           measure_target_type = ConfigSectionMapAdv(refference,'trns_measure_target_type'),
           measure_target_name = ConfigSectionMapAdv(refference,'trns_measure_target_name'),
           measure_target_description = ConfigSectionMapAdv(refference,'trns_measure_target_description'))
       tst.writerow(bytes_transmitted)
   if n is not None and len(files) is not None: ## number of files
       files_transmitted = std_line(
           value = n,
           measure_name = ConfigSectionMapAdv('counter','measure_name'),
           measure_sign = ConfigSectionMapAdv('counter','measure_sign'),
           measure_type_full = ConfigSectionMapAdv('counter','measure_type_full'),
           measure_type_abbr = ConfigSectionMapAdv('counter','measure_type_abbr'),
           measure_absolute_min = ConfigSectionMapAdv('counter','measure_absolute_min'),
           measure_absolute_max = len(files),
           measure_target_type = ConfigSectionMapAdv(refference,'trns_measure_target_type'),
           measure_target_name = ConfigSectionMapAdv(refference,'trns_measure_target_name'),
           measure_target_description = ConfigSectionMapAdv(refference,'trns_measure_target_description'))
       tst.writerow(files_transmitted)

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
