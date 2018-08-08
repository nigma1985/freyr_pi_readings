#!/usr/bin/python

# This script develops a python script to read and write system data
# -*- coding: utf-8 -*-

################################################################################

import module.config as ini ## https://wiki.python.org/moin/ConfigParserExamples
import module.decision as dec
import module.getOptions as opt
import module.timeTools as ttl
import module.netTools as ntt
import module.freyr.csvBuffer as bfr
import module.read.pi as rpi
from module.freyr import findConfig
from module import mean
import os

refference = "Sys"

## reading 'freyr_config.ini'
configFile = "freyr_config.ini"
config = ini.getConfig(configFile)


me = findConfig(sysKey = "me", confSection = refference, confOption = 'source_name', confFile = config)
my_user = findConfig(sysKey = "my_user", confSection = refference, confOption = 'user', confFile = config)


all_on = opt.findItm("ALLON")
all_off = opt.findItm("ALLOFF")

# Try to grab a sensor reading.  Use the read_retry method which will retry up
now1, utc1, nowsecs = ttl.start()

ram_time = nowsecs % (1.001 * (60 * 3))
ram_time_percent = nowsecs % (0.999 * (60 * 12))
disk_time = nowsecs % (1.001 * (60 * 60 * 12))
disk_time_percent = nowsecs % (0.999 * (60 * 60 * 24 * 7))
cpu_tempA = rpi.getCPUtemperature()
cpu_use = None
if dec.decision(onSwitch = [all_on, "CPUUSEON"], offSwitch = [all_off, "CPUUSEOFF"]):
    cpu_use = rpi.cpu_percent()

ram = rpi.virtual_memory()
ram_total = None
ram_used = None
ram_free = None
ram_percent_used = None
if dec.decision(onSwitch = [all_on, "RAMBITON", (cpu_use > 80.0), (cpu_tempA > 57.5)], numInterval = ram_time, offSwitch = [all_off, "RAMBITOFF"]):
    ram_total = ram.total / 2**20       # MiB.
    ram_used = ram.used / 2**20
    ram_free = ram.free / 2**20

if dec.decision(onSwitch = [all_on, "RAMUSEON"], numInterval = ram_time_percent, offSwitch = [all_off, "RAMUSEOFF"]):
    ram_percent_used = ram.percent


disk = rpi.disk_usage('/')
disk_total = None
disk_used = None
disk_remaining = None
disk_percentage = None
if dec.decision(onSwitch = [all_on, "DSKBITON"], numInterval = disk_time, offSwitch = [all_off, "DSKBITOFF"]):
    disk_total = disk.total / 2**30     # GiB.
    disk_used = disk.used / 2**30
    disk_remaining = disk.free / 2**30

if dec.decision(onSwitch = [all_on, "DSKUSEON"], numInterval = disk_time_percent, offSwitch = [all_off, "DSKUSEOFF"]):
    disk_percentage = disk.percent

cpu_tempB = rpi.get_cpu_temperature()
cpu_temp = None
if dec.decision(onSwitch = [all_on, "CPUTMPON"], offSwitch = [all_off, "CPUTMPOFF"]):
    cpu_temp = mean([float(cpu_tempA), cpu_tempB])

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
    measure_target_name = findConfig(sysKey = "measure_target_name", confSection = refference, confOption = 'measure_target_name', confFile = config),
    measure_target_description = findConfig(sysKey = "measure_target_description", confSection = refference, confOption = 'measure_target_description', confFile = config),
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
if cpu_temp is not None:
    bfr.writeRow(row = _stdLine(
        value = cpu_temp,
        # measure
        measure_name = findConfig(sysKey = "cpu_temp_measure_name", confSection = 'tmp_celsius', confOption = 'measure_name', confFile = config),
        measure_sign = findConfig(sysKey = "cpu_temp_measure_sign", confSection = 'tmp_celsius', confOption = 'measure_sign', confFile = config),
        measure_type_full = findConfig(sysKey = "cpu_temp_measure_type_full", confSection = 'tmp_celsius', confOption = 'measure_type_full', confFile = config),
        measure_type_abbr = findConfig(sysKey = "cpu_temp_measure_type_abbr", confSection = 'tmp_celsius', confOption = 'measure_type_abbr', confFile = config),
        measure_absolute_min = findConfig(sysKey = "cpu_temp_measure_absolute_min", confSection = 'tmp_celsius', confOption = 'measure_absolute_min', confFile = config),
        measure_absolute_max = findConfig(sysKey = "cpu_temp_measure_absolute_max", confSection = 'tmp_celsius', confOption = 'measure_absolute_max', confFile = config),
        measure_target_type = findConfig(sysKey = "cpu_temp_measure_target_type", confSection = refference, confOption = 'cpu_measure_target_type', confFile = config)
        ), csvFile = csv_name)
if cpu_use is not None:
    bfr.writeRow(row = _stdLine(
        value = cpu_use,
        # measure
        measure_name = findConfig(sysKey = "cpu_use_measure_name", confSection = 'percent_used', confOption = 'measure_name', confFile = config),
        measure_sign = findConfig(sysKey = "cpu_use_measure_sign", confSection = 'percent_used', confOption = 'measure_sign', confFile = config),
        measure_type_full = findConfig(sysKey = "cpu_use_measure_type_full", confSection = 'percent_used', confOption = 'measure_type_full', confFile = config),
        measure_type_abbr = findConfig(sysKey = "cpu_use_measure_type_abbr", confSection = 'percent_used', confOption = 'measure_type_abbr', confFile = config),
        measure_absolute_min = findConfig(sysKey = "cpu_use_measure_absolute_min", confSection = 'percent_used', confOption = 'measure_absolute_min', confFile = config),
        measure_absolute_max = findConfig(sysKey = "cpu_use_measure_absolute_max", confSection = 'percent_used', confOption = 'measure_absolute_max', confFile = config),
        measure_target_type = findConfig(sysKey = "cpu_use_measure_target_type", confSection = refference, confOption = 'cpu_measure_target_type', confFile = config)
        ), csvFile = csv_name)
if disk_percentage is not None:
    bfr.writeRow(row = _stdLine(
        value = disk_percentage,
        # measure
        measure_name = findConfig(sysKey = "disk_percentage_measure_name", confSection = 'percent_used', confOption = 'measure_name', confFile = config),
        measure_sign = findConfig(sysKey = "disk_percentage_measure_sign", confSection = 'percent_used', confOption = 'measure_sign', confFile = config),
        measure_type_full = findConfig(sysKey = "disk_percentage_measure_type_full", confSection = 'percent_used', confOption = 'measure_type_full', confFile = config),
        measure_type_abbr = findConfig(sysKey = "disk_percentage_measure_type_abbr", confSection = 'percent_used', confOption = 'measure_type_abbr', confFile = config),
        measure_absolute_min = findConfig(sysKey = "disk_percentage_measure_absolute_min", confSection = 'percent_used', confOption = 'measure_absolute_min', confFile = config),
        measure_absolute_max = findConfig(sysKey = "disk_percentage_measure_absolute_max", confSection = 'percent_used', confOption = 'measure_absolute_max', confFile = config),
        measure_target_type = findConfig(sysKey = "disk_percentage_measure_target_type", confSection = refference, confOption = 'disk_measure_target_type', confFile = config)
        ), csvFile = csv_name)
if ram_used is not None:
    bfr.writeRow(row = _stdLine(
        value = ram_used,
        # measure
        measure_name = findConfig(sysKey = "ram_used_measure_name", confSection = 'MegaByte', confOption = 'measure_name', confFile = config),
        measure_sign = findConfig(sysKey = "ram_used_measure_sign", confSection = 'MegaByte', confOption = 'measure_sign', confFile = config),
        measure_type_full = findConfig(sysKey = "ram_used_measure_type_full", confSection = refference, confOption = 'ram_measure_type_full', confFile = config),
        measure_type_abbr = findConfig(sysKey = "ram_used_measure_type_abbr", confSection = refference, confOption = 'ram_measure_type_abbr', confFile = config),
        measure_absolute_min = findConfig(sysKey = "ram_used_measure_absolute_min", confSection = 'MegaByte', confOption = 'measure_absolute_min', confFile = config),
        measure_absolute_max = findConfig(sysKey = "ram_used_measure_absolute_max", readVar = ram_total, confSection = 'MegaByte', confOption = 'measure_absolute_max', confFile = config),
        measure_target_type = findConfig(sysKey = "ram_used_measure_target_type", confSection = refference, confOption = 'ram_measure_target_type', confFile = config)
        ), csvFile = csv_name)
if ram_percent_used is not None:
    bfr.writeRow(row = _stdLine(
        value = ram_percent_used,
        # measure
        measure_name = findConfig(sysKey = "ram_percent_used_measure_name", confSection = 'percent_used', confOption = 'measure_name', confFile = config),
        measure_sign = findConfig(sysKey = "ram_percent_used_measure_sign", confSection = 'percent_used', confOption = 'measure_sign', confFile = config),
        measure_type_full = findConfig(sysKey = "ram_percent_used_measure_type_full", confSection = 'percent_used', confOption = 'measure_type_full', confFile = config),
        measure_type_abbr = findConfig(sysKey = "ram_percent_used_measure_type_abbr", confSection = 'percent_used', confOption = 'measure_type_abbr', confFile = config),
        measure_absolute_min = findConfig(sysKey = "ram_percent_used_measure_absolute_min", confSection = 'percent_used', confOption = 'measure_absolute_min', confFile = config),
        measure_absolute_max = findConfig(sysKey = "ram_percent_used_measure_absolute_max", confSection = 'percent_used', confOption = 'measure_absolute_max', confFile = config),
        measure_target_type = findConfig(sysKey = "ram_percent_used_measure_target_type", confSection = refference, confOption = 'ram_measure_target_type', confFile = config)
        ), csvFile = csv_name)
if disk_used is not None:
    bfr.writeRow(row = _stdLine(
        value = disk_used,
        # measure
        measure_name = findConfig(sysKey = "disk_used_measure_name", confSection = 'GigaByte', confOption = 'measure_name', confFile = config),
        measure_sign = findConfig(sysKey = "disk_used_measure_sign", confSection = 'GigaByte', confOption = 'measure_sign', confFile = config),
        measure_type_full = findConfig(sysKey = "disk_used_measure_type_full", confSection = refference, confOption = 'disk_measure_type_full', confFile = config),
        measure_type_abbr = findConfig(sysKey = "disk_used_measure_type_abbr", confSection = refference, confOption = 'disk_measure_type_abbr', confFile = config),
        measure_absolute_min = findConfig(sysKey = "disk_used_measure_absolute_min", confSection = 'GigaByte', confOption = 'measure_absolute_min', confFile = config),
        measure_absolute_max = findConfig(sysKey = "disk_used_measure_absolute_max", readVar = disk_total, confSection = 'GigaByte', confOption = 'measure_absolute_max', confFile = config),
        measure_target_type = findConfig(sysKey = "disk_used_measure_target_type", confSection = refference, confOption = 'disk_measure_target_type', confFile = config)
        ), csvFile = csv_name)

try:
    ntt.scp(
        file = findConfig(sysKey = "csvFile", readVar = csv_name, confSection = "Sys", confOption = 'csvFile', confFile = config),
        user = findConfig(sysKey = "db_user", confSection = "Sys", confOption = 'db_user', confFile = config),
        host = findConfig(sysKey = "db_host", confSection = "Sys", confOption = 'db_host', confFile = config),
        path = findConfig(sysKey = "db_path", confSection = "Sys", confOption = 'db_path', confFile = config))
    #print "tst"
except:
    print "ERROR @ transfer"
