from bge import logic
from uplogic.nodes import ULActionNode
from uplogic.utils import is_invalid
from uplogic.utils import not_met
import bpy


class ULRemoveOverlayCollection(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.collection = None

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        collection = self.get_socket_value(self.collection)
        if is_invalid(collection):
            return
        self._set_ready()
        col = bpy.data.collections.get(collection)
        if not col:
            return
        logic.getCurrentScene().removeOverlayCollection(col)
        self._set_value(True)
