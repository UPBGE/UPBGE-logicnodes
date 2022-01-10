from bge import logic
from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_waiting
from uplogic.utils import is_invalid
from uplogic.utils import not_met


class ULSetCamera(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.camera = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_input(self.condition)
        if not_met(condition):
            return
        camera = self.get_input(self.camera)
        if is_waiting(camera):
            return
        self._set_ready()
        if is_invalid(camera):
            return
        scene = logic.getCurrentScene()
        scene.active_camera = camera
        self.done = True
