import argparse
import logging

import cog_tool.data_manipulation as dm

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

def _link(state, args, data, path):
    other = state.get_by_path(path)
    other_id = dm.get(other, 'ID')
    if not other_id:
        logging.warn('Can not link to "%s", no id.', path)
        return

    key = 'LINK'
    if args.parent:
        key = 'PARENT'
    if args.prereq:
        key = 'PREREQ'

    if not key in data:
        data[key] = []

    name = dm.get(data, 'NAME', path)
    for line in data[key]:
        if line.startswith(other_id):
            logging.info('Already linked to "%s"',
                         dm.get(other, 'NAME', '?'))
            return

    dm.add_last(data, key, '%s %s' % (other_id, name))

    logging.info('Linking "%s" to "%s"',
                 dm.get(data, 'NAME', '?'),
                 dm.get(other, 'NAME', '?'))

def execute(state, args):
    if len(args.file) < 2:
        raise Exception('"link" command requires 2 or more arguments.')

    from_ = args.file[0]
    to = args.file[1:]

    data = state.get_by_path(from_)

    for path in state.expand_paths(to):
        _link(state, args, data, path)

    state.save(from_)
