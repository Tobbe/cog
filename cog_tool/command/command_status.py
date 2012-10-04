import argparse
import logging

import cog_tool.data_manipulation as dm

def get_command():
    return 'status'

def get_help():
    return 'Alter the status of an item.'

def get_argparser():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('file', nargs=1, help='File to change.')
    parser.add_argument('status', nargs=1,
                        choices=['not-started', 'ongoing', 'waiting', 'done'],
                        help='Status to set.')
    return parser

def execute(state, args):
    key = args.file[0]
    data = state.get(key)
    status = args.status[0]

    dm.set(data, 'STATUS', status)
    logging.info('"%s" is now %s' % (dm.get(data, 'NAME'), status))

    state.save(key)
