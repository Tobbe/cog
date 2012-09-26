import argparse
import logging

import cog_tool.common as common

def get_command():
    return 'link'

def get_help():
    return 'Setup links between items.'

def get_argparser():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('file', nargs='+',
                        help='The first file is being modified. Remaining files are link targets.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--link', action='store_true',
                       help='The link is a regular-link. This is the default.')
    group.add_argument('--parent', action='store_true',
                       help='The link is a parent-link.')
    group.add_argument('--prereq', action='store_true',
                       help='The link is a prereq-link.')
    return parser

def _link(args, data, path):
    other = common.load(path)
    other_id = common.get_value(other, 'ID')
    if not other_id:
        logging.warn('Can not link to "%s", no id.' % (path,))
        return

    key = 'LINK'
    if args.parent:
        key = 'PARENT'
    if args.prereq:
        key = 'PREREQ'

    if not key in data:
        data[key] = []

    lines = data[key]
    for line in lines:
        if line.startswith(other_id):
            return

    name = common.get_value(data, 'NAME', path)
    common.add_last(data, key, '%s %s' % (other_id, name))

def execute(args):
    if len(args.file) < 2:
        raise Exception('"link" command requires 2 or more arguments.')

    from_ = args.file[0]
    to = args.file[1:]

    data = common.load(from_)

    for path in to:
        _link(args, data, path)

    common.save(from_, data)
