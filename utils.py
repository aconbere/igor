from re import sub

def slugify(string):
    string = sub('\s+', '_', string)
    string = sub('[^\w.-]', '', string)
    return string.strip('_.- ').lower()

def hidden(relative_path):
    return relative_path.startswith(".") and len(relative_path) > 1
