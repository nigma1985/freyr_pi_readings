#!/usr/bin/python

# This script develops a python script to read and write envirophat data
# -*- coding: utf-8 -*-

import module.config as ini ## https://wiki.python.org/moin/ConfigParserExamples
import module.decision as dec
import module.getOptions as opt
import module.timeTools as ttl
import module.netTools as ntt
import module.freyr.csvBuffer as bfr
import module.read.enviroPHAT as env ## https://github.com/pimoroni/enviro-phat
from module.freyr import findConfig

refference = "Enviro pHAT"

configFile = "freyr_config.ini"
config = ini.getConfig(configFile)

me = findConfig(sysKey = "me", confSection = "Sys", confOption = 'source_name', confFile = config)
my_user = findConfig(sysKey = "my_user", confSection = "Sys", confOption = 'user', confFile = config)

all_on = opt.findItm("ALLON")
all_off = opt.findItm("ALLOFF")
led_on = opt.findItm("LEDON")
led_off = opt.findItm("LEDOFF")

sleeptimer = (1.0 / 3.0) * 2.0

# SWITCHES
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
    ttl.sleeper(timer = sleeptimer)
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

# WRITING
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

csv_name = bfr.csvName(me)
bfr.initiateFile(csv_name)
if off_light is not None:
    bfr.writeRow(row = _stdLine(
           value = off_light,
           pin = findConfig(sysKey = "off_lightPin", confSection = refference, confOption = 'tcf_pin', confFile = config),
           measure_name = findConfig(sysKey = "off_light_measure_name", confSection = "light level", confOption = 'measure_name', confFile = config),
           measure_sign = findConfig(sysKey = "off_light_measure_sign", confSection = "light level", confOption = 'measure_sign', confFile = config),
           measure_type_full = findConfig(sysKey = "off_light_measure_type_full", confSection = "light level", confOption = 'measure_type_full', confFile = config),
           measure_type_abbr = findConfig(sysKey = "off_light_measure_type_abbr", confSection = "light level", confOption = 'measure_type_abbr', confFile = config),
           measure_absolute_min = findConfig(sysKey = "off_light_measure_absolute_min", confSection = "light level", confOption = 'measure_absolute_min', confFile = config),
           measure_absolute_max = findConfig(sysKey = "off_light_measure_absolute_max", confSection = "light level", confOption = 'measure_absolute_max', confFile = config),
           measure_target_type = findConfig(sysKey = "off_light_tcf_measure_target_type", confSection = refference, confOption = 'tcf_measure_target_type', confFile = config),
           measure_target_name = findConfig(sysKey = "off_light_tcf_measure_target_name", confSection = refference, confOption = 'tcf_measure_target_name', confFile = config),
           measure_target_description = findConfig(sysKey = "off_light_tcf_measure_target_description", confSection = refference, confOption = 'tcf_measure_target_description', confFile = config) + " (LED: OFF)"
           ), csvFile = csv_name)
if on_light is not None:
    bfr.writeRow(row = _stdLine(
           value = on_light,
           pin = findConfig(sysKey = "on_lightPin", confSection = refference, confOption = 'tcf_pin', confFile = config),
           measure_name = findConfig(sysKey = "on_light_measure_name", confSection = "light level", confOption = 'measure_name', confFile = config),
           measure_sign = findConfig(sysKey = "on_light_measure_sign", confSection = "light level", confOption = 'measure_sign', confFile = config),
           measure_type_full = findConfig(sysKey = "on_light_measure_type_full", confSection = "light level", confOption = 'measure_type_full', confFile = config),
           measure_type_abbr = findConfig(sysKey = "on_light_measure_type_abbr", confSection = "light level", confOption = 'measure_type_abbr', confFile = config),
           measure_absolute_min = findConfig(sysKey = "on_light_measure_absolute_min", confSection = "light level", confOption = 'measure_absolute_min', confFile = config),
           measure_absolute_max = findConfig(sysKey = "on_light_measure_absolute_max", confSection = "light level", confOption = 'measure_absolute_max', confFile = config),
           measure_target_type = findConfig(sysKey = "on_light_tcf_measure_target_type", confSection = refference, confOption = 'tcf_measure_target_type', confFile = config),
           measure_target_name = findConfig(sysKey = "on_light_tcf_measure_target_name", confSection = refference, confOption = 'tcf_measure_target_name', confFile = config),
           measure_target_description = findConfig(sysKey = "on_light_tcf_measure_target_description", confSection = refference, confOption = 'tcf_measure_target_description', confFile = config) + " (LED: ON)"
           ), csvFile = csv_name)

if temp is not None:
    bfr.writeRow(row = _stdLine(
           value = temp,
           pin = findConfig(sysKey = "tempPin", confSection = refference, confOption = 'bmp_pin', confFile = config),
           measure_name = findConfig(sysKey = "tempMeasure_name", confSection = "tmp_celsius", confOption = 'measure_name', confFile = config),
           measure_sign = findConfig(sysKey = "tempMeasure_sign", confSection = "tmp_celsius", confOption = 'measure_sign', confFile = config),
           measure_type_full = findConfig(sysKey = "tempMeasure_type_full", confSection = "tmp_celsius", confOption = 'measure_type_full', confFile = config),
           measure_type_abbr = findConfig(sysKey = "tempMeasure_type_abbr", confSection = "tmp_celsius", confOption = 'measure_type_abbr', confFile = config),
           measure_absolute_min = findConfig(sysKey = "tempMeasure_absolute_min", confSection = "tmp_celsius", confOption = 'measure_absolute_min', confFile = config),
           measure_absolute_max = findConfig(sysKey = "tempMeasure_absolute_max", confSection = "tmp_celsius", confOption = 'measure_absolute_max', confFile = config),
           measure_target_type = findConfig(sysKey = "tempMeasure_target_type", confSection = refference, confOption = 'bmp_measure_target_type', confFile = config),
           measure_target_name = findConfig(sysKey = "tempMeasure_target_name", confSection = refference, confOption = 'bmp_measure_target_name', confFile = config),
           measure_target_description = findConfig(sysKey = "tempMeasure_target_description", confSection = refference, confOption = 'bmp_measure_target_description', confFile = config)
           ), csvFile = csv_name)
if prss is not None:
    bfr.writeRow(row = _stdLine(
           value = prss,
           pin = findConfig(sysKey = "prssPin", confSection = refference, confOption = 'bmp_pin', confFile = config),
           measure_name = findConfig(sysKey = "prssMeasure_name", confSection = "pressure_pa", confOption = 'measure_name', confFile = config),
           measure_sign = findConfig(sysKey = "prssMeasure_sign", confSection = "pressure_pa", confOption = 'measure_sign', confFile = config),
           measure_type_full = findConfig(sysKey = "prssMeasure_type_full", confSection = "pressure_pa", confOption = 'measure_type_full', confFile = config),
           measure_type_abbr = findConfig(sysKey = "prssMeasure_type_abbr", confSection = "pressure_pa", confOption = 'measure_type_abbr', confFile = config),
           measure_absolute_min = findConfig(sysKey = "prssMeasure_absolute_min", confSection = "pressure_pa", confOption = 'measure_absolute_min', confFile = config),
           measure_absolute_max = findConfig(sysKey = "prssMeasure_absolute_max", confSection = "pressure_pa", confOption = 'measure_absolute_max', confFile = config),
           measure_target_type = findConfig(sysKey = "prssMeasure_target_type", confSection = refference, confOption = 'bmp_measure_target_type', confFile = config),
           measure_target_name = findConfig(sysKey = "prssMeasure_target_name", confSection = refference, confOption = 'bmp_measure_target_name', confFile = config),
           measure_target_description = findConfig(sysKey = "prssMeasure_target_description", confSection = refference, confOption = 'bmp_measure_target_description', confFile = config)
           ), csvFile = csv_name)
if altd is not None:
    bfr.writeRow(row = _stdLine(
           value = altd,
           pin = findConfig(sysKey = "altdPin", confSection = refference, confOption = 'bmp_pin', confFile = config),
           measure_name = findConfig(sysKey = "altdMeasure_name", confSection = "altitude", confOption = 'measure_name', confFile = config),
           measure_sign = findConfig(sysKey = "altdMeasure_sign", confSection = "altitude", confOption = 'measure_sign', confFile = config),
           measure_type_full = findConfig(sysKey = "altdMeasure_type_full", confSection = "altitude", confOption = 'measure_type_full', confFile = config),
           measure_type_abbr = findConfig(sysKey = "altdMeasure_type_abbr", confSection = "altitude", confOption = 'measure_type_abbr', confFile = config),
           measure_absolute_min = findConfig(sysKey = "altdMeasure_absolute_min", confSection = "altitude", confOption = 'measure_absolute_min', confFile = config),
           measure_absolute_max = findConfig(sysKey = "altdMeasure_absolute_max", confSection = "altitude", confOption = 'measure_absolute_max', confFile = config),
           measure_target_type = findConfig(sysKey = "altdMeasure_target_type", confSection = refference, confOption = 'bmp_measure_target_type', confFile = config),
           measure_target_name = findConfig(sysKey = "altdMeasure_target_name", confSection = refference, confOption = 'bmp_measure_target_name', confFile = config),
           measure_target_description = findConfig(sysKey = "altdMeasure_target_description", confSection = refference, confOption = 'bmp_measure_target_description', confFile = config)
           ), csvFile = csv_name)
if altd_qnh is not None and prss_sl is not None:
    bfr.writeRow(row = _stdLine(
           value = altd_qnh,
           pin = findConfig(sysKey = "altd_qnhPin", confSection = refference, confOption = 'bmp_pin', confFile = config),
           measure_name = findConfig(sysKey = "altd_qnhMeasure_name", confSection = "altitude", confOption = 'measure_name', confFile = config),
           measure_sign = findConfig(sysKey = "altd_qnhMeasure_sign", confSection = "altitude", confOption = 'measure_sign', confFile = config),
           measure_type_full = findConfig(sysKey = "altd_qnhMeasure_type_full", confSection = "altitude", confOption = 'measure_type_full', confFile = config),
           measure_type_abbr = findConfig(sysKey = "altd_qnhMeasure_type_abbr", confSection = "altitude", confOption = 'measure_type_abbr', confFile = config),
           measure_absolute_min = findConfig(sysKey = "altd_qnhMeasure_absolute_min", confSection = "altitude", confOption = 'measure_absolute_min', confFile = config),
           measure_absolute_max = findConfig(sysKey = "altd_qnhMeasure_absolute_max", confSection = "altitude", confOption = 'measure_absolute_max', confFile = config),
           measure_target_type = findConfig(sysKey = "altd_qnhMeasure_target_type", confSection = refference, confOption = 'bmp_measure_target_type', confFile = config),
           measure_target_name = findConfig(sysKey = "altd_qnhMeasure_target_name", confSection = refference, confOption = 'bmp_measure_target_name', confFile = config),
           measure_target_description = findConfig(sysKey = "altd_qnhMeasure_target_description", confSection = refference, confOption = 'bmp_measure_target_description', confFile = config) + " (Air Pressure at Sea Level = " + str(prss_sl) + " hPa)"
           ), csvFile = csv_name)

if headng is not None:
    bfr.writeRow(row = _stdLine(
           value = headng,
           pin = findConfig(sysKey = "headngPin", confSection = refference, confOption = 'lsm_pin', confFile = config),
           measure_name = findConfig(sysKey = "headngMeasure_name", confSection = "heading", confOption = 'measure_name', confFile = config),
           measure_sign = findConfig(sysKey = "headngMeasure_sign", confSection = "heading", confOption = 'measure_sign', confFile = config),
           measure_type_full = findConfig(sysKey = "headngMeasure_type_full", confSection = "heading", confOption = 'measure_type_full', confFile = config),
           measure_type_abbr = findConfig(sysKey = "headngMeasure_type_abbr", confSection = "heading", confOption = 'measure_type_abbr', confFile = config),
           measure_absolute_min = findConfig(sysKey = "headngMeasure_absolute_min", confSection = "heading", confOption = 'measure_absolute_min', confFile = config),
           measure_absolute_max = findConfig(sysKey = "headngMeasure_absolute_max", confSection = "heading", confOption = 'measure_absolute_max', confFile = config),
           measure_target_type = findConfig(sysKey = "headngMeasure_target_type", confSection = refference, confOption = 'bmp_measure_target_type', confFile = config),
           measure_target_name = findConfig(sysKey = "headngMeasure_target_name", confSection = refference, confOption = 'bmp_measure_target_name', confFile = config),
           measure_target_description = findConfig(sysKey = "headngMeasure_target_description", confSection = refference, confOption = 'bmp_measure_target_description', confFile = config)
           ), csvFile = csv_name)
if rawheadng is not None:
    bfr.writeRow(row = _stdLine(
           value = rawheadng,
           pin = findConfig(sysKey = "rawheadngPin", confSection = refference, confOption = 'lsm_pin', confFile = config),
           measure_name = findConfig(sysKey = "rawheadngMeasure_name", confSection = "raw heading", confOption = 'measure_name', confFile = config),
           measure_sign = findConfig(sysKey = "rawheadngMeasure_sign", confSection = "raw heading", confOption = 'measure_sign', confFile = config),
           measure_type_full = findConfig(sysKey = "rawheadngMeasure_type_full", confSection = "raw heading", confOption = 'measure_type_full', confFile = config),
           measure_type_abbr = findConfig(sysKey = "rawheadngMeasure_type_abbr", confSection = "raw heading", confOption = 'measure_type_abbr', confFile = config),
           measure_absolute_min = findConfig(sysKey = "rawheadngMeasure_absolute_min", confSection = "raw heading", confOption = 'measure_absolute_min', confFile = config),
           measure_absolute_max = findConfig(sysKey = "rawheadngMeasure_absolute_max", confSection = "raw heading", confOption = 'measure_absolute_max', confFile = config),
           measure_target_type = findConfig(sysKey = "rawheadngMeasure_target_type", confSection = refference, confOption = 'lsm_measure_target_type', confFile = config),
           measure_target_name = findConfig(sysKey = "rawheadngMeasure_target_name", confSection = refference, confOption = 'lsm_measure_target_name', confFile = config),
           measure_target_description = findConfig(sysKey = "rawheadngMeasure_target_description", confSection = refference, confOption = 'lsm_measure_target_description', confFile = config)
           ), csvFile = csv_name)

if off_rgb is not None:
    bfr.writeRow(row = _stdLine(
        value = off_rgb[0],
        pin = findConfig(sysKey = "off_rgbPin", confSection = refference, confOption = 'tcf_pin', confFile = config),
        measure_name = findConfig(sysKey = "off_rgbMeasure_name", confSection = "rgb colour", confOption = 'r_measure_name', confFile = config),
        measure_sign = findConfig(sysKey = "off_rgbMeasure_sign", confSection = "rgb colour", confOption = 'measure_sign', confFile = config),
        measure_type_full = findConfig(sysKey = "off_rgbMeasure_type_full", confSection = "rgb colour", confOption = 'measure_type_full', confFile = config),
        measure_type_abbr = findConfig(sysKey = "off_rgbMeasure_type_abbr", confSection = "rgb colour", confOption = 'measure_type_abbr', confFile = config),
        measure_absolute_min = findConfig(sysKey = "off_rgbMeasure_absolute_min", confSection = "rgb colour", confOption = 'measure_absolute_min', confFile = config),
        measure_absolute_max = findConfig(sysKey = "off_rgbMeasure_absolute_max", confSection = "rgb colour", confOption = 'measure_absolute_max', confFile = config),
        measure_target_type = findConfig(sysKey = "off_rgbMeasure_target_type", confSection = refference, confOption = 'tcf_measure_target_type', confFile = config),
        measure_target_name = findConfig(sysKey = "off_rgbMeasure_target_name", confSection = refference, confOption = 'tcf_measure_target_name', confFile = config),
        measure_target_description = findConfig(sysKey = "off_rgbMeasure_target_description", confSection = refference, confOption = 'tcf_measure_target_description', confFile = config) + " (LED: OFF)"
        ), csvFile = csv_name)
    bfr.writeRow(row = _stdLine(
        value = off_rgb[1],
        pin = findConfig(sysKey = "off_rgbPin", confSection = refference, confOption = 'tcf_pin', confFile = config),
        measure_name = findConfig(sysKey = "off_rgbMeasure_name", confSection = "rgb colour", confOption = 'g_measure_name', confFile = config),
        measure_sign = findConfig(sysKey = "off_rgbMeasure_sign", confSection = "rgb colour", confOption = 'measure_sign', confFile = config),
        measure_type_full = findConfig(sysKey = "off_rgbMeasure_type_full", confSection = "rgb colour", confOption = 'measure_type_full', confFile = config),
        measure_type_abbr = findConfig(sysKey = "off_rgbMeasure_type_abbr", confSection = "rgb colour", confOption = 'measure_type_abbr', confFile = config),
        measure_absolute_min = findConfig(sysKey = "off_rgbMeasure_absolute_min", confSection = "rgb colour", confOption = 'measure_absolute_min', confFile = config),
        measure_absolute_max = findConfig(sysKey = "off_rgbMeasure_absolute_max", confSection = "rgb colour", confOption = 'measure_absolute_max', confFile = config),
        measure_target_type = findConfig(sysKey = "off_rgbMeasure_target_type", confSection = refference, confOption = 'tcf_measure_target_type', confFile = config),
        measure_target_name = findConfig(sysKey = "off_rgbMeasure_target_name", confSection = refference, confOption = 'tcf_measure_target_name', confFile = config),
        measure_target_description = findConfig(sysKey = "off_rgbMeasure_target_description", confSection = refference, confOption = 'tcf_measure_target_description', confFile = config) + " (LED: OFF)"
        ), csvFile = csv_name)
    bfr.writeRow(row = _stdLine(
        value = off_rgb[2],
        pin = findConfig(sysKey = "off_rgbPin", confSection = refference, confOption = 'tcf_pin', confFile = config),
        measure_name = findConfig(sysKey = "off_rgbMeasure_name", confSection = "rgb colour", confOption = 'b_measure_name', confFile = config),
        measure_sign = findConfig(sysKey = "off_rgbMeasure_sign", confSection = "rgb colour", confOption = 'measure_sign', confFile = config),
        measure_type_full = findConfig(sysKey = "off_rgbMeasure_type_full", confSection = "rgb colour", confOption = 'measure_type_full', confFile = config),
        measure_type_abbr = findConfig(sysKey = "off_rgbMeasure_type_abbr", confSection = "rgb colour", confOption = 'measure_type_abbr', confFile = config),
        measure_absolute_min = findConfig(sysKey = "off_rgbMeasure_absolute_min", confSection = "rgb colour", confOption = 'measure_absolute_min', confFile = config),
        measure_absolute_max = findConfig(sysKey = "off_rgbMeasure_absolute_max", confSection = "rgb colour", confOption = 'measure_absolute_max', confFile = config),
        measure_target_type = findConfig(sysKey = "off_rgbMeasure_target_type", confSection = refference, confOption = 'tcf_measure_target_type', confFile = config),
        measure_target_name = findConfig(sysKey = "off_rgbMeasure_target_name", confSection = refference, confOption = 'tcf_measure_target_name', confFile = config),
        measure_target_description = findConfig(sysKey = "off_rgbMeasure_target_description", confSection = refference, confOption = 'tcf_measure_target_description', confFile = config) + " (LED: OFF)"
        ), csvFile = csv_name)
if on_rgb is not None:
    bfr.writeRow(row = _stdLine(
        value = on_rgb[0],
        pin = findConfig(sysKey = "on_rgbPin", confSection = refference, confOption = 'tcf_pin', confFile = config),
        measure_name = findConfig(sysKey = "on_rgbMeasure_name", confSection = "rgb colour", confOption = 'r_measure_name', confFile = config),
        measure_sign = findConfig(sysKey = "on_rgbMeasure_sign", confSection = "rgb colour", confOption = 'measure_sign', confFile = config),
        measure_type_full = findConfig(sysKey = "on_rgbMeasure_type_full", confSection = "rgb colour", confOption = 'measure_type_full', confFile = config),
        measure_type_abbr = findConfig(sysKey = "on_rgbMeasure_type_abbr", confSection = "rgb colour", confOption = 'measure_type_abbr', confFile = config),
        measure_absolute_min = findConfig(sysKey = "on_rgbMeasure_absolute_min", confSection = "rgb colour", confOption = 'measure_absolute_min', confFile = config),
        measure_absolute_max = findConfig(sysKey = "on_rgbMeasure_absolute_max", confSection = "rgb colour", confOption = 'measure_absolute_max', confFile = config),
        measure_target_type = findConfig(sysKey = "on_rgbMeasure_target_type", confSection = refference, confOption = 'tcf_measure_target_type', confFile = config),
        measure_target_name = findConfig(sysKey = "on_rgbMeasure_target_name", confSection = refference, confOption = 'tcf_measure_target_name', confFile = config),
        measure_target_description = findConfig(sysKey = "on_rgbMeasure_target_description", confSection = refference, confOption = 'tcf_measure_target_description', confFile = config) + " (LED: ON)"
        ), csvFile = csv_name)
    bfr.writeRow(row = _stdLine(
        value = on_rgb[1],
        pin = findConfig(sysKey = "on_rgbPin", confSection = refference, confOption = 'tcf_pin', confFile = config),
        measure_name = findConfig(sysKey = "on_rgbMeasure_name", confSection = "rgb colour", confOption = 'g_measure_name', confFile = config),
        measure_sign = findConfig(sysKey = "on_rgbMeasure_sign", confSection = "rgb colour", confOption = 'measure_sign', confFile = config),
        measure_type_full = findConfig(sysKey = "on_rgbMeasure_type_full", confSection = "rgb colour", confOption = 'measure_type_full', confFile = config),
        measure_type_abbr = findConfig(sysKey = "on_rgbMeasure_type_abbr", confSection = "rgb colour", confOption = 'measure_type_abbr', confFile = config),
        measure_absolute_min = findConfig(sysKey = "on_rgbMeasure_absolute_min", confSection = "rgb colour", confOption = 'measure_absolute_min', confFile = config),
        measure_absolute_max = findConfig(sysKey = "on_rgbMeasure_absolute_max", confSection = "rgb colour", confOption = 'measure_absolute_max', confFile = config),
        measure_target_type = findConfig(sysKey = "on_rgbMeasure_target_type", confSection = refference, confOption = 'tcf_measure_target_type', confFile = config),
        measure_target_name = findConfig(sysKey = "on_rgbMeasure_target_name", confSection = refference, confOption = 'tcf_measure_target_name', confFile = config),
        measure_target_description = findConfig(sysKey = "on_rgbMeasure_target_description", confSection = refference, confOption = 'tcf_measure_target_description', confFile = config) + " (LED: ON)"
        ), csvFile = csv_name)
    bfr.writeRow(row = _stdLine(
        value = on_rgb[2],
        pin = findConfig(sysKey = "on_rgbPin", confSection = refference, confOption = 'tcf_pin', confFile = config),
        measure_name = findConfig(sysKey = "on_rgbMeasure_name", confSection = "rgb colour", confOption = 'b_measure_name', confFile = config),
        measure_sign = findConfig(sysKey = "on_rgbMeasure_sign", confSection = "rgb colour", confOption = 'measure_sign', confFile = config),
        measure_type_full = findConfig(sysKey = "on_rgbMeasure_type_full", confSection = "rgb colour", confOption = 'measure_type_full', confFile = config),
        measure_type_abbr = findConfig(sysKey = "on_rgbMeasure_type_abbr", confSection = "rgb colour", confOption = 'measure_type_abbr', confFile = config),
        measure_absolute_min = findConfig(sysKey = "on_rgbMeasure_absolute_min", confSection = "rgb colour", confOption = 'measure_absolute_min', confFile = config),
        measure_absolute_max = findConfig(sysKey = "on_rgbMeasure_absolute_max", confSection = "rgb colour", confOption = 'measure_absolute_max', confFile = config),
        measure_target_type = findConfig(sysKey = "on_rgbMeasure_target_type", confSection = refference, confOption = 'tcf_measure_target_type', confFile = config),
        measure_target_name = findConfig(sysKey = "on_rgbMeasure_target_name", confSection = refference, confOption = 'tcf_measure_target_name', confFile = config),
        measure_target_description = findConfig(sysKey = "on_rgbMeasure_target_description", confSection = refference, confOption = 'tcf_measure_target_description', confFile = config) + " (LED: ON)"
        ), csvFile = csv_name)

if off_rawl is not None:
    bfr.writeRow(row = _stdLine(
        value = off_rawl[0],
        pin = findConfig(sysKey = "off_rawlPin", confSection = refference, confOption = 'tcf_pin', confFile = config),
        measure_name = findConfig(sysKey = "off_rawlMeasure_name", confSection = "rgb colour", confOption = 'r_measure_name', confFile = config),
        measure_sign = findConfig(sysKey = "off_rawlMeasure_sign", confSection = "rgb colour", confOption = 'measure_sign', confFile = config),
        measure_type_full = findConfig(sysKey = "off_rawlMeasure_type_full", confSection = "rgb colour", confOption = 'measure_type_full', confFile = config),
        measure_type_abbr = findConfig(sysKey = "off_rawlMeasure_type_abbr", confSection = "rgb colour", confOption = 'measure_type_abbr', confFile = config),
        measure_absolute_min = findConfig(sysKey = "off_rawlMeasure_absolute_min", confSection = "rgb colour", confOption = 'measure_absolute_min', confFile = config),
        measure_absolute_max = findConfig(sysKey = "off_rawlMeasure_absolute_max", readVar = off_rawl[3], confSection = "rgb colour", confOption = 'measure_absolute_max', confFile = config),
        measure_target_type = findConfig(sysKey = "off_rawlMeasure_target_type", confSection = refference, confOption = 'tcf_measure_target_type', confFile = config),
        measure_target_name = findConfig(sysKey = "off_rawlMeasure_target_name", confSection = refference, confOption = 'tcf_measure_target_name', confFile = config),
        measure_target_description = findConfig(sysKey = "off_rawlMeasure_target_description", confSection = refference, confOption = 'tcf_measure_target_description', confFile = config) + " (LED: OFF)"
        ), csvFile = csv_name)
    bfr.writeRow(row = _stdLine(
        value = off_rawl[1],
        pin = findConfig(sysKey = "off_rawlPin", confSection = refference, confOption = 'tcf_pin', confFile = config),
        measure_name = findConfig(sysKey = "off_rawlMeasure_name", confSection = "rgb colour", confOption = 'g_measure_name', confFile = config),
        measure_sign = findConfig(sysKey = "off_rawlMeasure_sign", confSection = "rgb colour", confOption = 'measure_sign', confFile = config),
        measure_type_full = findConfig(sysKey = "off_rawlMeasure_type_full", confSection = "rgb colour", confOption = 'measure_type_full', confFile = config),
        measure_type_abbr = findConfig(sysKey = "off_rawlMeasure_type_abbr", confSection = "rgb colour", confOption = 'measure_type_abbr', confFile = config),
        measure_absolute_min = findConfig(sysKey = "off_rawlMeasure_absolute_min", confSection = "rgb colour", confOption = 'measure_absolute_min', confFile = config),
        measure_absolute_max = findConfig(sysKey = "off_rawlMeasure_absolute_max", readVar = off_rawl[3], confSection = "rgb colour", confOption = 'measure_absolute_max', confFile = config),
        measure_target_type = findConfig(sysKey = "off_rawlMeasure_target_type", confSection = refference, confOption = 'tcf_measure_target_type', confFile = config),
        measure_target_name = findConfig(sysKey = "off_rawlMeasure_target_name", confSection = refference, confOption = 'tcf_measure_target_name', confFile = config),
        measure_target_description = findConfig(sysKey = "off_rawlMeasure_target_description", confSection = refference, confOption = 'tcf_measure_target_description', confFile = config) + " (LED: OFF)"
        ), csvFile = csv_name)
    bfr.writeRow(row = _stdLine(
        value = off_rawl[2],
        pin = findConfig(sysKey = "off_rawlPin", confSection = refference, confOption = 'tcf_pin', confFile = config),
        measure_name = findConfig(sysKey = "off_rawlMeasure_name", confSection = "rgb colour", confOption = 'b_measure_name', confFile = config),
        measure_sign = findConfig(sysKey = "off_rawlMeasure_sign", confSection = "rgb colour", confOption = 'measure_sign', confFile = config),
        measure_type_full = findConfig(sysKey = "off_rawlMeasure_type_full", confSection = "rgb colour", confOption = 'measure_type_full', confFile = config),
        measure_type_abbr = findConfig(sysKey = "off_rawlMeasure_type_abbr", confSection = "rgb colour", confOption = 'measure_type_abbr', confFile = config),
        measure_absolute_min = findConfig(sysKey = "off_rawlMeasure_absolute_min", confSection = "rgb colour", confOption = 'measure_absolute_min', confFile = config),
        measure_absolute_max = findConfig(sysKey = "off_rawlMeasure_absolute_max", readVar = off_rawl[3], confSection = "rgb colour", confOption = 'measure_absolute_max', confFile = config),
        measure_target_type = findConfig(sysKey = "off_rawlMeasure_target_type", confSection = refference, confOption = 'tcf_measure_target_type', confFile = config),
        measure_target_name = findConfig(sysKey = "off_rawlMeasure_target_name", confSection = refference, confOption = 'tcf_measure_target_name', confFile = config),
        measure_target_description = findConfig(sysKey = "off_rawlMeasure_target_description", confSection = refference, confOption = 'tcf_measure_target_description', confFile = config) + " (LED: OFF)"
        ), csvFile = csv_name)
    bfr.writeRow(row = _stdLine(
        value = off_rawl[3],
        pin = findConfig(sysKey = "off_rawlPin", confSection = refference, confOption = 'tcf_pin', confFile = config),
        measure_name = findConfig(sysKey = "off_rawlMeasure_name", confSection = "rgb colour", confOption = 'c_measure_name', confFile = config),
        measure_sign = findConfig(sysKey = "off_rawlMeasure_sign", confSection = "rgb colour", confOption = 'measure_sign', confFile = config),
        measure_type_full = findConfig(sysKey = "off_rawlMeasure_type_full", confSection = "rgb colour", confOption = 'measure_type_full', confFile = config),
        measure_type_abbr = findConfig(sysKey = "off_rawlMeasure_type_abbr", confSection = "rgb colour", confOption = 'measure_type_abbr', confFile = config),
        measure_absolute_min = findConfig(sysKey = "off_rawlMeasure_absolute_min", confSection = "rgb colour", confOption = 'measure_absolute_min', confFile = config),
        measure_absolute_max = findConfig(sysKey = "off_rawlMeasure_absolute_max", confSection = "rgb colour", confOption = 'c_measure_absolute_max', confFile = config),
        measure_target_type = findConfig(sysKey = "off_rawlMeasure_target_type", confSection = refference, confOption = 'tcf_measure_target_type', confFile = config),
        measure_target_name = findConfig(sysKey = "off_rawlMeasure_target_name", confSection = refference, confOption = 'tcf_measure_target_name', confFile = config),
        measure_target_description = findConfig(sysKey = "off_rawlMeasure_target_description", confSection = refference, confOption = 'tcf_measure_target_description', confFile = config) + " (LED: OFF)"
        ), csvFile = csv_name)
if on_rawl is not None:
    bfr.writeRow(row = _stdLine(
        value = on_rawl[0],
        pin = findConfig(sysKey = "on_rawlPin", confSection = refference, confOption = 'tcf_pin', confFile = config),
        measure_name = findConfig(sysKey = "on_rawlMeasure_name", confSection = "rgb colour", confOption = 'r_measure_name', confFile = config),
        measure_sign = findConfig(sysKey = "on_rawlMeasure_sign", confSection = "rgb colour", confOption = 'measure_sign', confFile = config),
        measure_type_full = findConfig(sysKey = "on_rawlMeasure_type_full", confSection = "rgb colour", confOption = 'measure_type_full', confFile = config),
        measure_type_abbr = findConfig(sysKey = "on_rawlMeasure_type_abbr", confSection = "rgb colour", confOption = 'measure_type_abbr', confFile = config),
        measure_absolute_min = findConfig(sysKey = "on_rawlMeasure_absolute_min", confSection = "rgb colour", confOption = 'measure_absolute_min', confFile = config),
        measure_absolute_max = findConfig(sysKey = "on_rawlMeasure_absolute_max", readVar = on_rawl[3], confSection = "rgb colour", confOption = 'measure_absolute_max', confFile = config),
        measure_target_type = findConfig(sysKey = "on_rawlMeasure_target_type", confSection = refference, confOption = 'tcf_measure_target_type', confFile = config),
        measure_target_name = findConfig(sysKey = "on_rawlMeasure_target_name", confSection = refference, confOption = 'tcf_measure_target_name', confFile = config),
        measure_target_description = findConfig(sysKey = "on_rawlMeasure_target_description", confSection = refference, confOption = 'tcf_measure_target_description', confFile = config) + " (LED: ON)"
        ), csvFile = csv_name)
    bfr.writeRow(row = _stdLine(
        value = on_rawl[1],
        pin = findConfig(sysKey = "on_rawlPin", confSection = refference, confOption = 'tcf_pin', confFile = config),
        measure_name = findConfig(sysKey = "on_rawlMeasure_name", confSection = "rgb colour", confOption = 'g_measure_name', confFile = config),
        measure_sign = findConfig(sysKey = "on_rawlMeasure_sign", confSection = "rgb colour", confOption = 'measure_sign', confFile = config),
        measure_type_full = findConfig(sysKey = "on_rawlMeasure_type_full", confSection = "rgb colour", confOption = 'measure_type_full', confFile = config),
        measure_type_abbr = findConfig(sysKey = "on_rawlMeasure_type_abbr", confSection = "rgb colour", confOption = 'measure_type_abbr', confFile = config),
        measure_absolute_min = findConfig(sysKey = "on_rawlMeasure_absolute_min", confSection = "rgb colour", confOption = 'measure_absolute_min', confFile = config),
        measure_absolute_max = findConfig(sysKey = "on_rawlMeasure_absolute_max", readVar = on_rawl[3], confSection = "rgb colour", confOption = 'measure_absolute_max', confFile = config),
        measure_target_type = findConfig(sysKey = "on_rawlMeasure_target_type", confSection = refference, confOption = 'tcf_measure_target_type', confFile = config),
        measure_target_name = findConfig(sysKey = "on_rawlMeasure_target_name", confSection = refference, confOption = 'tcf_measure_target_name', confFile = config),
        measure_target_description = findConfig(sysKey = "on_rawlMeasure_target_description", confSection = refference, confOption = 'tcf_measure_target_description', confFile = config) + " (LED: ON)"
        ), csvFile = csv_name)
    bfr.writeRow(row = _stdLine(
        value = on_rawl[2],
        pin = findConfig(sysKey = "on_rawlPin", confSection = refference, confOption = 'tcf_pin', confFile = config),
        measure_name = findConfig(sysKey = "on_rawlMeasure_name", confSection = "rgb colour", confOption = 'b_measure_name', confFile = config),
        measure_sign = findConfig(sysKey = "on_rawlMeasure_sign", confSection = "rgb colour", confOption = 'measure_sign', confFile = config),
        measure_type_full = findConfig(sysKey = "on_rawlMeasure_type_full", confSection = "rgb colour", confOption = 'measure_type_full', confFile = config),
        measure_type_abbr = findConfig(sysKey = "on_rawlMeasure_type_abbr", confSection = "rgb colour", confOption = 'measure_type_abbr', confFile = config),
        measure_absolute_min = findConfig(sysKey = "on_rawlMeasure_absolute_min", confSection = "rgb colour", confOption = 'measure_absolute_min', confFile = config),
        measure_absolute_max = findConfig(sysKey = "on_rawlMeasure_absolute_max", readVar = on_rawl[3], confSection = "rgb colour", confOption = 'measure_absolute_max', confFile = config),
        measure_target_type = findConfig(sysKey = "on_rawlMeasure_target_type", confSection = refference, confOption = 'tcf_measure_target_type', confFile = config),
        measure_target_name = findConfig(sysKey = "on_rawlMeasure_target_name", confSection = refference, confOption = 'tcf_measure_target_name', confFile = config),
        measure_target_description = findConfig(sysKey = "on_rawlMeasure_target_description", confSection = refference, confOption = 'tcf_measure_target_description', confFile = config) + " (LED: ON)"
        ), csvFile = csv_name)
    bfr.writeRow(row = _stdLine(
        value = on_rawl[3],
        pin = findConfig(sysKey = "on_rawlPin", confSection = refference, confOption = 'tcf_pin', confFile = config),
        measure_name = findConfig(sysKey = "on_rawlMeasure_name", confSection = "rgb colour", confOption = 'c_measure_name', confFile = config),
        measure_sign = findConfig(sysKey = "on_rawlMeasure_sign", confSection = "rgb colour", confOption = 'measure_sign', confFile = config),
        measure_type_full = findConfig(sysKey = "on_rawlMeasure_type_full", confSection = "rgb colour", confOption = 'measure_type_full', confFile = config),
        measure_type_abbr = findConfig(sysKey = "on_rawlMeasure_type_abbr", confSection = "rgb colour", confOption = 'measure_type_abbr', confFile = config),
        measure_absolute_min = findConfig(sysKey = "on_rawlMeasure_absolute_min", confSection = "rgb colour", confOption = 'measure_absolute_min', confFile = config),
        measure_absolute_max = findConfig(sysKey = "on_rawlMeasure_absolute_max", confSection = "rgb colour", confOption = 'c_measure_absolute_max', confFile = config),
        measure_target_type = findConfig(sysKey = "on_rawlMeasure_target_type", confSection = refference, confOption = 'tcf_measure_target_type', confFile = config),
        measure_target_name = findConfig(sysKey = "on_rawlMeasure_target_name", confSection = refference, confOption = 'tcf_measure_target_name', confFile = config),
        measure_target_description = findConfig(sysKey = "on_rawlMeasure_target_description", confSection = refference, confOption = 'tcf_measure_target_description', confFile = config) + " (LED: ON)"
        ), csvFile = csv_name)

if mgnm is not None:
    bfr.writeRow(row = _stdLine(
        value = mgnm[0],
        pin = findConfig(sysKey = "mgnmPin", confSection = refference, confOption = 'tcf_pin', confFile = config),
        measure_name = findConfig(sysKey = "mgnmMeasure_name", confSection = "magnetometer", confOption = 'measure_name', confFile = config),
        measure_sign = findConfig(sysKey = "mgnmMeasure_sign", confSection = "magnetometer", confOption = 'measure_sign', confFile = config),
        measure_type_full = findConfig(sysKey = "mgnmMeasure_type_full", confSection = "magnetometer", confOption = 'x_measure_type_full', confFile = config),
        measure_type_abbr = findConfig(sysKey = "mgnmMeasure_type_abbr", confSection = "magnetometer", confOption = 'x_measure_type_abbr', confFile = config),
        measure_absolute_min = findConfig(sysKey = "mgnmMeasure_absolute_min", confSection = "magnetometer", confOption = 'measure_absolute_min', confFile = config),
        measure_absolute_max = findConfig(sysKey = "mgnmMeasure_absolute_max", confSection = "magnetometer", confOption = 'measure_absolute_max', confFile = config),
        measure_target_type = findConfig(sysKey = "mgnmMeasure_target_type", confSection = refference, confOption = 'lsm_measure_target_type', confFile = config),
        measure_target_name = findConfig(sysKey = "mgnmMeasure_target_name", confSection = refference, confOption = 'lsm_measure_target_name', confFile = config),
        measure_target_description = findConfig(sysKey = "mgnmMeasure_target_description", confSection = refference, confOption = 'lsm_measure_target_description', confFile = config) + " (LED: ON)"
        ), csvFile = csv_name)
    bfr.writeRow(row = _stdLine(
        value = mgnm[1],
        pin = findConfig(sysKey = "mgnmPin", confSection = refference, confOption = 'tcf_pin', confFile = config),
        measure_name = findConfig(sysKey = "mgnmMeasure_name", confSection = "magnetometer", confOption = 'measure_name', confFile = config),
        measure_sign = findConfig(sysKey = "mgnmMeasure_sign", confSection = "magnetometer", confOption = 'measure_sign', confFile = config),
        measure_type_full = findConfig(sysKey = "mgnmMeasure_type_full", confSection = "magnetometer", confOption = 'y_measure_type_full', confFile = config),
        measure_type_abbr = findConfig(sysKey = "mgnmMeasure_type_abbr", confSection = "magnetometer", confOption = 'y_measure_type_abbr', confFile = config),
        measure_absolute_min = findConfig(sysKey = "mgnmMeasure_absolute_min", confSection = "magnetometer", confOption = 'measure_absolute_min', confFile = config),
        measure_absolute_max = findConfig(sysKey = "mgnmMeasure_absolute_max", confSection = "magnetometer", confOption = 'measure_absolute_max', confFile = config),
        measure_target_type = findConfig(sysKey = "mgnmMeasure_target_type", confSection = refference, confOption = 'lsm_measure_target_type', confFile = config),
        measure_target_name = findConfig(sysKey = "mgnmMeasure_target_name", confSection = refference, confOption = 'lsm_measure_target_name', confFile = config),
        measure_target_description = findConfig(sysKey = "mgnmMeasure_target_description", confSection = refference, confOption = 'lsm_measure_target_description', confFile = config) + " (LED: ON)"
        ), csvFile = csv_name)
    bfr.writeRow(row = _stdLine(
        value = mgnm[2],
        pin = findConfig(sysKey = "mgnmPin", confSection = refference, confOption = 'tcf_pin', confFile = config),
        measure_name = findConfig(sysKey = "mgnmMeasure_name", confSection = "magnetometer", confOption = 'measure_name', confFile = config),
        measure_sign = findConfig(sysKey = "mgnmMeasure_sign", confSection = "magnetometer", confOption = 'measure_sign', confFile = config),
        measure_type_full = findConfig(sysKey = "mgnmMeasure_type_full", confSection = "magnetometer", confOption = 'z_measure_type_full', confFile = config),
        measure_type_abbr = findConfig(sysKey = "mgnmMeasure_type_abbr", confSection = "magnetometer", confOption = 'z_measure_type_abbr', confFile = config),
        measure_absolute_min = findConfig(sysKey = "mgnmMeasure_absolute_min", confSection = "magnetometer", confOption = 'measure_absolute_min', confFile = config),
        measure_absolute_max = findConfig(sysKey = "mgnmMeasure_absolute_max", confSection = "magnetometer", confOption = 'measure_absolute_max', confFile = config),
        measure_target_type = findConfig(sysKey = "mgnmMeasure_target_type", confSection = refference, confOption = 'lsm_measure_target_type', confFile = config),
        measure_target_name = findConfig(sysKey = "mgnmMeasure_target_name", confSection = refference, confOption = 'lsm_measure_target_name', confFile = config),
        measure_target_description = findConfig(sysKey = "mgnmMeasure_target_description", confSection = refference, confOption = 'lsm_measure_target_description', confFile = config) + " (LED: ON)"
        ), csvFile = csv_name)

if acclm is not None:
    bfr.writeRow(row = _stdLine(
        value = acclm[0],
        pin = findConfig(sysKey = "acclmPin", confSection = refference, confOption = 'lsm_pin', confFile = config),
        measure_name = findConfig(sysKey = "acclmMeasure_name", confSection = "accelerometer", confOption = 'measure_name', confFile = config),
        measure_sign = findConfig(sysKey = "acclmMeasure_sign", confSection = "accelerometer", confOption = 'measure_sign', confFile = config),
        measure_type_full = findConfig(sysKey = "acclmMeasure_type_full", confSection = "accelerometer", confOption = 'x_measure_type_full', confFile = config),
        measure_type_abbr = findConfig(sysKey = "acclmMeasure_type_abbr", confSection = "accelerometer", confOption = 'x_measure_type_abbr', confFile = config),
        measure_absolute_min = findConfig(sysKey = "acclmMeasure_absolute_min", confSection = "accelerometer", confOption = 'measure_absolute_min', confFile = config),
        measure_absolute_max = findConfig(sysKey = "acclmMeasure_absolute_max", confSection = "accelerometer", confOption = 'measure_absolute_max', confFile = config),
        measure_target_type = findConfig(sysKey = "acclmMeasure_target_type", confSection = refference, confOption = 'lsm_measure_target_type', confFile = config),
        measure_target_name = findConfig(sysKey = "acclmMeasure_target_name", confSection = refference, confOption = 'lsm_measure_target_name', confFile = config),
        measure_target_description = findConfig(sysKey = "acclmMeasure_target_description", confSection = refference, confOption = 'lsm_measure_target_description', confFile = config) + " (LED: ON)"
        ), csvFile = csv_name)
    bfr.writeRow(row = _stdLine(
        value = acclm[1],
        pin = findConfig(sysKey = "acclmPin", confSection = refference, confOption = 'lsm_pin', confFile = config),
        measure_name = findConfig(sysKey = "acclmMeasure_name", confSection = "accelerometer", confOption = 'measure_name', confFile = config),
        measure_sign = findConfig(sysKey = "acclmMeasure_sign", confSection = "accelerometer", confOption = 'measure_sign', confFile = config),
        measure_type_full = findConfig(sysKey = "acclmMeasure_type_full", confSection = "accelerometer", confOption = 'y_measure_type_full', confFile = config),
        measure_type_abbr = findConfig(sysKey = "acclmMeasure_type_abbr", confSection = "accelerometer", confOption = 'y_measure_type_abbr', confFile = config),
        measure_absolute_min = findConfig(sysKey = "acclmMeasure_absolute_min", confSection = "accelerometer", confOption = 'measure_absolute_min', confFile = config),
        measure_absolute_max = findConfig(sysKey = "acclmMeasure_absolute_max", confSection = "accelerometer", confOption = 'measure_absolute_max', confFile = config),
        measure_target_type = findConfig(sysKey = "acclmMeasure_target_type", confSection = refference, confOption = 'lsm_measure_target_type', confFile = config),
        measure_target_name = findConfig(sysKey = "acclmMeasure_target_name", confSection = refference, confOption = 'lsm_measure_target_name', confFile = config),
        measure_target_description = findConfig(sysKey = "acclmMeasure_target_description", confSection = refference, confOption = 'lsm_measure_target_description', confFile = config) + " (LED: ON)"
        ), csvFile = csv_name)
    bfr.writeRow(row = _stdLine(
        value = acclm[2],
        pin = findConfig(sysKey = "acclmPin", confSection = refference, confOption = 'lsm_pin', confFile = config),
        measure_name = findConfig(sysKey = "acclmMeasure_name", confSection = "accelerometer", confOption = 'measure_name', confFile = config),
        measure_sign = findConfig(sysKey = "acclmMeasure_sign", confSection = "accelerometer", confOption = 'measure_sign', confFile = config),
        measure_type_full = findConfig(sysKey = "acclmMeasure_type_full", confSection = "accelerometer", confOption = 'z_measure_type_full', confFile = config),
        measure_type_abbr = findConfig(sysKey = "acclmMeasure_type_abbr", confSection = "accelerometer", confOption = 'z_measure_type_abbr', confFile = config),
        measure_absolute_min = findConfig(sysKey = "acclmMeasure_absolute_min", confSection = "accelerometer", confOption = 'measure_absolute_min', confFile = config),
        measure_absolute_max = findConfig(sysKey = "acclmMeasure_absolute_max", confSection = "accelerometer", confOption = 'measure_absolute_max', confFile = config),
        measure_target_type = findConfig(sysKey = "acclmMeasure_target_type", confSection = refference, confOption = 'lsm_measure_target_type', confFile = config),
        measure_target_name = findConfig(sysKey = "acclmMeasure_target_name", confSection = refference, confOption = 'lsm_measure_target_name', confFile = config),
        measure_target_description = findConfig(sysKey = "acclmMeasure_target_description", confSection = refference, confOption = 'lsm_measure_target_description', confFile = config) + " (LED: ON)"
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
