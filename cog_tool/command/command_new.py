import argparse
import logging
import uuid

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

def _do_file(state, args, path):
    data = state.get_by_path(path)
    if not data:
        logging.info('Creating new file: %s', path)
        data = state.new(path)
    else:
        logging.info('Updating file %s', path)

    _set_if(data, 'ID', str(uuid.uuid4()))
    _set_if(data, 'NAME', '')
    _set_if(data, 'DESCRIPTION', '')
    if args.all:
        for key in ['STATUS', 'ASSIGNED', 'PRIORITY', 'LINK',
                    'ORIGINAL-ESTIMATE', 'PARENT', 'TAG', 'TIME-REPORT']:
            _set_if(data, key, '')

    state.save(path)

def execute(state, args):
    paths = state.expand_paths(args.file,
                               only_items=False,
                               only_existing=False)

    for path in paths:
        if state.get_by_path(path):
            if path.endswith('.txt'):
                _do_file(state, args, path)
        else:
            if not path.endswith('.txt'):
                path += '.txt'

            _do_file(state, args, path)
