import re

RE_HEADER = re.compile('^\[([a-zA-Z0-9 _-]+)\]$')

def _get_header(line):
    """Returns the header name or None if not an header."""
    mobj = RE_HEADER.match(line)
    if mobj:
        return mobj.group(1)

def parse_lines(lines):
    result = {}
    key = None

    for line in lines:
        line = line.rstrip()
        header = _get_header(line)
        if header:
            key = header
            continue

        if line and not key:
            raise Exception('Body encountered before header. "%s"' % (line,))

        if not key in result:
            result[key] = []

        result[key].append(line)

    return result

def load(path):
    return parse_lines(open(path).readlines())

def _adjust_newlines(lines):
    """Removes excessive trailing newlines."""
    if lines:
        while lines and lines[-1] == '':
            lines = lines[:-1]
        lines.append('')
    return lines

def save(path, data):
    master_keys = ['NAME', 'ID', 'STATUS', 'ASSIGNED', 'DESCRIPTION']
    other_keys = sorted(filter(lambda k: k not in master_keys,
                               data.keys()))

    def output(file, keys):
        for key in keys:
            if not key in data:
                continue

            wrote_nl = False
            f.write('[%s]' % (key,))
            f.write('\n')

            for line in _adjust_newlines(data[key]):
                wrote_nl = len(line) == 0
                f.write(line)
                f.write('\n')

            if not wrote_nl:
                f.write('\n')

    with open(path, 'w') as f:
        output(f, master_keys)
        output(f, other_keys)
