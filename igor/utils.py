from re import sub

def slugify(string):
    string = sub('\s+', '_', string)
    string = sub('[^\w.-]', '', string)
    return string.strip('_.- ').lower()

def hidden(p):
    return not (p == "." or p == "..") and p.startswith(".")
