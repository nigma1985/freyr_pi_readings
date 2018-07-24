from datetime import datetime
from datetime import timedelta
import time


#################################################
###  Tools for time management                ###
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
###  Other Tools                              ###
#################################################

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)
