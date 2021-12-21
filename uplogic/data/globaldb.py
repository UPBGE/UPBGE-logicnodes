'''TODO: Documentation
'''

from bge import logic
import bpy
import os
from uplogic.utils import debug
from uplogic.utils import unload_nodes


class GlobalDB(object):
    '''TODO: Documentation
    '''
    index: int

    class LineBuffer(object):
        def __init__(self, buffer=[]):
            self.buffer = buffer
            self.index = 0
            self.size = len(self.buffer)

        def read(self):
            line = self.buffer[self.index]
            self.index += 1
            return line

        def write(self, line):
            self.buffer.append(line + "\n")

        def has_next(self):
            return self.index < self.size

        def flush(self, file):
            with open(file, "a") as f:
                f.writelines(self.buffer)

    class Serializer(object):
        def read(self, line_reader):
            raise NotImplementedError()

        def write(self, value, line_writer):
            raise NotImplementedError()

    serializers = {}
    storage_dir = logic.expandPath("//Globals")
    shared_dbs = {}

    @classmethod
    def retrieve(cls, fname):
        '''TODO: Documentation
        '''
        db = cls.shared_dbs.get(fname)
        if db is None:
            db = GlobalDB(fname)
            cls.shared_dbs[fname] = db
        return db

    @classmethod
    def get_storage_dir(cls):
        '''TODO: Documentation
        '''
        return cls.storage_dir

    @classmethod
    def put_value(cls, key, value, buffer):
        '''TODO: Documentation
        '''
        type_name = str(type(value))
        serializer = cls.serializers.get(type_name)
        if not serializer:
            return False
        buffer.write("PUT")
        buffer.write(key)
        buffer.write(type_name)
        serializer.write(value, buffer)

    @classmethod
    def read_existing(cls, fpath, intodic):
        '''TODO: Documentation
        '''
        lines = []
        with open(fpath, "r") as f:
            lines.extend(f.read().splitlines())
        buffer = GlobalDB.LineBuffer(lines)
        log_size = 0
        while buffer.has_next():
            op = buffer.read()
            assert op == "PUT"
            key = buffer.read()
            type_id = buffer.read()
            serializer = GlobalDB.serializers.get(type_id)
            value = serializer.read(buffer)
            intodic[key] = value
            log_size += 1
        return log_size

    @classmethod
    def write_put(cls, fname, key, value):
        '''TODO: Documentation
        '''
        type_name = str(type(value))
        serializer = cls.serializers.get(type_name)
        if not serializer:
            return  # no serializer for given value type
        if not os.path.exists(cls.get_storage_dir()):
            os.mkdir(cls.get_storage_dir())
        fpath = os.path.join(
            cls.get_storage_dir(),
            "{}.logdb.txt".format(fname)
        )
        buffer = GlobalDB.LineBuffer()
        cls.put_value(key, value, buffer)
        buffer.flush(fpath)

    @classmethod
    def read(cls, fname, intodic):
        '''TODO: Documentation
        '''
        fpath = os.path.join(
            cls.get_storage_dir(),
            "{}.logdb.txt".format(fname)
        )
        if os.path.exists(fpath):
            return cls.read_existing(fpath, intodic)
        else:
            return 0

    @classmethod
    def compress(cls, fname, content):
        '''TODO: Documentation
        '''
        buffer = GlobalDB.LineBuffer()
        for key in content:
            value = content[key]
            cls.put_value(key, value, buffer)
        fpath = os.path.join(
            cls.get_storage_dir(),
            "{}.logdb.txt".format(fname)
        )
        with open(fpath, "w") as f:
            f.writelines(buffer.buffer)

    def __init__(self, file_name):
        self.fname = file_name
        self.locked = {}
        self.content = {}

        filter(
            lambda a: a.__name__ == 'unload_nodes',
            bpy.app.handlers.game_post
        )
        remove_f = []
        for f in bpy.app.handlers.game_post:
            if f.__name__ == 'unload_nodes':
                remove_f.append(f)
        for f in remove_f:
            bpy.app.handlers.game_post.remove(f)
        bpy.app.handlers.game_post.append(unload_nodes)

        log_size = GlobalDB.read(self.fname, self.content)
        if log_size > (5 * len(self.content)):
            debug("Compressing sld {}".format(file_name))
            GlobalDB.compress(self.fname, self.content)

    def lock(self, item, event):
        self.locked[item] = event

    def unlock(self, item):
        self.locked.pop(item)

    def get(self, key, default_value=None):
        '''TODO: Documentation
        '''
        if not key:
            return default_value
        return self.content.get(key, default_value)

    def clear(self):
        '''TODO: Documentation
        '''
        self.content.clear()

    def put(self, key, value, persist=False):
        '''TODO: Documentation
        '''
        self.content[key] = value
        if persist:
            old_value = self.content.get(key)
            changed = old_value != value
            if changed:
                GlobalDB.write_put(self.fname, key, value)

    def check(self, key):
        '''TODO: Documentation
        '''
        valid = key in self.content
        return valid

    def pop(self, key, default=None):
        '''TODO: Documentation
        '''
        if not key:
            return default
        return self.content.pop(key, default)

    def log(self):
        '''TODO: Documentation
        '''
        print(self.content)
