from uplogic.nodes import ULParameterNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import STATUS_WAITING, is_invalid
from mathutils import Vector


class ULScreenPosition(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.game_object = None
        self.camera = None
        self.pos = None
        self.OUT = ULOutSocket(self, self.get_pos)

    def get_pos(self):
        game_object = self.get_input(self.game_object)
        camera = self.get_input(self.camera)
        if is_invalid(game_object) or is_invalid(camera):
            return STATUS_WAITING
        position = camera.getScreenPosition(game_object)
        self._set_value(position)
        return Vector((position[0], position[1]))

    def evaluate(self):
        self._set_ready()
