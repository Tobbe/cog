import argparse
import os
import uuid

import cog_tool.common as common

def get_command():
    return 'new'

def get_help():
    return 'Create/update file with recommended values.'

def get_argparser():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('file', nargs='+',
                        help='The filenames to create. If file exists; expand with missing headers.')
    parser.add_argument('--all', action='store_true',
                        help='Create/update all headers.')
    return parser

def _set_if(data, key, value):
    if key in data:
        for line in data[key]:
            if len(line.strip()) > 0:
                return
    data[key] = [value]

def _do_file(args, path):
    if os.path.exists(path):
        data = common.load(path)
    else:
        data = {}

    _set_if(data, 'ID', str(uuid.uuid4()))
    _set_if(data, 'NAME', '')
    _set_if(data, 'DESCRIPTION', '')
    if args.all:
        for key in ['STATUS', 'ASSIGNED', 'IMPORTANCE', 'LINK',
                    'ORIGINAL-ESTIMATE', 'PARENT', 'TAG', 'TIME-REPORT']:
            _set_if(data, key, '')

    common.save(path, data)

def execute(args):
    paths = common.expand_dirs(args.file)

    for path in paths:
        if os.path.exists(path):
            if path.endswith('.txt'):
                _do_file(args, path)
        else:
            if not path.endswith('.txt'):
                path = '%s.txt' % (path,)
            _do_file(args, path)
