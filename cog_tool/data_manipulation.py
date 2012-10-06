"""This module provides functions for manipulating data
items. (Generally gotten from the State object.)
"""

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

def set(data, key, *values):
    data[key] = list(values)

def get_links(data, key):
    links = data.get(key, [])
    result = []

    for link in links:
        if link.strip():
            id = link.split()[0]
            result.append(id)

    return result

def null(data, key):
    """Returns True if the value of key is empty."""
    for line in data.get(key, []):
        if line.strip():
            return False
    return True

#--------------------------------------------------
# time

def get_time_reports(data):
    result = []

    for line in data.get('TIME-REPORT', []):
        line = line.strip()
        if line:
            time, user, spent, remaining = line.split()
            result.append({'time': time,
                           'user': user,
                           'spent': spent,
                           'remaining': remaining})

    return sorted(result, key=lambda x: x['time'])

def get_time_spent(data):
    reps = get_time_reports(data)
    result = 0
    for rep in reps:
        result += int(rep['spent'])
    return result

def get_remaining_time(data):
    reps = get_time_reports(data)
    if not reps:
        return get_estimate(data)

    return int(reps[-1].get('remaining'))

def get_estimate(data):
    return int(get(data, 'ESTIMATE', -1))

def get_projected_time_diff(data):
    return get_remaining_time(data) - (get_estimate(data) - get_time_spent(data))

#--------------------------------------------------
# status

def get_status(data):
    status = get(data, 'STATUS')
    if not status:
        if get_remaining_time(data) == 0:
            status = 'done'
        elif get_time_reports(data):
            status = 'ongoing'
        else:
            status = 'not-started'
    return status
