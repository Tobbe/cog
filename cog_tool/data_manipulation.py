
def get(data, key, default=''):
    """Returns the first non-empty, non-whitespace value."""
    for line in data.get(key, []):
        if line.strip():
            return line
    return default

def add_last(data, key, value):
    if not key in data:
        data[key] = []

    lines = data[key]
    while lines and lines[-1] == '':
        lines = lines[:-1]

    lines.append(value)
    data[key] = lines

def get_links(data, key):
    links = data.get(key, [])
    result = []

    for link in links:
        if link.strip():
            id = link.split()[0]
            result.append(id)

    return result
