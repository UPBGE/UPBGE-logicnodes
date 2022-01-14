from uplogic.nodes import ULParameterNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import debug
import bpy
import json
import os


class ULLoadVariableDict(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.path = ''
        self.file_name = ''
        self.var = None
        self.VAR = ULOutSocket(self, self.get_var)

    def get_var(self):
        socket = self.get_output('var')
        if socket is None:
            cust_path = self.get_custom_path(self.path)

            path = (
                bpy.path.abspath('//Data/')
                if self.path == ''
                else bpy.path.abspath(cust_path)
            )
            os.makedirs(path, exist_ok=True)

            return self.set_output(
                'var',
                self.read_from_json(path)
            )
        return socket

    def read_from_json(self, path):
        self.done = False
        if not path.endswith('.json'):
            path = path + f'{self.file_name}.json'
        if not os.path.isfile(path):
            debug('No Saved Variables!')
            return
        f = open(path, 'r')
        data = json.load(f)
        self.var = data
        f.close()

    def get_custom_path(self, path):
        if not path.endswith('/') and not path.endswith('json'):
            path = path + '/'
        return path

    def evaluate(self):
        self._set_ready()
