from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import debug
from uplogic.utils import not_met
import bpy
import json
import os


class ULClearVariables(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.path = ''
        self.file_name = ''
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def write_to_json(self, path):
        data = None
        if not path.endswith('.json'):
            path = path + f'{self.file_name}.json'
        if os.path.isfile(path):
            data = {}
            f = open(path, 'w')
            json.dump(data, f, indent=2)
        else:
            debug('File does not exist - creating...')
            f = open(path, 'w')
            data = {}
            json.dump(data, f, indent=2)
        f.close()

    def get_custom_path(self, path):
        if not path.endswith('/') and not path.endswith('json'):
            path = path + '/'
        return path

    def evaluate(self):
        self.done = False
        condition = self.get_input(self.condition)
        if not_met(condition):
            return
        self._set_ready()
        cust_path = self.get_custom_path(self.path)

        path = (
            bpy.path.abspath('//Data/')
            if self.path == ''
            else bpy.path.abspath(cust_path)
        )
        os.makedirs(path, exist_ok=True)

        self.write_to_json(path)
        self.done = True
