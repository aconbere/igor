from re import sub

def slugify(string):
    string = sub('\s+', '_', string)
    string = sub('[^\w.-]', '', string)
    return string.strip('_.- ').lower()

def hidden(p):
    return not (p == "." or p == "..") and p.startswith(".")

def compare_post_dates(p1, p2):
    return cmp(p2.published_on, p1.published_on)
