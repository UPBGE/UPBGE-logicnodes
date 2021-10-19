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
        collection = self.get_socket_value(self.collection)
        if is_invalid(collection):
            return STATUS_WAITING
        col = bpy.data.collections.get(collection)
        if not col:
            return STATUS_WAITING
        objects = []
        for o in col.objects:
            objects.append(check_game_object(o.name))
        return objects

    def evaluate(self):
        self._set_ready()
