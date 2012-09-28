import copy
import os

import cog_tool.common as common

_abs = os.path.abspath
_PATH = "_COG_INTERNAL_PATH"

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

    def get_all(self):
        self._load_all()
        return self.dat.values()

    def _load(self, path):
        path = _abs(path)
        if path in self.dat:
            return
        if not os.path.exists(path):
            return
        if not path.endswith('.txt'):
            return
        data = common.load(path)
        data[_PATH] = path
        self.dat[path] = data

    def _load_all(self):
        for path in common.find_all_files([self.root]):
            self._load(path)

    def new(self, path):
        path = _abs(path)
        data = {_PATH: path}
        self.dat[path] = data
        return data

    def save(self, key):
        data = self.get(key)
        if not data:
            raise Exception('Unknown key "%s"' % (key,))

        path = data[_PATH]
        save_data = copy.deepcopy(data)
        del save_data[_PATH]
        common.save(path, save_data)

    def expand_paths(self, paths, only_items=True, only_existing=True):
        result = common.expand_dirs(paths)
        if only_items:
            result = common.filter_existing(result)
        if only_existing:
            result = common.filter_items(result)
        return result
