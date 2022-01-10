from bge import logic
from uplogic.nodes import ULActionNode
from uplogic.utils import is_invalid
from uplogic.utils import not_met
import bpy


class ULSetOverlayCollection(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.camera = None
        self.collection = None

    def evaluate(self):
        condition = self.get_input(self.condition)
        if not_met(condition):
            return
        collection = self.get_input(self.collection)
        camera = self.get_input(self.camera)
        if is_invalid(camera, collection):
            return
        self._set_ready()
        col = bpy.data.collections.get(collection)
        if not col:
            return
        logic.getCurrentScene().addOverlayCollection(camera, col)
        self._set_value(True)
