from uplogic.nodes import ULParameterNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_invalid


class ULScreenPosition(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.game_object = None
        self.camera = None
        self.xposition = ULOutSocket(self, self._get_xposition)
        self.yposition = ULOutSocket(self, self._get_yposition)
        self._xpos = None
        self._ypos = None

    def _get_xposition(self):
        return self._xpos

    def _get_yposition(self):
        return self._ypos

    def evaluate(self):
        self._set_ready()
        game_object = self.get_socket_value(self.game_object)
        camera = self.get_socket_value(self.camera)
        if is_invalid(game_object) or is_invalid(camera):
            self._xpos = None
            self._ypos = None
            self._set_value(None)
            return
        position = camera.getScreenPosition(game_object)
        self._set_value(position)
        self._xpos = position[0]
        self._ypos = position[1]
