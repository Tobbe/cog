import os

import cog_tool.common as common

_abs = os.path.abspath
_PATH = object()

class State(object):
    def __init__(self, start_path='.'):
        self.root = _abs(start_path)
        self.dat = {}

        self._setup_root(_abs(start_path))
        self._load_all()

    def _setup_root(self, path):
        next = os.path.dirname(path)
        if path == next:
            raise Exception('Failed to find .cogfig file.')

        for fn in os.listdir(path):
            if fn == '.cogfig':
                self.root = path
                return

        self._setup_root(next)

    def get(self, key):
        return self.get_by_path(key) or self.get_by_key('ID', key)

    def get_by_path(self, path):
        path = _abs(path)
        self._load(path)
        return self.dat.get(_abs(path), None)

    def get_by_key(self, key, value):
        for data in self.dat.values():
            if common.get_value(data, key) == value:
                return data

    def _load(self, path):
        if path in self.dat:
            return
        data = common.load(path)
        data[_PATH] = path
        self.dat[path] = data

    def _load_all(self):
        for path in common.find_all_files([self.root]):
            self._load(path)
