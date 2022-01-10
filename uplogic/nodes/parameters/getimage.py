from uplogic.nodes import ULParameterNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_invalid
import bpy


class ULGetImage(ULParameterNode):

    def __init__(self):
        ULParameterNode.__init__(self)
        self.image = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        image = self.get_input(self.image)
        if is_invalid(image):
            return
        return bpy.data.images[image]

    def evaluate(self):
        self._set_ready()
