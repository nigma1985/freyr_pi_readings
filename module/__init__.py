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
                var = str(var)
    return var
