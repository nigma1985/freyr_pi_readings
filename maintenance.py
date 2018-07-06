#!/usr/bin/python

# This script develops a python script to read and write envirophat data
# -*- coding: utf-8 -*-
from __future__ import division
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
import ConfigParser ## https://wiki.python.org/moin/ConfigParserExamples
import glob
import shutil
#import pyping
import math

#################################################
### do not forget to get ssh-key : 
###
###  > ssh-keygen -t rsa
###
### ... and share ssh-key!
#################################################

# csv_name = sys.argv[1]
refference = "Sys"

## reading 'freyr_config.ini'
ini = "freyr_config.ini"
config = ConfigParser.SafeConfigParser()
config.read(ini)

# print config.sections()

def ConfigSectionMap(section):
     dict1 = {}
     options = config.options(section)
     for option in options:
         try:
             dict1[option] = config.get(section, option)
             if dict1[option] == -1:
                 DebugPrint("skip: %s" % option)
         except:
             print("exception on %s!" % option)
             dict1[option] = None
     return dict1

def ConfigSectionMapAdv(section,option):
     dict1 = {}
     try:
         dict1 = ConfigSectionMap(section)[option]
     except:
         dict1 = ConfigSectionMap("defaults")[option]
     if dict1 == 'None' or dict1 == '':
         dict1 = None
     else:
         try:
             dict1 = int(dict1)
         except:
             try:
                 dict1 = float(dict1)
             except:
                 dict1 = str(dict1)
     if isinstance(dict1, str):
         if dict1[:3] == "u'\\" or dict1[:3] == 'u"\\':
             x = re.search(r"u[\"|\'](\\.+)[\"|\']", dict1)
             x = x.group(1)
             dict1 = x.decode('unicode-escape')
     return dict1

def def_counter(sec = 'Sys', opt = 'offline_counter', x = ""):
    change = config.set(sec, opt, str(x))
    with open(ini, 'wb') as change:
        # change = config.set(sec, opt, str(x))
        config.write(change)

me = ConfigSectionMapAdv(refference,'source_name')
my_user = ConfigSectionMapAdv(refference,'user')
mothership = ConfigSectionMapAdv(refference,'db_host')
hosts = ConfigSectionMapAdv(refference,'ping')
router = ConfigSectionMapAdv(refference,'router')

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

def ping_singlehost(host = me, trys = randint(1, 10)):
    try:
        output = subprocess.check_output("ping -{} {} {}".format('n' if platform.system().lower()=="windows" else 'c', trys, host), shell=True)
    except Exception, e:
        return False
    return True

def ping_host(hosts = me, meta_trys = randint(3, 10)):
    if isinstance(hosts, str):
        return ping_singlehost(host = hosts, trys = meta_trys)
    elif isinstance(hosts, (list, tuple)):
        i = 0 # result to be returned
        j = meta_trys # number tries
        k = 0 # random number of pings (lower j)
        l = 0 # number of hosts pinged
        m = 0
        hosts = sample(hosts, j) # take random sample of hosts, shuffle them 
        # hosts = shuffle(hosts) # take random sample of hosts, shuffle them 
        for h in hosts: # loop host list
            m = m + 1
            k = 0
            if (random() ** 2) >= (m / len(hosts)):
                k = randint(0,j)
            if m == len(hosts):
                k = j
            # k = randint(0,y)
            # print "numb of pings now: " + str(k)
            if k > 0:
                if ping_singlehost(host = h, trys = k) == False:
                    # print h + " : " + str(k) + "x"
                    i = i + 1
                j = j - k
                l = l + 1
        # print 1.0 * (i / l)
        return .5 > 1.0 * (i / l) # more then half of hosts = no connection
    else:
        return None

def scp(file = "", user = "pi", host = me, path = "~/in/"):
    cmd = "scp {} {}@{}:{}".format(file, user, host, path)
    # print cmd
    response = subprocess.call(cmd, shell=True)
    return response == 0

def mv(f = "", p = "~/"):
    return shutil.move(f, p)

def f_name(path):
    if path is not None:
        # print path
        try:
            p = open(path)
            # print p
            return os.path.basename(p.name)
        except:
            return None
    else:
        None

def f_size(file = ""):
    size = os.stat(file)
    return size.st_size # output in bytes

def f_age(file = ""):
    age = os.stat(file)
    # age = max(
        # age.st_atime ## time of access
        # age.st_mtime ## time of change
        # age.st_ctime ## time of creation/metachange
    # )
    return age.st_ctime # output in bytes

def islist(lst):
    if type(lst)==list:
        return True
    else:
        return False

## not adopted
def reconnect():
    return

def reboot():
    return

#################################################
#################################################

# print "me " + me

# 1.  Is mothership available?

online = None
stml = ConfigSectionMapAdv(refference,'short_time_memory_loss') # Short time memory loss (SMTL) in minutes for moving files into archive
### test f_age
# print "File : " + str(f_age("/home/pi/out/FREYR_2018-05-05_1230_" + me + ".csv"))
clean_out = None
if all_off:
    clean_out = False
    print "Clean-Out off"
elif all_on:
    clean_out = True
    print "Clean-Out on"
else:
    clean_out = random() <= (1.0 / float(ConfigSectionMapAdv(refference,'clean_out')))
# print clean_out

#################################################
#################################################
#################################################

## Start process ##
now1 = datetime.now()
utc1 = datetime.utcnow()
nowsecs = time.mktime(now1.timetuple())

#################################################

## Ping hosts ##
if ping_host(mothership):
    ### is mothership available ? 
    print "online: mothership"
    online = 0
else:
    if ping_host(hosts.split(',')) == True:
        ### is web available ?
        print "online: WWW"
        online = 1
    else:
        if ping_host(router) == True:
            ### is router available ? 
            print "online: router"
            online = 2
        else:
            print "network down!"
            online = 3

# 2.  If mothership is available then check FILES
reg = None
files = None
if online < 1 and clean_out == True:
    reg = "/home/*/out/FREYR_20*-*-*_*_" + me + ".csv"
    # reg = "/home/*/out/FREYR_2018-05-12_08*_" + me + ".csv" ## for testing
    files = glob.glob(reg)
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
        print str(n) + " (" + str(math.ceil(100.0 * n / len(files) * 100)/100.0 ) + "%)"
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
    con_cnt = ConfigSectionMapAdv(refference,'offline_counter')
    def_counter(refference, 'offline_counter', con_cnt + (3.0 / online))
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
        print "reboot"
    else:
        # print "let's fix it"
        if random() <= (1/4):
            print "wlan0"
        else:
            print "err"
else: 
    print "ok"
