from bge import logic
from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULParameterNode
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_invalid


class ULActiveCamera(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.OUT = ULOutSocket(self, self.get_camera)

    def get_camera(self):
        scene = logic.getCurrentScene()
        if is_invalid(scene):
            return STATUS_WAITING
        return scene.active_camera

    def evaluate(self):
        self._set_ready()
