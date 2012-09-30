"""Main entry point for the application.
"""
import argparse
import importlib
import logging
import os

import cog_tool.state as state

def _make_parser(cmd_mods):
    """Constructs an ArgumentParser by combining all the sub commands
    ArgumentParsers."""
    parser = argparse.ArgumentParser(description='Cog command line util.')
    subparsers = parser.add_subparsers(help='Sub commands.')

    for mod in cmd_mods:
        subparsers.add_parser(mod.get_command(),
                              parents=[mod.get_argparser()],
                              help=mod.get_help())

    return parser

def _setup_logging():
    logging.basicConfig(format='%(asctime)s.%(msecs)d <%(levelname)s> %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

def _load_commands():
    """Loads commands that can be found and returns them in a list."""
    result = []

    path = os.path.join(os.path.dirname(__file__),
                        'command')
    base = __name__.rsplit('.', 1)[0]
    for fn in os.listdir(path):
        if fn.startswith('command_') and fn.endswith('.py'):
            modname = '%s.command.%s' % (base, fn.rsplit('.', 1)[0])
            result.append(importlib.import_module(modname))

    return result

def _run_command(cmd, cmd_mods, args):
    st = state.State()

    for mod in cmd_mods:
        if mod.get_command() == cmd:
            mod.execute(st, args)
            return

    raise Exception('Unknown command "%s"' % (cmd,))

def run(arg_seq=None):
    cmd_mods = _load_commands()
    args = _make_parser(cmd_mods).parse_args(args=arg_seq)
    _setup_logging()
    _run_command(arg_seq[0], cmd_mods, args)
