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
    parser.add_argument('file', nargs=1,
                        help='The filename of the file to create. If an existing file is given any missing default values will be added to that file.')
    parser.add_argument('--all', action='store_true',
                        help='Create/update all headers.')
    return parser

def _set_if(data, key, value):
    if key in data:
        for line in data[key]:
            if len(line.strip()) > 0:
                return
    data[key] = [value]

def execute(args):
    path = args.file[0]

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
