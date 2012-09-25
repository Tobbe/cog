import argparse

import cog_tool.common as common

def get_command():
    return 'validate'

def get_argparser():
    parser = argparse.ArgumentParser(description='Runs a sanity check on the values.',
                                     add_help=False)
    parser.add_argument('files', nargs='+',
                        help='The files to check.')
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

def _check_file(path):
    data = common.load(path)
    errors = []

    for key in ['ID', 'NAME', 'DESCRIPTION']:
        _add_error(errors, _has_value(data, key))

    if errors:
        print('File: %s' % (path,))
        for err in errors:
            print(' - %s' % (err,))

def execute(args):
    for f in args.files:
        _check_file(f)
