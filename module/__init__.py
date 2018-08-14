import re

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

def cleanType(var = None):
    ## try to convert to correct data type:
    if var in [None, 'None', '']:
        return None
    else:
        try:
            if type(var) not in [int, float]:
                var = int(var)
        except:
            try:
                var = float(var)
            except:
                ## var = str(var) ## error
                var = var
                ## print var, type(var)
    return var

def cleanUnicode(var = None):
    ## try to find unicode and decode it:
    if isinstance(var, str):
        if var[:3] == "u'\\" or var[:3] == 'u"\\':
            x = re.search(r"u[\"|\'](\\.+)[\"|\']", var)
            x = x.group(1)
            var = x.decode('unicode-escape')
    return var
