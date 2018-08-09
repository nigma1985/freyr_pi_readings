#!/usr/bin/python

# This script develops a python script to read and write envirophat data
# -*- coding: utf-8 -*-

from __future__ import division
#from envirophat import light, motion, weather, analog, leds
import os
#from subprocess import PIPE, Popen
import subprocess, platform
#import psutil ## install python-psutil
import sys
#import Adafruit_DHT
#import datetime
#from datetime import datetime
#from datetime import timedelta
#import time
import re
#import sqlite3 as lite
#import csv
#import unicodecsv as csv
#import random
#import ConfigParser ## https://wiki.python.org/moin/ConfigParserExamples

################################################################################

import module.config as ini ## https://wiki.python.org/moin/ConfigParserExamples
import module.decision as dec
import module.getOptions as opt
import module.timeTools as ttl
import module.netTools as ntt
import module.freyr.csvBuffer as bfr
import module.read.enviroPHAT as env ## https://github.com/pimoroni/enviro-phat
from module.freyr import findConfig
from module import mean
import os

refference = "Enviro pHAT"
# csv_name = sys.argv[1]
# refference = "Enviro pHAT"

## reading 'freyr_config.ini'
configFile = "freyr_config.ini"
config = ini.getConfig(configFile)
# ini = "freyr_config.ini"
# config = ConfigParser.SafeConfigParser()
# config.read(ini)


me = findConfig(sysKey = "me", confSection = refference, confOption = 'source_name', confFile = config)
my_user = findConfig(sysKey = "my_user", confSection = refference, confOption = 'user', confFile = config)
# me = ConfigSectionMapAdv("Sys",'source_name')
# my_user = ConfigSectionMapAdv("Sys",'user')

# _input = sys.argv
# csv_name = _csvName(_input, me)
all_on = opt.findItm("ALLON")
all_off = opt.findItm("ALLOFF")
led_on = opt.findItm("LEDON")
led_off = opt.findItm("LEDOFF")
# all_on = _findItm(_input, "ALLON")
# all_off = _findItm(_input, "ALLOFF")

# led_on = _findItm(_input, "LEDON")
# led_off = _findItm(_input, "LEDOFF")
# rgb_on = _findItm(_input, "RGBON")
# rgb_off = _findItm(_input, "RGBOFF")
# lgt_on = _findItm(_input, "LGTON")
# lgt_off = _findItm(_input, "LGTOFF")
# raw_on = _findItm(_input, "RAWON")
# raw_off = _findItm(_input, "RAWOFF")

sleeptimer = (1.0 / 3.0) * 2.0

## lights via TCS3472

led_light = dec.decision(
    onSwitch = [all_on, led_on, "LGTON"],
    offSwitch = [all_off, led_off, "LGTOFF"],
    numChance = findConfig(sysKey = "LGT", confSection = refference, confOption = 'led_light', confFile = config))

led_rgb = dec.decision(
    onSwitch = [all_on, led_on, "RGBON"],
    offSwitch = [all_off, led_off, "RGBOFF"],
    numChance = findConfig(sysKey = "RGB", confSection = refference, confOption = 'led_rgb', confFile = config))

led_raw = dec.decision(
    onSwitch = [all_on, led_on, "RAWON"],
    offSwitch = [all_off, led_off, "RAWOFF"],
    numChance = findConfig(sysKey = "RAW", confSection = refference, confOption = 'led_raw', confFile = config))

rec_light = dec.decision(
    onSwitch = [all_on, led_off, "LGTON"],
    offSwitch = [all_off, led_on, "LGTOFF"],
    numChance = findConfig(sysKey = "LGT", confSection = refference, confOption = 'rec_light', confFile = config))

rec_rgb = dec.decision(
    onSwitch = [all_on, led_off, "RGBON"],
    offSwitch = [all_off, led_on, "RGBOFF"],
    numChance = findConfig(sysKey = "RGB", confSection = refference, confOption = 'rec_rgb', confFile = config))

rec_raw = dec.decision(
    onSwitch = [all_on, led_off, "RAWON"],
    offSwitch = [all_off, led_on, "RAWOFF"],
    numChance = findConfig(sysKey = "RAW", confSection = refference, confOption = 'rec_raw', confFile = config))


## weather via BMP280

rec_temp = dec.decision(
    onSwitch = [all_on, "TMPON"],
    offSwitch = [all_off, "TMPOFF"],
    numChance = findConfig(sysKey = "TMP", confSection = refference, confOption = 'rec_temp', confFile = config))

rec_prss = dec.decision(
    onSwitch = [all_on, "PRSON"],
    offSwitch = [all_off, "PRSOFF"],
    numChance = findConfig(sysKey = "PRS", confSection = refference, confOption = 'rec_prss', confFile = config))

rec_altd_qnh = dec.decision(
    onSwitch = [all_on, "QNHON"],
    offSwitch = [all_off, "QNHOFF"],
    numChance = findConfig(sysKey = "QNH", confSection = refference, confOption = 'rec_altd_qnh', confFile = config))

rec_altd = dec.decision(
    onSwitch = [all_on, "ALTON"],
    offSwitch = [all_off, "ALTOFF"],
    numChance = findConfig(sysKey = "ALT", confSection = refference, confOption = 'rec_altd', confFile = config))

# weather.update()


## motion via LSM303D

rec_mgnm = dec.decision(
    onSwitch = [all_on, "MGMON"],
    offSwitch = [all_off, "MGMOFF"],
    numChance = findConfig(sysKey = "MGM", confSection = refference, confOption = 'rec_mgnm', confFile = config))

rec_acclm = dec.decision(
    onSwitch = [all_on, "ACCON"],
    offSwitch = [all_off, "ACCOFF"],
    numChance = findConfig(sysKey = "ACC", confSection = refference, confOption = 'rec_acclm', confFile = config))

rec_headng = dec.decision(
    onSwitch = [all_on, "HDON"],
    offSwitch = [all_off, "HDOFF"],
    numChance = findConfig(sysKey = "HD", confSection = refference, confOption = 'rec_headng', confFile = config))

rec_rawheadng = dec.decision(
    onSwitch = [all_on, "RHDON"],
    offSwitch = [all_off, "RHDOFF"],
    numChance = findConfig(sysKey = "RHD", confSection = refference, confOption = 'rec_rawheadng', confFile = config))


#################################################
#################################################
#################################################




# Try to grab a sensor reading.  Use the read_retry method which will retry up
now1, utc1, nowsecs = ttl.start()

## lights via TCS3472
off_light = None
off_rgb = None
off_rawl = None
if led_light == False and rec_light == True:
    off_light = env.getLight()
if (led_rgb == False and rec_rgb == True) and off_light > 5:
    off_rgb = env.getRGB()
if led_raw == False and rec_raw == True:
    off_rawl = env.getRaw()

on_light = None
on_rgb = None
on_rawl = None
if (led_light == True and rec_light == True) or (led_rgb == True and rec_rgb == True) or (led_raw == True and rec_raw == True):
    env.setLedOn()
    time.sleep(sleeptimer)
    if rec_light == True:
        on_light = env.getLight()
    if rec_rgb == True:
        on_rgb = env.getRGB()
    if rec_raw == True:
        on_rawl = env.getRaw()
    env.setLedOff()
    # time.sleep(sleeptimer)


## motion via LSM303D
mgnm = None
acclm = None
headng = None
rawheadng = None
if rec_mgnm == True:
    mgnm = env.getMagn()
if rec_acclm == True:
    acclm = env.getAccl()
if rec_headng == True:
    headng = env.getHead()
if rec_rawheadng == True:
    rawheadng = env.getRawHead()
#print env.getMotionUpdate()


## Analog via ADS1015
#analog = None


## weather via BMP280
temp = None
prss = None
prss_sl = None
altd_qnh = None
altd = None
if rec_temp == True:
    temp = env.getTemp()
if rec_prss == True:
    prss = env.getPrss()
if rec_altd_qnh == True:
    prss_sl = findConfig(sysKey = "hpa_sea_level", confSection = refference, confOption = 'hpa_sea_level', confFile = config)
    altd_qnh == env.getAltd(qnh = prss_sl)
if rec_altd == True:
    altd = env.getAltd()
# env.getWeatherUpdate()
## No analog reading interpreted


utc2, offset_utc, duration, duration2 = ttl.end(now1, utc1)


def _stdLine(
    value = 0.0,
    pin = None,
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
