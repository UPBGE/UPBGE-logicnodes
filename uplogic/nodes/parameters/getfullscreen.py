from bge import render
from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULParameterNode


class ULGetFullscreen(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.OUT = ULOutSocket(self.get_vsync)

    def get_vsync(self):
        return render.getFullScreen()

    def evaluate(self):
        self._set_ready()
