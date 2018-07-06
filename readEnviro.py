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
import random
import ConfigParser ## https://wiki.python.org/moin/ConfigParserExamples

csv_name = sys.argv[1]
refference = "Enviro pHAT"

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

me = ConfigSectionMapAdv("Sys",'source_name')
my_user = ConfigSectionMapAdv("Sys",'user')

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

# sensor = Adafruit_DHT.DHT22
# pin = ConfigSectionMap(refference)['pin']
sleeptimer = (1.0 / 3.0) * 2.0

led_on = _findItm(_input, "LEDON")
led_off = _findItm(_input, "LEDOFF")
rgb_on = _findItm(_input, "RGBON")
rgb_off = _findItm(_input, "RGBOFF")
lgt_on = _findItm(_input, "LGTON")
lgt_off = _findItm(_input, "LGTOFF")
raw_on = _findItm(_input, "RAWON")
raw_off = _findItm(_input, "RAWOFF")

led_light = None
if (lgt_off or all_off or led_off):
	led_light = False
        print "led light off"
elif (lgt_on or all_on or led_on):
	led_light = True
        print "led light on"
else:
	led_light = random.random() <= (1.0 / float(ConfigSectionMapAdv(refference,'led_light')))

led_rgb = None
if (rgb_off or all_off or led_off):
	led_rgb = False
        print "led rgb off"
elif (rgb_on or all_on or led_on):
	led_rgb = True
        print "led rgb on"
else:
	led_rgb = random.random() <= (1.0 / float(ConfigSectionMapAdv(refference,'led_rgb')))

led_raw = None
if (raw_off or all_off or led_off):
	led_raw = False
        print "led raw off"
elif (raw_on or all_on or led_on):
	led_raw = True
        print "led raw on"
else:
        led_raw = random.random() <= (1.0 / float(ConfigSectionMapAdv(refference,'led_raw')))


rec_light = None
if (lgt_off or all_off or led_on):
	rec_light = False
        print "light off"
elif (lgt_on or all_on or led_off):
	rec_light = True
        print "light on"
else:
	rec_light = random.random() <= (1.0 / float(ConfigSectionMapAdv(refference,'rec_light')))

rec_rgb = None
if (rgb_off or all_off or led_on):
	rec_rgb = False
        print "rgb off"
elif (rgb_on or all_on or led_off):
	rec_rgb = True
        print "rgb on"
else:
	rec_rgb = random.random() <= (1.0 / float(ConfigSectionMapAdv(refference,'rec_rgb')))

rec_raw = None
if (raw_off or all_off or led_on):
	rec_raw = False
        print "raw off"
elif (raw_on or all_on or led_off):
	rec_raw = True
        print "raw on"
else:
	rec_raw = random.random() <= (1.0 / float(ConfigSectionMapAdv(refference,'rec_raw')))

tmp_on = _findItm(_input, "TMPON")
tmp_off = _findItm(_input, "TMPOFF")
qnh_on = _findItm(_input, "QNHON")
qnh_off = _findItm(_input, "QNHOFF")
alt_on = _findItm(_input, "ALTON")
alt_off = _findItm(_input, "ALTOFF")
prs_on = _findItm(_input, "PRSON")
prs_off = _findItm(_input, "PRSOFF")

## weather via BMP280

rec_temp = None
if (all_off or tmp_off):
	rec_temp = False
        print "tmp off"
elif (all_on or tmp_on):
	rec_temp = True
        print "tmp on"
else:
	rec_temp = random.random() <= (1.0 / float(ConfigSectionMapAdv(refference,'rec_temp')))

rec_prss = None
if (all_off or prs_off):
	rec_prss = False
        print "prss off"
elif (all_on or prs_on):
	rec_prss = True
        print "prss on"
else:
	rec_prss = random.random() <= (1.0 / float(ConfigSectionMapAdv(refference,'rec_prss')))

rec_altd_qnh = None
if (all_off or qnh_off):
	rec_altd_qnh = False
        print "altd_qnh off"
elif (all_on or qnh_on):
	rec_altd_qnh = True
        print "altd_qnh on"
else:
	rec_altd_qnh = random.random() <= (1.0 / float(ConfigSectionMapAdv(refference,'rec_altd_qnh')))

rec_altd = None
if (alt_off or all_off):
	rec_altd = False
        print "altd off"
elif (alt_on or all_on):
	rec_altd = True
        print "altd on"
else:
	rec_altd = random.random() <= (1.0 / float(ConfigSectionMapAdv(refference,'rec_altd')))
# weather.update()


mgm_on = _findItm(_input, "MGMON")
mgm_off = _findItm(_input, "MGMOFF")
acc_on = _findItm(_input, "ACCON")
acc_off = _findItm(_input, "ACCOFF")
hd_on = _findItm(_input, "HDON")
hd_off = _findItm(_input, "HDOFF")
rhd_on = _findItm(_input, "RHDON")
rhd_off = _findItm(_input, "RHDOFF")

## motion via LSM303D
rec_mgnm = None
if (mgm_off or all_off):
	rec_mgnm = False
        print "mgnm off"
elif (mgm_on or all_on):
	rec_mgnm = True
        print "mgnm on"
else:
	rec_mgnm = random.random() <= (1.0 / float(ConfigSectionMapAdv(refference,'rec_mgnm')))

rec_acclm = None
if (acc_off or all_off):
	rec_acclm = False
        print "acclm off"
elif (acc_on or all_on):
	rec_acclm = True
        print "acclm on"
else:
	rec_acclm = random.random() <= (1.0 / float(ConfigSectionMapAdv(refference,'rec_acclm')))

rec_headng = None
if (hd_off or all_off):
	rec_headng = False
        print "heading off"
elif (hd_on or all_on):
	rec_headng = True
        print "heading on"
else:
	rec_headng = random.random() <= (1.0 / float(ConfigSectionMapAdv(refference,'rec_headng')))

rec_rawheadng = None
if (rhd_off or all_off):
	rec_rawheadng = False
        print "raw heading off"
elif (rhd_on or all_on):
	rec_rawheadng = True
        print "raw heading on"
else:
	rec_rawheadng = random.random() <= (1.0 / float(ConfigSectionMapAdv(refference,'rec_rawheadng')))


# Try to grab a sensor reading.  Use the read_retry method which will retry up
now1 = datetime.now()
utc1 = datetime.utcnow()
nowsecs = time.mktime(now1.timetuple())

## lights via TCS3472
off_light = None
off_rgb = None
off_rawl = None
if led_light == False and rec_light == True:
    off_light = light.light()
if (led_rgb == False and rec_rgb == True) and off_light > 5:
    off_rgb = light.rgb()
if led_raw == False and rec_raw == True:
    off_rawl = light.raw()

on_light = None
on_rgb = None
on_rawl = None
if (led_light == True and rec_light == True) or (led_rgb == True and rec_rgb == True) or (led_raw == True and rec_raw == True):
    leds.on() 
    time.sleep(sleeptimer)
    if rec_light == True:
        on_light = light.light()
    if rec_rgb == True:
        on_rgb = light.rgb()
    if rec_raw == True:
        on_rawl = light.raw()
    leds.off()
    # time.sleep(sleeptimer)

## motion via LSM303D
mgnm = None
acclm = None
headng = None
rawheadng = None
if rec_mgnm == True:
    mgnm = motion.magnetometer()
if rec_acclm == True:
    acclm = motion.accelerometer()
if rec_headng == True:
    headng = motion.heading()
if rec_rawheadng == True:
    rawheadng = motion.raw_heading()
#print motion.update()

## Analog via ADS1015
#analog = None
## weather via BMP280
temp = None
prss = None
prss_sl = None
altd_qnh = None
altd = None
if rec_temp == True:
    temp = weather.temperature()
if rec_prss == True:
    prss = weather.pressure()
if rec_altd_qnh == True:
    prss_sl = ConfigSectionMapAdv(refference,'hpa_sea_level')
    altd_qnh == weather.altitude(qnh=prss_sl)
if rec_altd == True:
    altd = weather.altitude()
# weather.update()

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

with open(csv_name, 'ab') as csvfile:
   tst = csv.writer(csvfile, delimiter='|', quoting=csv.QUOTE_NONNUMERIC)
   if off_light is not None:
       off_light_line = std_line(
           value = off_light,
           pin = ConfigSectionMapAdv(refference,'tcf_pin'),
           measure_name = ConfigSectionMapAdv('light level','measure_name'),
           measure_sign = ConfigSectionMapAdv('light level','measure_sign'),
           measure_type_full = ConfigSectionMapAdv('light level','measure_type_full'),
           measure_type_abbr = ConfigSectionMapAdv('light level','measure_type_abbr'),
           measure_absolute_min = ConfigSectionMapAdv('light level','measure_absolute_min'),
           measure_absolute_max = ConfigSectionMapAdv('light level','measure_absolute_max'), 
           measure_target_type = ConfigSectionMapAdv(refference,'tcf_measure_target_type'),
           measure_target_name = ConfigSectionMapAdv(refference,'tcf_measure_target_name'),
           measure_target_description = ConfigSectionMapAdv(refference,'tcf_measure_target_description') + " (LED: OFF)")
       tst.writerow(off_light_line)
   if on_light is not None:
       on_light_line = std_line(
           value = on_light,
           pin = ConfigSectionMapAdv(refference,'tcf_pin'),
           measure_name = ConfigSectionMapAdv('light level','measure_name'),
           measure_sign = ConfigSectionMapAdv('light level','measure_sign'),
           measure_type_full = ConfigSectionMapAdv('light level','measure_type_full'),
           measure_type_abbr = ConfigSectionMapAdv('light level','measure_type_abbr'),
           measure_absolute_min = ConfigSectionMapAdv('light level','measure_absolute_min'),
           measure_absolute_max = ConfigSectionMapAdv('light level','measure_absolute_max'),
           measure_target_type = ConfigSectionMapAdv(refference,'tcf_measure_target_type'),
           measure_target_name = ConfigSectionMapAdv(refference,'tcf_measure_target_name'),
           measure_target_description = ConfigSectionMapAdv(refference,'tcf_measure_target_description') + " (LED: ON)")
       tst.writerow(on_light_line)
   if temp is not None:
       temp_line = std_line(
           value = temp,
           pin = ConfigSectionMapAdv(refference,'bmp_pin'),
           measure_name = ConfigSectionMapAdv('tmp_celsius','measure_name'),
           measure_sign = ConfigSectionMapAdv('tmp_celsius','measure_sign'),
           measure_type_full = ConfigSectionMapAdv('tmp_celsius','measure_type_full'),
           measure_type_abbr = ConfigSectionMapAdv('tmp_celsius','measure_type_abbr'),
           measure_absolute_min = ConfigSectionMapAdv('tmp_celsius','measure_absolute_min'),
           measure_absolute_max = ConfigSectionMapAdv('tmp_celsius','measure_absolute_max'), 
           measure_target_type = ConfigSectionMapAdv(refference,'bmp_measure_target_type'),
           measure_target_name = ConfigSectionMapAdv(refference,'bmp_measure_target_name'),
           measure_target_description = ConfigSectionMapAdv(refference,'bmp_measure_target_description'))
       tst.writerow(temp_line)
   if prss is not None:
       prss_line = std_line(
           value = prss,
           pin = ConfigSectionMapAdv(refference,'bmp_pin'),
           measure_name = ConfigSectionMapAdv('pressure_pa','measure_name'),
           measure_sign = ConfigSectionMapAdv('pressure_pa','measure_sign'),
           measure_type_full = ConfigSectionMapAdv('pressure_pa','measure_type_full'),
           measure_type_abbr = ConfigSectionMapAdv('pressure_pa','measure_type_abbr'),
           measure_absolute_min = ConfigSectionMapAdv('pressure_pa','measure_absolute_min'),
           measure_absolute_max = ConfigSectionMapAdv('pressure_pa','measure_absolute_max'),
           measure_target_type = ConfigSectionMapAdv(refference,'bmp_measure_target_type'),
           measure_target_name = ConfigSectionMapAdv(refference,'bmp_measure_target_name'),
           measure_target_description = ConfigSectionMapAdv(refference,'bmp_measure_target_description'))
       tst.writerow(prss_line)
   if altd is not None:
       altd_line = std_line(
           value = altd_qnh,
           pin = ConfigSectionMapAdv(refference,'bmp_pin'),
           measure_name = ConfigSectionMapAdv('altitude','measure_name'),
           measure_sign = ConfigSectionMapAdv('altitude','measure_sign'),
           measure_type_full = ConfigSectionMapAdv('altitude','measure_type_full'),
           measure_type_abbr = ConfigSectionMapAdv('altitude','measure_type_abbr'),
           measure_absolute_min = ConfigSectionMapAdv('altitude','measure_absolute_min'),
           measure_absolute_max = ConfigSectionMapAdv('altitude','measure_absolute_max'), 
           measure_target_type = ConfigSectionMapAdv(refference,'bmp_measure_target_type'),
           measure_target_name = ConfigSectionMapAdv(refference,'bmp_measure_target_name'),
           measure_target_description = ConfigSectionMapAdv(refference,'bmp_measure_target_description'))
       tst.writerow(altd_line)
   if altd_qnh is not None and prss_sl is not None:
       altd_qnh_line = std_line(
           value = altd_qnh,
           pin = ConfigSectionMapAdv(refference,'bmp_pin'),
           measure_name = ConfigSectionMapAdv('altitude','measure_name'),
           measure_sign = ConfigSectionMapAdv('altitude','measure_sign'),
           measure_type_full = ConfigSectionMapAdv('altitude','measure_type_full'),
           measure_type_abbr = ConfigSectionMapAdv('altitude','measure_type_abbr'),
           measure_absolute_min = ConfigSectionMapAdv('altitude','measure_absolute_min'),
           measure_absolute_max = ConfigSectionMapAdv('altitude','measure_absolute_max'),
           measure_target_type = ConfigSectionMapAdv(refference,'bmp_measure_target_type'),
           measure_target_name = ConfigSectionMapAdv(refference,'bmp_measure_target_name'),
           measure_target_description = ConfigSectionMapAdv(refference,'bmp_measure_target_description') + " (Air Pressure at Sea Level = " + str(prss_sl) + " hPa)")
       tst.writerow(altd_qnh_line)
   if headng is not None:
       headng_line = std_line(
           value = headng,
           pin = ConfigSectionMapAdv(refference,'lsm_pin'),
           measure_name = ConfigSectionMapAdv('heading','measure_name'),
           measure_sign = ConfigSectionMapAdv('heading','measure_sign'),
           measure_type_full = ConfigSectionMapAdv('heading','measure_type_full'),
           measure_type_abbr = ConfigSectionMapAdv('heading','measure_type_abbr'),
           measure_absolute_min = ConfigSectionMapAdv('heading','measure_absolute_min'),
           measure_absolute_max = ConfigSectionMapAdv('heading','measure_absolute_max'), 
           measure_target_type = ConfigSectionMapAdv(refference,'lsm_measure_target_type'),
           measure_target_name = ConfigSectionMapAdv(refference,'lsm_measure_target_name'),
           measure_target_description = ConfigSectionMapAdv(refference,'lsm_measure_target_description') )
       tst.writerow(headng_line)
   if rawheadng is not None:
       rawheadng_line = std_line(
           value = rawheadng,
           pin = ConfigSectionMapAdv(refference,'lsm_pin'),
           measure_name = ConfigSectionMapAdv('raw heading','measure_name'),
           measure_sign = ConfigSectionMapAdv('raw heading','measure_sign'),
           measure_type_full = ConfigSectionMapAdv('raw heading','measure_type_full'),
           measure_type_abbr = ConfigSectionMapAdv('raw heading','measure_type_abbr'),
           measure_absolute_min = ConfigSectionMapAdv('raw heading','measure_absolute_min'),
           measure_absolute_max = ConfigSectionMapAdv('raw heading','measure_absolute_max'),
           measure_target_type = ConfigSectionMapAdv(refference,'lsm_measure_target_type'),
           measure_target_name = ConfigSectionMapAdv(refference,'lsm_measure_target_name'),
           measure_target_description = ConfigSectionMapAdv(refference,'lsm_measure_target_description'))
       tst.writerow(rawheadng_line)
   if off_rgb is not None:
       roff_rgb_line = std_line(
           value = off_rgb[0],
           pin = ConfigSectionMapAdv(refference,'tcf_pin'),
           measure_name = ConfigSectionMapAdv('rgb colour','r_measure_name'),
           measure_sign = ConfigSectionMapAdv('rgb colour','measure_sign'),
           measure_type_full = ConfigSectionMapAdv('rgb colour','measure_type_full'),
           measure_type_abbr = ConfigSectionMapAdv('rgb colour','measure_type_abbr'),
           measure_absolute_min = ConfigSectionMapAdv('rgb colour','measure_absolute_min'),
           measure_absolute_max = ConfigSectionMapAdv('rgb colour','measure_absolute_max'),
           measure_target_type = ConfigSectionMapAdv(refference,'tcf_measure_target_type'),
           measure_target_name = ConfigSectionMapAdv(refference,'tcf_measure_target_name'),
           measure_target_description = ConfigSectionMapAdv(refference,'tcf_measure_target_description')  + " (LED: OFF)")
       tst.writerow(roff_rgb_line)
   if off_rgb is not None:
       goff_rgb_line = std_line(
           value = off_rgb[1],
           pin = ConfigSectionMapAdv(refference,'tcf_pin'),
           measure_name = ConfigSectionMapAdv('rgb colour','g_measure_name'),
           measure_sign = ConfigSectionMapAdv('rgb colour','measure_sign'),
           measure_type_full = ConfigSectionMapAdv('rgb colour','measure_type_full'),
           measure_type_abbr = ConfigSectionMapAdv('rgb colour','measure_type_abbr'),
           measure_absolute_min = ConfigSectionMapAdv('rgb colour','measure_absolute_min'),
           measure_absolute_max = ConfigSectionMapAdv('rgb colour','measure_absolute_max'), 
           measure_target_type = ConfigSectionMapAdv(refference,'tcf_measure_target_type'),
           measure_target_name = ConfigSectionMapAdv(refference,'tcf_measure_target_name'),
           measure_target_description = ConfigSectionMapAdv(refference,'tcf_measure_target_description')  + " (LED: OFF)")
       tst.writerow(goff_rgb_line)
   if off_rgb is not None:
       boff_rgb_line = std_line(
           value = off_rgb[2],
           pin = ConfigSectionMapAdv(refference,'tcf_pin'),
           measure_name = ConfigSectionMapAdv('rgb colour','b_measure_name'),
           measure_sign = ConfigSectionMapAdv('rgb colour','measure_sign'),
           measure_type_full = ConfigSectionMapAdv('rgb colour','measure_type_full'),
           measure_type_abbr = ConfigSectionMapAdv('rgb colour','measure_type_abbr'),
           measure_absolute_min = ConfigSectionMapAdv('rgb colour','measure_absolute_min'),
           measure_absolute_max = ConfigSectionMapAdv('rgb colour','measure_absolute_max'),
           measure_target_type = ConfigSectionMapAdv(refference,'tcf_measure_target_type'),
           measure_target_name = ConfigSectionMapAdv(refference,'tcf_measure_target_name'),
           measure_target_description = ConfigSectionMapAdv(refference,'tcf_measure_target_description')  + " (LED: OFF)")
       tst.writerow(boff_rgb_line)
   if on_rgb is not None:
       ron_rgb_line = std_line(
           value = on_rgb[0],
           pin = ConfigSectionMapAdv(refference,'tcf_pin'),
           measure_name = ConfigSectionMapAdv('rgb colour','r_measure_name'),
           measure_sign = ConfigSectionMapAdv('rgb colour','measure_sign'),
           measure_type_full = ConfigSectionMapAdv('rgb colour','measure_type_full'),
           measure_type_abbr = ConfigSectionMapAdv('rgb colour','measure_type_abbr'),
           measure_absolute_min = ConfigSectionMapAdv('rgb colour','measure_absolute_min'),
           measure_absolute_max = ConfigSectionMapAdv('rgb colour','measure_absolute_max'),
           measure_target_type = ConfigSectionMapAdv(refference,'tcf_measure_target_type'),
           measure_target_name = ConfigSectionMapAdv(refference,'tcf_measure_target_name'),
           measure_target_description = ConfigSectionMapAdv(refference,'tcf_measure_target_description')  + " (LED: ON)")
       tst.writerow(ron_rgb_line)
   if on_rgb is not None:
       gon_rgb_line = std_line(
           value = on_rgb[1],
           pin = ConfigSectionMapAdv(refference,'tcf_pin'),
           measure_name = ConfigSectionMapAdv('rgb colour','g_measure_name'),
           measure_sign = ConfigSectionMapAdv('rgb colour','measure_sign'),
           measure_type_full = ConfigSectionMapAdv('rgb colour','measure_type_full'),
           measure_type_abbr = ConfigSectionMapAdv('rgb colour','measure_type_abbr'),
           measure_absolute_min = ConfigSectionMapAdv('rgb colour','measure_absolute_min'),
           measure_absolute_max = ConfigSectionMapAdv('rgb colour','measure_absolute_max'), 
           measure_target_type = ConfigSectionMapAdv(refference,'tcf_measure_target_type'),
           measure_target_name = ConfigSectionMapAdv(refference,'tcf_measure_target_name'),
           measure_target_description = ConfigSectionMapAdv(refference,'tcf_measure_target_description')  + " (LED: ON)")
       tst.writerow(gon_rgb_line)
   if on_rgb is not None:
       bon_rgb_line = std_line(
           value = on_rgb[2],
           pin = ConfigSectionMapAdv(refference,'tcf_pin'),
           measure_name = ConfigSectionMapAdv('rgb colour','b_measure_name'),
           measure_sign = ConfigSectionMapAdv('rgb colour','measure_sign'),
           measure_type_full = ConfigSectionMapAdv('rgb colour','measure_type_full'),
           measure_type_abbr = ConfigSectionMapAdv('rgb colour','measure_type_abbr'),
           measure_absolute_min = ConfigSectionMapAdv('rgb colour','measure_absolute_min'),
           measure_absolute_max = ConfigSectionMapAdv('rgb colour','measure_absolute_max'),
           measure_target_type = ConfigSectionMapAdv(refference,'tcf_measure_target_type'),
           measure_target_name = ConfigSectionMapAdv(refference,'tcf_measure_target_name'),
           measure_target_description = ConfigSectionMapAdv(refference,'tcf_measure_target_description')  + " (LED: ON)")
       tst.writerow(bon_rgb_line)
   if off_rawl is not None:
       roff_rawl_line = std_line(
           value = off_rawl[0],
           pin = ConfigSectionMapAdv(refference,'tcf_pin'),
           measure_name = ConfigSectionMapAdv('rgb colour','r_measure_name'),
           measure_sign = ConfigSectionMapAdv('rgb colour','measure_sign'),
           measure_type_full = ConfigSectionMapAdv('rgb colour','measure_type_full'),
           measure_type_abbr = ConfigSectionMapAdv('rgb colour','measure_type_abbr'),
           measure_absolute_min = ConfigSectionMapAdv('rgb colour','measure_absolute_min'),
           measure_absolute_max = off_rawl[3],
           measure_target_type = ConfigSectionMapAdv(refference,'tcf_measure_target_type'),
           measure_target_name = ConfigSectionMapAdv(refference,'tcf_measure_target_name'),
           measure_target_description = ConfigSectionMapAdv(refference,'tcf_measure_target_description')  + " (LED: OFF)")
       tst.writerow(roff_rawl_line)
   if off_rawl is not None:
       goff_rawl_line = std_line(
           value = off_rawl[1],
           pin = ConfigSectionMapAdv(refference,'tcf_pin'),
           measure_name = ConfigSectionMapAdv('rgb colour','g_measure_name'),
           measure_sign = ConfigSectionMapAdv('rgb colour','measure_sign'),
           measure_type_full = ConfigSectionMapAdv('rgb colour','measure_type_full'),
           measure_type_abbr = ConfigSectionMapAdv('rgb colour','measure_type_abbr'),
           measure_absolute_min = ConfigSectionMapAdv('rgb colour','measure_absolute_min'),
           measure_absolute_max = off_rawl[3],
           measure_target_type = ConfigSectionMapAdv(refference,'tcf_measure_target_type'),
           measure_target_name = ConfigSectionMapAdv(refference,'tcf_measure_target_name'),
           measure_target_description = ConfigSectionMapAdv(refference,'tcf_measure_target_description')  + " (LED: OFF)")
       tst.writerow(goff_rawl_line)
   if off_rawl is not None:
       boff_rawl_line = std_line(
           value = off_rawl[2],
           pin = ConfigSectionMapAdv(refference,'tcf_pin'),
           measure_name = ConfigSectionMapAdv('rgb colour','b_measure_name'),
           measure_sign = ConfigSectionMapAdv('rgb colour','measure_sign'),
           measure_type_full = ConfigSectionMapAdv('rgb colour','measure_type_full'),
           measure_type_abbr = ConfigSectionMapAdv('rgb colour','measure_type_abbr'),
           measure_absolute_min = ConfigSectionMapAdv('rgb colour','measure_absolute_min'),
           measure_absolute_max = off_rawl[3],
           measure_target_type = ConfigSectionMapAdv(refference,'tcf_measure_target_type'),
           measure_target_name = ConfigSectionMapAdv(refference,'tcf_measure_target_name'),
           measure_target_description = ConfigSectionMapAdv(refference,'tcf_measure_target_description')  + " (LED: OFF)")
       tst.writerow(boff_rawl_line)
   if off_rawl is not None:
       coff_rawl_line = std_line(
           value = off_rawl[3],
           pin = ConfigSectionMapAdv(refference,'tcf_pin'),
           measure_name = ConfigSectionMapAdv('rgb colour','c_measure_name'),
           measure_sign = ConfigSectionMapAdv('rgb colour','measure_sign'),
           measure_type_full = ConfigSectionMapAdv('rgb colour','measure_type_full'),
           measure_type_abbr = ConfigSectionMapAdv('rgb colour','measure_type_abbr'),
           measure_absolute_min = ConfigSectionMapAdv('rgb colour','measure_absolute_min'),
           measure_absolute_max = ConfigSectionMapAdv('rgb colour','c_measure_absolute_max'),
           measure_target_type = ConfigSectionMapAdv(refference,'tcf_measure_target_type'),
           measure_target_name = ConfigSectionMapAdv(refference,'tcf_measure_target_name'),
           measure_target_description = ConfigSectionMapAdv(refference,'tcf_measure_target_description')  + " (LED: OFF)")
       tst.writerow(coff_rawl_line)
   if on_rawl is not None:
       ron_rawl_line = std_line(
           value = on_rawl[0],
           pin = ConfigSectionMapAdv(refference,'tcf_pin'),
           measure_name = ConfigSectionMapAdv('rgb colour','r_measure_name'),
           measure_sign = ConfigSectionMapAdv('rgb colour','measure_sign'),
           measure_type_full = ConfigSectionMapAdv('rgb colour','measure_type_full'),
           measure_type_abbr = ConfigSectionMapAdv('rgb colour','measure_type_abbr'),
           measure_absolute_min = ConfigSectionMapAdv('rgb colour','measure_absolute_min'),
           measure_absolute_max = on_rawl[3],
           measure_target_type = ConfigSectionMapAdv(refference,'tcf_measure_target_type'),
           measure_target_name = ConfigSectionMapAdv(refference,'tcf_measure_target_name'),
           measure_target_description = ConfigSectionMapAdv(refference,'tcf_measure_target_description')  + " (LED: ON)")
       tst.writerow(ron_rawl_line)
   if on_rawl is not None:
       gon_rawl_line = std_line(
           value = on_rawl[1],
           pin = ConfigSectionMapAdv(refference,'tcf_pin'),
           measure_name = ConfigSectionMapAdv('rgb colour','g_measure_name'),
           measure_sign = ConfigSectionMapAdv('rgb colour','measure_sign'),
           measure_type_full = ConfigSectionMapAdv('rgb colour','measure_type_full'),
           measure_type_abbr = ConfigSectionMapAdv('rgb colour','measure_type_abbr'),
           measure_absolute_min = ConfigSectionMapAdv('rgb colour','measure_absolute_min'),
           measure_absolute_max = on_rawl[3],
           measure_target_type = ConfigSectionMapAdv(refference,'tcf_measure_target_type'),
           measure_target_name = ConfigSectionMapAdv(refference,'tcf_measure_target_name'),
           measure_target_description = ConfigSectionMapAdv(refference,'tcf_measure_target_description')  + " (LED: ON)")
       tst.writerow(gon_rawl_line)
   if on_rawl is not None:
       bon_rawl_line = std_line(
           value = on_rawl[2],
           pin = ConfigSectionMapAdv(refference,'tcf_pin'),
           measure_name = ConfigSectionMapAdv('rgb colour','b_measure_name'),
           measure_sign = ConfigSectionMapAdv('rgb colour','measure_sign'),
           measure_type_full = ConfigSectionMapAdv('rgb colour','measure_type_full'),
           measure_type_abbr = ConfigSectionMapAdv('rgb colour','measure_type_abbr'),
           measure_absolute_min = ConfigSectionMapAdv('rgb colour','measure_absolute_min'),
           measure_absolute_max = on_rawl[3],
           measure_target_type = ConfigSectionMapAdv(refference,'tcf_measure_target_type'),
           measure_target_name = ConfigSectionMapAdv(refference,'tcf_measure_target_name'),
           measure_target_description = ConfigSectionMapAdv(refference,'tcf_measure_target_description')  + " (LED: ON)")
       tst.writerow(bon_rawl_line)
   if on_rawl is not None:
       con_rawl_line = std_line(
           value = on_rawl[3],
           pin = ConfigSectionMapAdv(refference,'tcf_pin'),
           measure_name = ConfigSectionMapAdv('rgb colour','c_measure_name'),
           measure_sign = ConfigSectionMapAdv('rgb colour','measure_sign'),
           measure_type_full = ConfigSectionMapAdv('rgb colour','measure_type_full'),
           measure_type_abbr = ConfigSectionMapAdv('rgb colour','measure_type_abbr'),
           measure_absolute_min = ConfigSectionMapAdv('rgb colour','measure_absolute_min'),
           measure_absolute_max = ConfigSectionMapAdv('rgb colour','c_measure_absolute_max'),
           measure_target_type = ConfigSectionMapAdv(refference,'tcf_measure_target_type'),
           measure_target_name = ConfigSectionMapAdv(refference,'tcf_measure_target_name'),
           measure_target_description = ConfigSectionMapAdv(refference,'tcf_measure_target_description')  + " (LED: ON)")
       tst.writerow(con_rawl_line)  
   if mgnm is not None:
       xmgnm_line = std_line(
           value = mgnm[0],
           pin = ConfigSectionMapAdv(refference,'lsm_pin'),
           measure_name = ConfigSectionMapAdv('magnetometer','measure_name'),
           measure_sign = ConfigSectionMapAdv('magnetometer','measure_sign'),
           measure_type_full = ConfigSectionMapAdv('magnetometer','x_measure_type_full'),
           measure_type_abbr = ConfigSectionMapAdv('magnetometer','x_measure_type_abbr'),
           measure_absolute_min = ConfigSectionMapAdv('magnetometer','measure_absolute_min'),
           measure_absolute_max = ConfigSectionMapAdv('magnetometer','measure_absolute_max'),
           measure_target_type = ConfigSectionMapAdv(refference,'lsm_measure_target_type'),
           measure_target_name = ConfigSectionMapAdv(refference,'lsm_measure_target_name'),
           measure_target_description = ConfigSectionMapAdv(refference,'lsm_measure_target_description'))
       tst.writerow(xmgnm_line)
   if mgnm is not None:
       ymgnm_line = std_line(
           value = mgnm[1],
           pin = ConfigSectionMapAdv(refference,'lsm_pin'),
           measure_name = ConfigSectionMapAdv('magnetometer','measure_name'),
           measure_sign = ConfigSectionMapAdv('magnetometer','measure_sign'),
           measure_type_full = ConfigSectionMapAdv('magnetometer','y_measure_type_full'),
           measure_type_abbr = ConfigSectionMapAdv('magnetometer','y_measure_type_abbr'),
           measure_absolute_min = ConfigSectionMapAdv('magnetometer','measure_absolute_min'),
           measure_absolute_max = ConfigSectionMapAdv('magnetometer','measure_absolute_max'), 
           measure_target_type = ConfigSectionMapAdv(refference,'lsm_measure_target_type'),
           measure_target_name = ConfigSectionMapAdv(refference,'lsm_measure_target_name'),
           measure_target_description = ConfigSectionMapAdv(refference,'lsm_measure_target_description'))
       tst.writerow(ymgnm_line)
   if mgnm is not None:
       zmgnm_line = std_line(
           value = mgnm[2],
           pin = ConfigSectionMapAdv(refference,'lsm_pin'),
           measure_name = ConfigSectionMapAdv('magnetometer','measure_name'),
           measure_sign = ConfigSectionMapAdv('magnetometer','measure_sign'),
           measure_type_full = ConfigSectionMapAdv('magnetometer','z_measure_type_full'),
           measure_type_abbr = ConfigSectionMapAdv('magnetometer','z_measure_type_abbr'),
           measure_absolute_min = ConfigSectionMapAdv('magnetometer','measure_absolute_min'),
           measure_absolute_max = ConfigSectionMapAdv('magnetometer','measure_absolute_max'),
           measure_target_type = ConfigSectionMapAdv(refference,'lsm_measure_target_type'),
           measure_target_name = ConfigSectionMapAdv(refference,'lsm_measure_target_name'),
           measure_target_description = ConfigSectionMapAdv(refference,'lsm_measure_target_description'))
       tst.writerow(zmgnm_line)
   if acclm is not None:
       xacclm_line = std_line(
           value = acclm[0],
           pin = ConfigSectionMapAdv(refference,'lsm_pin'),
           measure_name = ConfigSectionMapAdv('accelerometer','measure_name'),
           measure_sign = ConfigSectionMapAdv('accelerometer','measure_sign'),
           measure_type_full = ConfigSectionMapAdv('accelerometer','x_measure_type_full'),
           measure_type_abbr = ConfigSectionMapAdv('accelerometer','x_measure_type_abbr'),
           measure_absolute_min = ConfigSectionMapAdv('accelerometer','measure_absolute_min'),
           measure_absolute_max = ConfigSectionMapAdv('accelerometer','measure_absolute_max'),
           measure_target_type = ConfigSectionMapAdv(refference,'lsm_measure_target_type'),
           measure_target_name = ConfigSectionMapAdv(refference,'lsm_measure_target_name'),
           measure_target_description = ConfigSectionMapAdv(refference,'lsm_measure_target_description'))
       tst.writerow(xacclm_line)
   if acclm is not None:
       yacclm_line = std_line(
           value = acclm[1],
           pin = ConfigSectionMapAdv(refference,'lsm_pin'),
           measure_name = ConfigSectionMapAdv('accelerometer','measure_name'),
           measure_sign = ConfigSectionMapAdv('accelerometer','measure_sign'),
           measure_type_full = ConfigSectionMapAdv('accelerometer','y_measure_type_full'),
           measure_type_abbr = ConfigSectionMapAdv('accelerometer','y_measure_type_abbr'),
           measure_absolute_min = ConfigSectionMapAdv('accelerometer','measure_absolute_min'),
           measure_absolute_max = ConfigSectionMapAdv('accelerometer','measure_absolute_max'), 
           measure_target_type = ConfigSectionMapAdv(refference,'lsm_measure_target_type'),
           measure_target_name = ConfigSectionMapAdv(refference,'lsm_measure_target_name'),
           measure_target_description = ConfigSectionMapAdv(refference,'lsm_measure_target_description'))
       tst.writerow(yacclm_line)
   if acclm is not None:
       zacclm_line = std_line(
           value = acclm[2],
           pin = ConfigSectionMapAdv(refference,'lsm_pin'),
           measure_name = ConfigSectionMapAdv('accelerometer','measure_name'),
           measure_sign = ConfigSectionMapAdv('accelerometer','measure_sign'),
           measure_type_full = ConfigSectionMapAdv('accelerometer','z_measure_type_full'),
           measure_type_abbr = ConfigSectionMapAdv('accelerometer','z_measure_type_abbr'),
           measure_absolute_min = ConfigSectionMapAdv('accelerometer','measure_absolute_min'),
           measure_absolute_max = ConfigSectionMapAdv('accelerometer','measure_absolute_max'),
           measure_target_type = ConfigSectionMapAdv(refference,'lsm_measure_target_type'),
           measure_target_name = ConfigSectionMapAdv(refference,'lsm_measure_target_name'),
           measure_target_description = ConfigSectionMapAdv(refference,'lsm_measure_target_description'))
       tst.writerow(zacclm_line)
      

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
    print "ERROR @ transfere"
