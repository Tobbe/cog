"""Helpers functions for testing.
"""
import os
import unittest

import cog_tool.app as app
import cog_tool.data_manipulation as dm
import cog_tool.state as st

_abs = os.path.abspath
_PATH = st._PATH

def run_cmd(state, *arguments):
    cmd = arguments[0]
    cmd_mods = app._load_commands()
    args = app._make_parser(cmd_mods).parse_args(args=arguments)

    app._run_command(state, cmd, cmd_mods, args)

def add_data(state, **kvs):
    if not state:
        state = TestState()

    for id, data in kvs.items():
        for key, value in data.items():
            if not type(value) == list:
                data[key] = [str(value)]

        path = _abs(id)
        if not 'ID' in data:
            data['ID'] = [id]
        data[_PATH] = path
        state.dat[path] = data

class TestState(st.State):
    def __init__(self):
        self.dat = {}
        self.root = _abs('.')

    def _load(self, path):
        pass

    def _load_all(self):
        pass

    def save(self, key):
        data = self.get(key)
        if not data:
            raise Exception('Unknown key "%s"' % (key,))

    def expand_paths(self, paths, only_items=True, only_existing=True):
        return paths

    def relative_path(self, id):
        data = self.get(id)
        return data.get(_PATH, '')

class TC(unittest.TestCase):
    def setUp(self):
        self.new_state()

    def new_state(self):
        self.state = TestState()

    def assertCount(self, num):
        """Checks that the number of items are equal to num."""
        self.assertEqual(len(self.state.get_all()), num)

    def assertHas(self, id, key, value):
        data = self.state.get(id) or {}
        values = []

        for line in data.get(key, []):
            if line.strip():
                values.append(line)

        self.assertTrue(value in values,
                        msg='Did not find "%s" in %s' % (value, values))
