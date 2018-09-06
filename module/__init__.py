import re, shutil, codecs

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

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
    return max(age.st_ctime, age.st_mtime) # output in bytes

def islist(lst):
    if type(lst)==list:
        return True
    else:
        return False

def cleanUnicode(var = None):
    ## print("start")
    if var is not None and isinstance(var, str):
        ## print("step1")
        if re.search(r"^u[\"|\'](.*?)[\"|\']$", var):
            ## print("step2")
            try:
                ## print("try")
                return( codecs.decode(var[2:-1], 'unicode_escape') )
                ## print("exec:", mirror, var)
            except:
                return( var[2:-1] )
    ## print("end")
    return(var)

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
