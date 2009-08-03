import sys
sys.append("..")

from rfc3339 import rfc3339

filters = []

def date(value, format='%H:%M / %d-%m-%Y'):
    return value.strftime(format)
filters.append(date)

def rfc3339(value):
    return rfc3339(value)
filters.append(rfc3339)
    
