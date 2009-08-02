filters = []

def date(value, format='%H:%M / %d-%m-%Y'):
    return value.strftime(format)
filters.append(date)
