import argparse

import cog_tool.data_manipulation as dm
import cog_tool.state

def get_command():
    return 'validate'

def get_help():
    return 'Sanity check given files.'

def get_argparser():
    parser = argparse.ArgumentParser(add_help=False)
    return parser

def _has_value(data, key):
    if not key in data:
        return '[%s] header is recommended but missing.' % (key,)

    for line in data[key]:
        if len(line.strip()) > 0:
            return

    return '[%s] does not have a body.' % (key,)

def _add_error(lst, error):
    if error:
        lst.append(error)

def _check_data(state, data):
    errors = []

    for key in ['ID', 'NAME']:
        _add_error(errors, _has_value(data, key))

    if errors:
        print('File: %s' % state.relative_path(dm.get(data, 'ID')))
        for err in errors:
            print(' - %s' % (err,))
        print('')

def execute(state, args):
    for data in state.get_all():
        _check_data(state, data)
