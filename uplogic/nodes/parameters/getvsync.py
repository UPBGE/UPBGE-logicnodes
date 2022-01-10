from bge import render
from uplogic.nodes import ULParameterNode


class ULGetVSync(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)

    def evaluate(self):
        self._set_ready()
        self._set_value(render.getVsync())
