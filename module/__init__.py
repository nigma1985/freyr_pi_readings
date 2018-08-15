import re

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

def cleanUnicode(var = None):
    ## try to find unicode and decode it:
    if isinstance(var, str):
        if var[:3] == "u'\\" or var[:3] == 'u"\\':
            var = re.search(r"u[\"|\'](\\.+)[\"|\']", var)
            var = var.group(1)
            var = var.decode('unicode-escape')
    return var

def str2list(var = None, symbol = None):
    if var is None or type(var) != str:
        return var
    if symbol is None:
        symbol = ","
    if re.search(symbol, var): ## symbol in var
        return var.split(symbol)
    else:
        return var

def cleanSpaces(var = None):
    if var is None:
        return var
    elif type(var) == str:
        mirror = None
        while mirror != var:
            mirror = var
            var = var.replace("  "," ")
        return var.strip()
    else:
        mirror = None
        while mirror != var:
            mirror = var
            var = [itm.replace("  "," ") for itm in var]
        return [itm.strip() for itm in var]

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

def cleanList(string = None, sym = None):
    if string is None:
        return string
    string = str2list(var = string, symbol = sym)
    string = cleanSpaces(var = string)
    if type(string) == list:
        return [cleanUnicode(var = cleanType(var = itm)) for itm in string]
    else:
        return cleanUnicode(var = cleanType(var = string))
