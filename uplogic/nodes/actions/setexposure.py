from bge import logic
from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_invalid
from uplogic.utils import not_met
import bpy


class ULSetExposure(ULActionNode):

    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.value = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_input(self.condition)
        if not_met(condition):
            return
        value = self.get_input(self.value)
        if is_invalid(value):
            return
        self._set_ready()
        scene = logic.getCurrentScene()
        bpy.data.scenes[
            scene.name
        ].view_settings.exposure = value
        self.done = True
