from bge import render
from mathutils import Vector
from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULParameterNode


class ULGetResolution(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.width = None
        self.height = None
        self.res = None
        self.WIDTH = ULOutSocket(self, self.get_width)
        self.HEIGHT = ULOutSocket(self, self.get_height)
        self.RES = ULOutSocket(self, self.get_res)

    def get_width(self):
        return render.getWindowWidth()

    def get_height(self):
        return render.getWindowHeight()

    def get_res(self):
        return Vector((self.width, self.height))

    def evaluate(self):
        self._set_ready()
