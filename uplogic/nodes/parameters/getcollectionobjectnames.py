from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULParameterNode
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_invalid
import bpy


class ULGetCollectionObjectNames(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.condition = None
        self.collection = None
        self.OUT = ULOutSocket(self, self.get_objects)

    def get_objects(self):
        socket = self.get_output('objects')
        if socket is None:
            collection = self.get_input(self.collection)
            if is_invalid(collection):
                return STATUS_WAITING
            col = bpy.data.collections.get(collection)
            if not col:
                return STATUS_WAITING
            objects = []
            for o in col.objects:
                if not o.parent:
                    objects.append(o.name)
            return self.set_output('objects', objects)
        return socket

    def evaluate(self):
        self._set_ready()
