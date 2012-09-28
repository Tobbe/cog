import argparse

def get_command():
    return 'validate'

def get_help():
    return 'Sanity check given files.'

def get_argparser():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('file', nargs='*', default='.',
                        help='The files to check. Default: "%(default)s"')
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

def _check_file(state, path):
    data = state.get_by_path(path)
    errors = []

    for key in ['ID', 'NAME', 'DESCRIPTION']:
        _add_error(errors, _has_value(data, key))

    if errors:
        print('File: %s' % (path,))
        for err in errors:
            print(' - %s' % (err,))
        print('')

def execute(state, args):
    files = state.expand_paths(args.file)
    for f in files:
        _check_file(state, f)
