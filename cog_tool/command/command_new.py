import argparse
import os
import uuid

import cog_tool.common as common

def get_command():
    return 'new'

def get_argparser():
    parser = argparse.ArgumentParser(description='Create new cog file with default values.',
                                     add_help=False)
    parser.add_argument('file', nargs=1,
                        help='The filename of the file to create. If an existing file is given any missing default values will be added to that file.')
    return parser

def set_if(data, key, value):
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

    set_if(data, 'ID', str(uuid.uuid4()))
    set_if(data, 'NAME', '')
    set_if(data, 'DESCRIPTION', '')
    set_if(data, 'ASSIGNED', '')
    set_if(data, 'IMPORTANCE', '')

    common.save(path, data)
