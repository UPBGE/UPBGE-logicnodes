from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULParameterNode
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_invalid
from uplogic.utils import check_game_object
import bpy


class ULGetCollectionObjects(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
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
                objects.append(check_game_object(o.name))
            return self.set_output('objects', objects)
        return socket

    def evaluate(self):
        self._set_ready()
