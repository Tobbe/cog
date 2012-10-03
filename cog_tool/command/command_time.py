import argparse
import os
import time

import cog_tool.data_manipulation as dm

def get_command():
    return 'time'

def get_help():
    return 'Report time for an item.'

def get_argparser():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('file', nargs=1,
                        help='The item to work with.')
    parser.add_argument('spent', nargs=1,
                        help='The number of hours spent on the task.')
    parser.add_argument('remaining', nargs=1,
                        help='The number of hours left for the task.')
    parser.add_argument('--user', default=os.environ.get('USER', '?'),
                        help='The user to report for. Default: %(default)s')
    parser.add_argument('--time', default=_generate_now(),
                        help='The day to report for. Default: %(default)s')
    return parser

def _generate_now():
    tm = time.localtime()
    return '%04d-%02d-%02d' % (tm[0], tm[1], tm[2])

def execute(state, args):
    key = args.file[0]

    data = state.get(key)
    if not data:
        raise Exception('Unable to find "%s"' % (args.file,))

    dm.add_last(data,
                'TIME-REPORT',
                '%s %s %s %s' % (args.time,
                                 args.user,
                                 args.spent[0],
                                 args.remaining[0]))

    state.save(key)
